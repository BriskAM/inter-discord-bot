from typing import Optional, List
from pathlib import Path
import discord
import asyncio
from collections import deque

from music.audio_source import create_audio_source


class MusicPlayer:
    def __init__(self, guild_id: int):
        self.guild_id = guild_id
        self.queue: deque[Path] = deque()
        self.current_track: Optional[Path] = None
        self.voice_client: Optional[discord.VoiceClient] = None
        self.is_playing = False
        self.is_paused = False
        self.volume = 0.5
    
    def add_tracks(self, tracks: List[Path]) -> None:
        self.queue.extend(tracks)
    
    def clear_queue(self) -> None:
        self.queue.clear()
    
    def skip(self) -> bool:
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()
            return True
        return False
    
    async def play_next(self) -> None:
        if not self.queue:
            self.is_playing = False
            self.current_track = None
            return
        
        self.current_track = self.queue.popleft()
        self.is_playing = True
        self.is_paused = False
        
        if self.voice_client and self.voice_client.is_connected():
            audio_source = create_audio_source(self.current_track)
            audio_source = discord.PCMVolumeTransformer(audio_source, volume=self.volume)
            
            self.voice_client.play(
                audio_source,
                after=lambda e: asyncio.run_coroutine_threadsafe(
                    self.play_next(), self.voice_client.loop
                )
            )
    
    async def start_playback(self, voice_client: discord.VoiceClient) -> bool:
        self.voice_client = voice_client
        
        if self.is_paused and voice_client.is_paused():
            voice_client.resume()
            self.is_paused = False
            return True
        
        if not self.is_playing and self.queue:
            await self.play_next()
            return True
        
        return False
    
    def pause(self) -> bool:
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.pause()
            self.is_paused = True
            return True
        return False
    
    def resume(self) -> bool:
        if self.voice_client and self.voice_client.is_paused():
            self.voice_client.resume()
            self.is_paused = False
            return True
        return False
    
    def stop(self) -> None:
        if self.voice_client:
            self.voice_client.stop()
        self.clear_queue()
        self.current_track = None
        self.is_playing = False
        self.is_paused = False
    
    def get_queue_list(self) -> List[Path]:
        return list(self.queue)
    
    def set_volume(self, volume: float) -> None:
        self.volume = max(0.0, min(1.0, volume))
