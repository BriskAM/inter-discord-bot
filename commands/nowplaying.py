import discord
from discord import app_commands
from typing import Dict
from music import MusicPlayer, PlaylistManager


async def setup_nowplaying_command(tree: app_commands.CommandTree, players: Dict[int, MusicPlayer], playlist_manager: PlaylistManager):
    @tree.command(name="nowplaying", description="Show information about the current track")
    async def nowplaying(interaction: discord.Interaction):
        guild_id = interaction.guild_id
        
        if guild_id not in players:
            await interaction.response.send_message(
                "No music player active!",
                ephemeral=True
            )
            return
        
        player = players[guild_id]
        
        if not player.current_track:
            await interaction.response.send_message(
                "Nothing is playing!",
                ephemeral=True
            )
            return
        
        status = "Paused" if player.is_paused else "Playing"
        current_playlist = playlist_manager.get_current_playlist()
        
        embed = discord.Embed(
            title="Now Playing",
            description=f"**{player.current_track.stem}**",
            color=discord.Color.green()
        )
        embed.add_field(name="Status", value=status, inline=True)
        embed.add_field(name="Playlist", value=current_playlist or "Unknown", inline=True)
        embed.add_field(name="Volume", value=f"{int(player.volume * 100)}%", inline=True)
        embed.add_field(name="Tracks in Queue", value=str(len(player.queue)), inline=True)
        
        await interaction.response.send_message(embed=embed)
