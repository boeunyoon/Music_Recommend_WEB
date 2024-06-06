package musicweb.backend.controller.musiccontroller;

import lombok.RequiredArgsConstructor;
import musicweb.backend.entity.musicentity.ArtistEntity;
import musicweb.backend.entity.musicentity.SongEntity;
import musicweb.backend.service.musicservice.ArtistSongService;
import musicweb.backend.service.musicservice.SongSearchService;
import org.json.simple.JSONObject;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;

@RestController
@RequiredArgsConstructor
@CrossOrigin(origins = "http://localhost:3000")
public class MusicSearchController {
    private final SongSearchService songSearchService;
    private final ArtistSongService artistSongService;

    @GetMapping("/search")
    public ResponseEntity<?> searchSongs(@RequestParam("keyword") String keyword) {
        List<SongEntity> searchResults = songSearchService.searchByArtistAndTitle(keyword);
        return ResponseEntity.ok(searchResults);
    }
}
