package musicweb.backend.controller;

import lombok.RequiredArgsConstructor;
import musicweb.backend.service.ProfileService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class ProfileController {
    private final ProfileService profileService;
    @GetMapping("/profile")
    public ResponseEntity<?> getProfile(){
        ResponseEntity<?> profileData = profileService.getProfileData();
        return profileData;
    }
}
