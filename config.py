import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is required")

PLAYLISTS_DIR = Path(os.getenv("PLAYLISTS_DIR", "./playlists"))
if not PLAYLISTS_DIR.exists():
    raise ValueError(f"Playlists directory not found: {PLAYLISTS_DIR}")

AUDIO_VOLUME = 0.5
AUDIO_BITRATE = 128
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

SUPPORTED_FORMATS = {'.mp3', '.m4a', '.wav', '.ogg', '.flac', '.opus', '.webm'}

DEFAULT_PLAYLIST = "default"
COMMAND_PREFIX = "/"
