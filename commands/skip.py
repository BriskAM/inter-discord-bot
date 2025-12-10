import discord
from discord import app_commands
from typing import Dict
from music import MusicPlayer


async def setup_skip_command(tree: app_commands.CommandTree, players: Dict[int, MusicPlayer]):
    @tree.command(name="skip", description="Skip the current track")
    async def skip(interaction: discord.Interaction):
        guild_id = interaction.guild_id
        
        if guild_id not in players:
            await interaction.response.send_message(
                "Nothing is playing!",
                ephemeral=True
            )
            return
        
        player = players[guild_id]
        
        if player.skip():
            next_track = player.queue[0].stem if player.queue else "End of queue"
            await interaction.response.send_message(f"Skipped! Next: **{next_track}**")
        else:
            await interaction.response.send_message(
                "Nothing is playing!",
                ephemeral=True
            )
