import discord
from pathlib import Path
import config


def create_audio_source(file_path: Path) -> discord.FFmpegOpusAudio:
    return discord.FFmpegOpusAudio(
        str(file_path),
        bitrate=config.AUDIO_BITRATE,
        **config.FFMPEG_OPTIONS
    )
