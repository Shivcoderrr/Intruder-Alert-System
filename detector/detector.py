import base64
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import List

import cv2
import face_recognition
import requests
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
KNOWN_FACES_DIR = BASE_DIR / "known_faces"
CAPTURES_DIR = BASE_DIR / "captures"


class KnownFace:
    def __init__(self, name: str, encoding) -> None:
        self.name = name
        self.encoding = encoding


class IntruderDetector:
    def __init__(self) -> None:
        load_dotenv(BASE_DIR / ".env")
        CAPTURES_DIR.mkdir(exist_ok=True)

        # These settings keep the detector easy to tune without touching code.
        self.backend_alert_url = os.getenv(
            "BACKEND_ALERT_URL", "http://localhost:8080/api/alerts"
        )
        self.camera_id = os.getenv("CAMERA_ID", "CAM-01")
        self.alert_cooldown_seconds = int(os.getenv("ALERT_COOLDOWN_SECONDS", "20"))
        self.face_match_tolerance = float(os.getenv("FACE_MATCH_TOLERANCE", "0.48"))
        self.last_alert_time = 0.0
        self.known_faces = self._load_known_faces()

    def _person_key_from_path(self, image_path: Path) -> str:
        stem = image_path.stem.strip()

        # Allow multiple files per person like harry_1.jpg, harry_2.jpg.
        if "_" in stem:
            return stem.rsplit("_", 1)[0]

        return stem

    def _load_known_faces(self) -> List[KnownFace]:
        known_faces: List[KnownFace] = []

        for image_path in sorted(KNOWN_FACES_DIR.glob("*")):
            if image_path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                continue

            # Each image file contributes one reference encoding for an authorized person.
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if not encodings:
                print(f"[WARN] No face found in {image_path.name}. Skipping file.")
                continue

            known_faces.append(
                KnownFace(name=self._person_key_from_path(image_path), encoding=encodings[0])
            )

        if not known_faces:
            raise RuntimeError(
                "No usable authorized faces found. Add clear photos to known_faces."
            )

        print(f"[INFO] Loaded {len(known_faces)} authorized face sample(s).")
        return known_faces

    def _recognize_face(self, face_encoding) -> tuple[bool, str]:
        matches = face_recognition.compare_faces(
            [face.encoding for face in self.known_faces],
            face_encoding,
            tolerance=self.face_match_tolerance,
        )

        if True not in matches:
            return False, "Unknown"

        face_distances = face_recognition.face_distance(
            [face.encoding for face in self.known_faces], face_encoding
        )
        best_match_index = face_distances.argmin()
        return True, self.known_faces[best_match_index].name

    def _save_capture(self, frame) -> Path:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        filename = f"intruder_{timestamp}.jpg"
        capture_path = CAPTURES_DIR / filename
        cv2.imwrite(str(capture_path), frame)
        return capture_path

    def _encode_image(self, image_path: Path) -> str:
        with image_path.open("rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def _send_alert(self, capture_path: Path) -> None:
        now = time.time()
        # Cooldown prevents repeated alerts from flooding the dashboard.
        if now - self.last_alert_time < self.alert_cooldown_seconds:
            return

        timestamp = datetime.now(timezone.utc).isoformat()
        payload = {
            "cameraId": self.camera_id,
            "timestamp": timestamp,
            "imageBase64": self._encode_image(capture_path),
            "fileName": capture_path.name,
            "message": "Unauthorized person detected near secured area.",
        }

        try:
            response = requests.post(self.backend_alert_url, json=payload, timeout=5)
            response.raise_for_status()
            self.last_alert_time = now
            print(f"[ALERT] Intruder sent to backend at {timestamp}")
        except requests.RequestException as exc:
            print(f"[ERROR] Failed to send alert: {exc}")

    def run(self) -> None:
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            raise RuntimeError("Could not open webcam.")

        print("[INFO] Detector started. Press 'q' to quit.")

        while True:
            success, frame = video_capture.read()
            if not success:
                print("[WARN] Failed to read frame from webcam.")
                continue

            # Detection runs on a smaller frame for better speed during demos.
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations
            )

            intruder_detected = False

            for (top, right, bottom, left), face_encoding in zip(
                face_locations, face_encodings
            ):
                authorized, name = self._recognize_face(face_encoding)

                # Scale face boxes back up to original webcam resolution.
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                box_color = (60, 180, 75) if authorized else (0, 0, 255)
                label_text = name if authorized else "Unknown"

                cv2.rectangle(frame, (left, top), (right, bottom), box_color, 2)
                cv2.putText(
                    frame,
                    label_text,
                    (left, max(top - 10, 25)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    box_color,
                    2,
                )

                if not authorized:
                    intruder_detected = True

            status_text = "System Secure"
            status_color = (60, 180, 75)

            if intruder_detected:
                status_text = "Intruder Detected"
                status_color = (0, 0, 255)
                capture_path = self._save_capture(frame)
                self._send_alert(capture_path)

            cv2.putText(
                frame,
                status_text,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                status_color,
                2,
            )

            cv2.imshow("Smart Intruder Alert System", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    detector = IntruderDetector()
    detector.run()
