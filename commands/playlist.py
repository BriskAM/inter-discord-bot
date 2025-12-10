import discord
from discord import app_commands
from typing import Dict
from music import MusicPlayer, PlaylistManager


async def setup_playlist_command(tree: app_commands.CommandTree, players: Dict[int, MusicPlayer], playlist_manager: PlaylistManager):
    playlist_group = app_commands.Group(name="playlist", description="Playlist management commands")
    
    @playlist_group.command(name="list", description="Show available playlists")
    async def playlist_list(interaction: discord.Interaction):
        playlists = playlist_manager.get_playlists()
        current = playlist_manager.get_current_playlist()
        
        if not playlists:
            await interaction.response.send_message(
                "No playlists found! Create a folder in the playlists directory.",
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title="Available Playlists",
            color=discord.Color.purple()
        )
        
        playlists_text = "\n".join([
            f"{'> ' if p == current else '  '} **{p}**"
            for p in playlists
        ])
        
        embed.description = playlists_text
        embed.set_footer(text=f"Current: {current or 'None'}")
        
        await interaction.response.send_message(embed=embed)
    
    @playlist_group.command(name="switch", description="Switch to a different playlist")
    @app_commands.describe(name="Name of the playlist to switch to")
    async def playlist_switch(interaction: discord.Interaction, name: str):
        if playlist_manager.switch_playlist(name):
            guild_id = interaction.guild_id
            if guild_id in players:
                players[guild_id].clear_queue()
            
            await interaction.response.send_message(
                f"Switched to playlist: **{name}**\n"
                f"Use `/play` to start playing from this playlist."
            )
        else:
            available = ", ".join(playlist_manager.get_playlists())
            await interaction.response.send_message(
                f"Playlist '{name}' not found!\n"
                f"Available playlists: {available}",
                ephemeral=True
            )
    
    @playlist_group.command(name="current", description="Show the current playlist")
    async def playlist_current(interaction: discord.Interaction):
        current = playlist_manager.get_current_playlist()
        
        if current:
            tracks = playlist_manager.get_tracks()
            embed = discord.Embed(
                title="Current Playlist",
                description=f"**{current}**",
                color=discord.Color.purple()
            )
            embed.add_field(name="Tracks", value=str(len(tracks)), inline=True)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(
                "No playlist selected!",
                ephemeral=True
            )
    
    tree.add_command(playlist_group)
