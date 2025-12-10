import discord
from discord import app_commands
import asyncio
import logging
from typing import Dict

import config
from music import MusicPlayer, PlaylistManager
from commands import (
    setup_play_command,
    setup_stop_command,
    setup_pause_command,
    setup_resume_command,
    setup_skip_command,
    setup_queue_command,
    setup_nowplaying_command,
    setup_playlist_command,
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('discord_music_bot')


class MusicBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.voice_states = True
        intents.guilds = True
        
        super().__init__(intents=intents)
        
        self.tree = app_commands.CommandTree(self)
        self.players: Dict[int, MusicPlayer] = {}
        self.playlist_manager = PlaylistManager()
    
    async def setup_hook(self):
        logger.info("Setting up commands...")
        
        await setup_play_command(self.tree, self.players, self.playlist_manager)
        await setup_stop_command(self.tree, self.players)
        await setup_pause_command(self.tree, self.players)
        await setup_resume_command(self.tree, self.players)
        await setup_skip_command(self.tree, self.players)
        await setup_queue_command(self.tree, self.players)
        await setup_nowplaying_command(self.tree, self.players, self.playlist_manager)
        await setup_playlist_command(self.tree, self.players, self.playlist_manager)
        
        logger.info("Syncing commands with Discord...")
        await self.tree.sync()
        logger.info("Commands synced successfully!")
    
    async def on_ready(self):
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logger.info(f'Connected to {len(self.guilds)} guilds')
        logger.info(f'Available playlists: {", ".join(self.playlist_manager.get_playlists())}')
        logger.info('Bot is ready!')
        
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="music from playlists"
            )
        )
    
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if member.id == self.user.id:
            return
        
        voice_client = member.guild.voice_client
        if voice_client and voice_client.channel:
            members = [m for m in voice_client.channel.members if not m.bot]
            
            if len(members) == 0:
                await asyncio.sleep(300)
                
                if voice_client.is_connected():
                    members = [m for m in voice_client.channel.members if not m.bot]
                    if len(members) == 0:
                        logger.info(f"Disconnecting from {member.guild.name} - no users in voice channel")
                        
                        if member.guild.id in self.players:
                            self.players[member.guild.id].stop()
                        await voice_client.disconnect()


async def main():
    logger.info("Starting Discord Music Bot...")
    logger.info(f"Playlists directory: {config.PLAYLISTS_DIR}")
    
    bot = MusicBot()
    
    try:
        await bot.start(config.DISCORD_TOKEN)
    except KeyboardInterrupt:
        logger.info("Shutting down bot...")
        await bot.close()
    except Exception as e:
        logger.error(f"Error running bot: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(main())
