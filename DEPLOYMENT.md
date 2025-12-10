# Deployment Guide

This guide covers deploying the Discord Music Bot to a production server using Docker.

## Server Requirements

- **OS**: Linux (Ubuntu 20.04+ recommended)
- **Docker**: 20.10 or higher
- **Docker Compose**: V2
- **RAM**: Minimum 512MB (1GB recommended)
- **Storage**: Depends on your music library size
- **Network**: Stable internet connection

## Installation Steps

### 1. Install Docker and Docker Compose

```bash
# Update package index
sudo apt-get update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group (optional, to run without sudo)
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Compose V2
sudo apt-get install docker-compose-plugin

# Verify installation
docker --version
docker compose version
```

### 2. Clone and Configure

```bash
# Clone your repository (or upload files via SCP/SFTP)
git clone <your-repo-url> discord-music-bot
cd discord-music-bot

# Create .env file
cp .env.example .env
nano .env  # Add your DISCORD_TOKEN

# Upload your playlists
# You can use SCP, SFTP, or rsync to transfer your music files
# Example: scp -r ./playlists user@server:/path/to/discord-music-bot/
```

### 3. Build and Run

```bash
# Build the Docker image
docker compose build

# Start the bot in detached mode
docker compose up -d

# Check if it's running
docker compose ps

# View logs
docker compose logs -f bot
```

## Managing the Bot

### View Logs

```bash
# Real-time logs
docker compose logs -f bot

# Last 100 lines
docker compose logs --tail=100 bot
```

### Restart the Bot

```bash
# Restart
docker compose restart

# Or stop and start
docker compose down
docker compose up -d
```

### Update the Bot

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker compose down
docker compose build
docker compose up -d
```

## Volume Management

The `playlists` directory is mounted as a volume in the container. To manage your music:

```bash
# Add new playlists while bot is running
mkdir -p playlists/new-playlist
# Add music files to playlists/new-playlist/

# The bot will detect new playlists when you run /playlist list
```

## Production Best Practices

### 1. Use a Process Manager (Optional)

While Docker Compose has a restart policy, you can use systemd for additional control:

Create `/etc/systemd/system/discord-bot.service`:

```ini
[Unit]
Description=Discord Music Bot
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/path/to/discord-music-bot
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
StandardOutput=journal

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable discord-bot
sudo systemctl start discord-bot
```

### 2. Set Up Log Rotation

Docker automatically rotates logs based on the config in `docker-compose.yml`:

```yaml
logging:
  driver: json-file
  options:
    max-size: "10m"
    max-file: "3"
```

### 3. Monitor Resource Usage

```bash
# Check container stats
docker stats discord-music-bot

# Adjust resource limits in docker-compose.yml if needed
```

### 4. Backup Playlists

```bash
# Create backup
tar -czf playlists-backup-$(date +%Y%m%d).tar.gz playlists/

# Restore backup
tar -xzf playlists-backup-20231210.tar.gz
```

### 5. Security Considerations

- **Never commit `.env`** to version control
- Keep your bot token secret
- Use a non-root user (already configured in Dockerfile)
- Consider using Docker secrets for sensitive data in production
- Keep Docker and the host system updated

## Troubleshooting

### Bot crashes on startup

```bash
# Check logs for errors
docker compose logs bot

# Common issues:
# - Missing or invalid DISCORD_TOKEN
# - Playlists directory doesn't exist
# - Permission issues with playlists directory
```

### Out of memory errors

```bash
# Increase memory limit in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 1G  # Increase from 512M
```

### Bot not connecting to voice

```bash
# Ensure FFmpeg is properly installed (check Dockerfile)
# Verify audio files are accessible
docker compose exec bot ls -la /app/playlists

# Check if bot has proper Discord permissions
```

### Updating playlists doesn't reflect

```bash
# Restart the bot to rescan playlists
docker compose restart
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DISCORD_TOKEN` | Yes | - | Your Discord bot token |
| `PLAYLISTS_DIR` | No | `/app/playlists` | Path to playlists directory |

## Scaling Considerations

For multiple servers or high-traffic scenarios:

1. **Use a VPS with more resources**: Consider 2GB+ RAM
2. **Monitor performance**: Use `docker stats` to watch resource usage
3. **Consider sharding**: If the bot is in 2,500+ servers, implement sharding
4. **Use external storage**: Mount playlists from network storage for easier management

## Updating Dependencies

```bash
# Update Python packages
docker compose build --no-cache

# This will install the latest compatible versions from pyproject.toml
```

## Getting Help

- Check logs: `docker compose logs -f bot`
- Verify config: `cat .env`
- Test locally first before deploying to production
- Ensure all prerequisites are met

---

For additional help, check the [README.md](README.md) or create an issue in the repository.
