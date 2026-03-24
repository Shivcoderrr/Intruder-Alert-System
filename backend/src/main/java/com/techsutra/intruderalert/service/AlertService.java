package com.techsutra.intruderalert.service;

import com.techsutra.intruderalert.model.AlertRecord;
import com.techsutra.intruderalert.model.AlertRequest;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.atomic.AtomicLong;

@Service
public class AlertService {
    private final AtomicLong idCounter = new AtomicLong(1);
    private final CopyOnWriteArrayList<AlertRecord> alerts = new CopyOnWriteArrayList<>();

    public AlertRecord createAlert(AlertRequest request) {
        // New alerts are inserted at the top so the dashboard can show the newest item first.
        AlertRecord alert = new AlertRecord(
                idCounter.getAndIncrement(),
                request.getCameraId(),
                request.getTimestamp(),
                request.getImageBase64(),
                request.getFileName(),
                request.getMessage(),
                "HIGH"
        );

        alerts.add(0, alert);
        return alert;
    }

    public List<AlertRecord> getAllAlerts() {
        return Collections.unmodifiableList(new ArrayList<>(alerts));
    }

    public AlertRecord getLatestAlert() {
        return alerts.isEmpty() ? null : alerts.get(0);
    }

    public void clearAlerts() {
        alerts.clear();
    }
}
