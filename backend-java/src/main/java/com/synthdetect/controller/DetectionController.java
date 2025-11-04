package com.synthdetect.controller;

import com.synthdetect.model.DetectionResult;
import com.synthdetect.service.DetectionService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class DetectionController {

    private static final Logger log = LoggerFactory.getLogger(DetectionController.class);
    
    @Autowired
    private DetectionService detectionService;

    @PostMapping("/detect/image")
    public ResponseEntity<DetectionResult> detectImage(@RequestParam("file") MultipartFile file) {
        try {
            log.info("Received image: {}", file.getOriginalFilename());
            
            if (file.isEmpty()) {
                throw new RuntimeException("File is empty");
            }
            
            DetectionResult result = detectionService.detectImage(file);
            return ResponseEntity.ok(result);
            
        } catch (Exception e) {
            log.error("Detection failed: {}", e.getMessage());
            
            // Return error as DetectionResult
            DetectionResult errorResult = new DetectionResult();
            errorResult.setPrediction("error");
            errorResult.setConfidence(0.0);
            errorResult.setFakeProbability(0.0);
            errorResult.setRealProbability(0.0);
            errorResult.setProcessingTime(0.0);
            return ResponseEntity.ok(errorResult);
        }
    }

    @PostMapping("/detect/audio")
    public ResponseEntity<DetectionResult> detectAudio(@RequestParam("file") MultipartFile file) {
        try {
            log.info("Received audio: {}", file.getOriginalFilename());
            DetectionResult result = detectionService.detectAudio(file);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            log.error("Audio detection failed: {}", e.getMessage());
            
            DetectionResult errorResult = new DetectionResult();
            errorResult.setPrediction("error");
            errorResult.setConfidence(0.0);
            return ResponseEntity.ok(errorResult);
        }
    }

    @PostMapping("/detect/video")
    public ResponseEntity<DetectionResult> detectVideo(@RequestParam("file") MultipartFile file) {
        try {
            log.info("Received video: {}", file.getOriginalFilename());
            DetectionResult result = detectionService.detectVideo(file);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            log.error("Video detection failed: {}", e.getMessage());
            
            DetectionResult errorResult = new DetectionResult();
            errorResult.setPrediction("error");
            errorResult.setConfidence(0.0);
            return ResponseEntity.ok(errorResult);
        }
    }
}
