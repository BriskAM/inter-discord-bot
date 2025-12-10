from commands.play import setup_play_command
from commands.stop import setup_stop_command
from commands.pause import setup_pause_command
from commands.resume import setup_resume_command
from commands.skip import setup_skip_command
from commands.queue import setup_queue_command
from commands.nowplaying import setup_nowplaying_command
from commands.playlist import setup_playlist_command

__all__ = [
    'setup_play_command',
    'setup_stop_command',
    'setup_pause_command',
    'setup_resume_command',
    'setup_skip_command',
    'setup_queue_command',
    'setup_nowplaying_command',
    'setup_playlist_command',
]
