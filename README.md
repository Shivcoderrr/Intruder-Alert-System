# Smart Intruder Alert System

Demo-ready college showcase project built as a 3-part system:

- `detector/`: Python webcam monitor with face recognition and alert posting
- `backend/`: Spring Boot API with in-memory alert storage
- `frontend/`: React dashboard for live monitoring

## Architecture

1. The Python detector reads faces from `detector/known_faces/`.
2. When an unknown face is seen, it saves a snapshot in `detector/captures/`.
3. The detector sends the alert data to the Spring Boot backend.
4. The React dashboard polls the backend and renders the latest alerts.

## Demo Flow

1. Add authorized face images to `detector/known_faces/`.
2. Start the backend.
3. Start the frontend.
4. Start the detector.
5. Show an authorized user first.
6. Show an unauthorized user to trigger the alert dashboard.

## Setup

### Backend

- Java 17+
- Maven 3.9+

```powershell
cd backend
mvn spring-boot:run
```

Backend runs on `http://localhost:8080`.

### Frontend

- Node.js 18+

```powershell
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`.

### Detector

- Python 3.11 recommended

Install dependencies:

```powershell
cd detector
pip install -r requirements.txt
```

Run:

```powershell
python detector.py
```

## Notes

- The detector uses OpenCV face detection plus LBPH recognition so it is easier to run on Windows for live demos.
- Alert suppression is built in so the same person does not spam the system every frame.
- The backend uses in-memory storage to keep the project simple for a showcase.
