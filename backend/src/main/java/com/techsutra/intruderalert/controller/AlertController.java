package com.techsutra.intruderalert.controller;

import com.techsutra.intruderalert.model.AlertRecord;
import com.techsutra.intruderalert.model.AlertRequest;
import com.techsutra.intruderalert.service.AlertService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/alerts")
@CrossOrigin(origins = "*")
public class AlertController {
    private final AlertService alertService;

    public AlertController(AlertService alertService) {
        this.alertService = alertService;
    }

    @GetMapping
    public List<AlertRecord> getAlerts() {
        return alertService.getAllAlerts();
    }

    @GetMapping("/latest")
    public AlertRecord getLatestAlert() {
        return alertService.getLatestAlert();
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public AlertRecord createAlert(@RequestBody AlertRequest request) {
        return alertService.createAlert(request);
    }

    @DeleteMapping
    public Map<String, String> clearAlerts() {
        alertService.clearAlerts();
        return Map.of("status", "cleared");
    }
}
