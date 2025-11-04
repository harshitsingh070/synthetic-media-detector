package com.synthdetect.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import com.synthdetect.model.DetectionResult;

@Service
public class DetectionService {

    private static final Logger log = LoggerFactory.getLogger(DetectionService.class);
    
    @Value("${ml.service.url:http://ml-service:8000}")
    private String mlServiceUrl;

    private final RestTemplate restTemplate = new RestTemplate();

    public DetectionResult detectImage(MultipartFile file) throws Exception {
        return callMLService(file, "/api/detect/image");
    }

    public DetectionResult detectAudio(MultipartFile file) throws Exception {
        return callMLService(file, "/api/detect/audio");
    }

    public DetectionResult detectVideo(MultipartFile file) throws Exception {
        return callMLService(file, "/api/detect/video");
    }

    private DetectionResult callMLService(MultipartFile file, String endpoint) throws Exception {
        try {
            String url = mlServiceUrl + endpoint;
            log.info("Calling ML service: {}", url);
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.MULTIPART_FORM_DATA);
            
            ByteArrayResource fileResource = new ByteArrayResource(file.getBytes()) {
                @Override
                public String getFilename() {
                    return file.getOriginalFilename();
                }
            };
            
            MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
            body.add("file", fileResource);
            
            HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
            
            ResponseEntity<DetectionResult> response = restTemplate.exchange(
                url, HttpMethod.POST, requestEntity, DetectionResult.class
            );
            
            if (response.getBody() != null) {
                DetectionResult result = response.getBody();
                log.info("ML service response: {} ({}%)", result.getPrediction(), 
                    Math.round(result.getConfidence() * 100));
                return result;
            } else {
                throw new Exception("No response from ML service");
            }
            
        } catch (Exception e) {
            log.error("ML service call failed: {}", e.getMessage());
            throw e;
        }
    }
}
