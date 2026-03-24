package com.techsutra.intruderalert.model;

public class AlertRecord {
    private Long id;
    private String cameraId;
    private String timestamp;
    private String imageBase64;
    private String fileName;
    private String message;
    private String severity;

    public AlertRecord() {
    }

    public AlertRecord(
            Long id,
            String cameraId,
            String timestamp,
            String imageBase64,
            String fileName,
            String message,
            String severity
    ) {
        this.id = id;
        this.cameraId = cameraId;
        this.timestamp = timestamp;
        this.imageBase64 = imageBase64;
        this.fileName = fileName;
        this.message = message;
        this.severity = severity;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getCameraId() {
        return cameraId;
    }

    public void setCameraId(String cameraId) {
        this.cameraId = cameraId;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    public String getImageBase64() {
        return imageBase64;
    }

    public void setImageBase64(String imageBase64) {
        this.imageBase64 = imageBase64;
    }

    public String getFileName() {
        return fileName;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getSeverity() {
        return severity;
    }

    public void setSeverity(String severity) {
        this.severity = severity;
    }
}
