# Discord Music Bot

A Discord bot that plays music from local playlists stored in folders. Built with discord.py, Docker, and uv for fast dependency management.

## Features

- 🎵 Play music from local playlists
- 📁 Multiple playlist support with easy switching
- ⏯️ Full playback controls (play, pause, resume, stop, skip)
- 📋 Queue management
- 🔊 Volume control
- 🐳 Docker containerized for easy deployment
- ⚡ Fast dependency installation with uv

## Commands

- `/play` - Start playing music from the current playlist
- `/stop` - Stop playback and disconnect from voice channel
- `/pause` - Pause the current track
- `/resume` - Resume paused playback
- `/skip` - Skip to the next track
- `/queue` - Display the current music queue
- `/nowplaying` - Show information about the current track
- `/playlist list` - Show all available playlists
- `/playlist switch <name>` - Switch to a different playlist
- `/playlist current` - Show the current playlist

## Prerequisites

- **Docker** (20.10+) and **Docker Compose** (V2)
- **Discord Bot Token** - Create a bot at [Discord Developer Portal](https://discord.com/developers/applications)
- **Audio Files** - MP3, M4A, WAV, OGG, FLAC files organized in playlist folders

## Setup

### 1. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Under "Privileged Gateway Intents", enable:
   - `SERVER MEMBERS INTENT`
   - `VOICE STATES`
5. Copy the bot token (you'll need this later)
6. Go to "OAuth2" → "URL Generator"
7. Select scopes: `bot`, `applications.commands`
8. Select bot permissions: `Connect`, `Speak`, `Use Slash Commands`
9. Copy the generated URL and use it to invite the bot to your server

### 2. Configure the Bot

```bash
# Clone or navigate to the project directory
cd inter-discord-bot

# Copy the environment template
cp .env.example .env

# Edit .env and add your bot token
# DISCORD_TOKEN=your_bot_token_here
```

### 3. Set Up Playlists

Create playlist folders in the `playlists` directory:

```
playlists/
├── chill-vibes/
│   ├── track1.mp3
│   ├── track2.mp3
│   └── track3.mp3
├── workout/
│   ├── song1.mp3
│   └── song2.mp3
└── study-music/
    └── ambient1.mp3
```

Supported audio formats: `.mp3`, `.m4a`, `.wav`, `.ogg`, `.flac`, `.opus`, `.webm`

### 4. Run with Docker Compose

```bash
# Build and start the bot
docker-compose up -d

# View logs
docker-compose logs -f bot

# Stop the bot
docker-compose down
```

## Local Development (without Docker)

If you want to run the bot locally without Docker:

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv pip install -e .

# Ensure FFmpeg is installed
# macOS: brew install ffmpeg
# Ubuntu: sudo apt-get install ffmpeg

# Run the bot
python bot.py
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions for production servers.

## Project Structure

```
inter-discord-bot/
├── bot.py                 # Main bot entry point
├── config.py              # Configuration management
├── music/                 # Music system
│   ├── player.py          # Music player with queue
│   ├── playlist_manager.py # Playlist management
│   └── audio_source.py    # FFmpeg audio source
├── commands/              # Slash commands
│   ├── play.py
│   ├── stop.py
│   ├── pause.py
│   ├── resume.py
│   ├── skip.py
│   ├── queue.py
│   ├── nowplaying.py
│   └── playlist.py
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker Compose config
├── pyproject.toml         # Python dependencies (uv)
└── playlists/             # Your music playlists
```

## Configuration

Edit `config.py` to customize:
- Audio volume (default: 0.5)
- Audio bitrate (default: 128 kbps)
- FFmpeg options
- Supported audio formats

## Troubleshooting

### Bot doesn't appear online
- Check that your bot token is correct in `.env`
- Verify the bot is running: `docker-compose logs -f bot`

### No slash commands showing
- Wait a few minutes for Discord to sync commands
- Try kicking and re-inviting the bot

### Bot can't play audio
- Ensure FFmpeg is installed in the container (it should be via Dockerfile)
- Check audio file formats are supported
- Verify playlist folder structure

### Bot disconnects immediately
- Check Docker logs for errors
- Ensure you're in a voice channel when using `/play`

## License

MIT License - Feel free to modify and use as you wish!
