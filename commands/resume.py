import discord
from discord import app_commands
from typing import Dict
from music import MusicPlayer


async def setup_resume_command(tree: app_commands.CommandTree, players: Dict[int, MusicPlayer]):
    @tree.command(name="resume", description="Resume paused playback")
    async def resume(interaction: discord.Interaction):
        guild_id = interaction.guild_id
        
        if guild_id not in players:
            await interaction.response.send_message(
                "Nothing is paused!",
                ephemeral=True
            )
            return
        
        player = players[guild_id]
        
        if player.resume():
            await interaction.response.send_message("Resumed playback.")
        else:
            await interaction.response.send_message(
                "Nothing is paused!",
                ephemeral=True
            )
