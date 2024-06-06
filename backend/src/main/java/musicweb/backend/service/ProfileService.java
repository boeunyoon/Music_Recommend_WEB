package musicweb.backend.service;

import lombok.RequiredArgsConstructor;
import musicweb.backend.service.musicservice.RecommendService;
import org.json.simple.JSONObject;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
@RequiredArgsConstructor
public class ProfileService {
    private final RestTemplate restTemplate;
    private final RecommendService recommendService;
    public ResponseEntity<?> getProfileData(){
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        String url = "http://127.0.0.1:8000/profile";
        JSONObject jsonObject = recommendService.makeTrackListForm();
        HttpEntity<JSONObject> request = new HttpEntity<>(jsonObject, headers);
        ResponseEntity<String> response = restTemplate.postForEntity(url, request, String.class);
        if (response.getStatusCode().is2xxSuccessful()){
            return response;
        }else {
            return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
        }
    }
}
