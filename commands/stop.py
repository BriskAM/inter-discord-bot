import discord
from discord import app_commands
from typing import Dict
from music import MusicPlayer


async def setup_stop_command(tree: app_commands.CommandTree, players: Dict[int, MusicPlayer]):
    @tree.command(name="stop", description="Stop playing music and disconnect from voice channel")
    async def stop(interaction: discord.Interaction):
        guild_id = interaction.guild_id
        
        if guild_id not in players:
            await interaction.response.send_message(
                "Nothing is playing!",
                ephemeral=True
            )
            return
        
        player = players[guild_id]
        voice_client = interaction.guild.voice_client
        
        player.stop()
        
        if voice_client:
            await voice_client.disconnect()
        
        await interaction.response.send_message("Stopped playback and disconnected.")
