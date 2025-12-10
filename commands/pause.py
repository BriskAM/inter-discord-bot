import discord
from discord import app_commands
from typing import Dict
from music import MusicPlayer


async def setup_pause_command(tree: app_commands.CommandTree, players: Dict[int, MusicPlayer]):
    @tree.command(name="pause", description="Pause the current track")
    async def pause(interaction: discord.Interaction):
        guild_id = interaction.guild_id
        
        if guild_id not in players:
            await interaction.response.send_message(
                "Nothing is playing!",
                ephemeral=True
            )
            return
        
        player = players[guild_id]
        
        if player.pause():
            await interaction.response.send_message("Paused playback.")
        else:
            await interaction.response.send_message(
                "Nothing is playing!",
                ephemeral=True
            )
