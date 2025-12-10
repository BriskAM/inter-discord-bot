from pathlib import Path
from typing import List, Optional
import config


class PlaylistManager:
    def __init__(self):
        self.playlists_dir = config.PLAYLISTS_DIR
        self.current_playlist: Optional[str] = None
        self._scan_playlists()
    
    def _scan_playlists(self) -> None:
        self.available_playlists = [
            d.name for d in self.playlists_dir.iterdir()
            if d.is_dir() and not d.name.startswith('.')
        ]
        
        if config.DEFAULT_PLAYLIST in self.available_playlists:
            self.current_playlist = config.DEFAULT_PLAYLIST
        elif self.available_playlists:
            self.current_playlist = self.available_playlists[0]
    
    def get_playlists(self) -> List[str]:
        self._scan_playlists()
        return self.available_playlists
    
    def get_current_playlist(self) -> Optional[str]:
        return self.current_playlist
    
    def switch_playlist(self, playlist_name: str) -> bool:
        self._scan_playlists()
        if playlist_name in self.available_playlists:
            self.current_playlist = playlist_name
            return True
        return False
    
    def get_tracks(self, playlist_name: Optional[str] = None) -> List[Path]:
        if playlist_name is None:
            playlist_name = self.current_playlist
        
        if not playlist_name or playlist_name not in self.available_playlists:
            return []
        
        playlist_path = self.playlists_dir / playlist_name
        tracks = []
        
        for file_path in sorted(playlist_path.iterdir()):
            if file_path.is_file() and file_path.suffix.lower() in config.SUPPORTED_FORMATS:
                tracks.append(file_path)
        
        return tracks
    
    def validate_playlist(self, playlist_name: str) -> bool:
        return playlist_name in self.available_playlists and len(self.get_tracks(playlist_name)) > 0
