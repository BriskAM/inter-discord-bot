import discord
from discord import app_commands
from typing import Dict
from music import MusicPlayer, PlaylistManager


async def setup_play_command(tree: app_commands.CommandTree, players: Dict[int, MusicPlayer], playlist_manager: PlaylistManager):
    @tree.command(name="play", description="Start playing music from the current playlist")
    async def play(interaction: discord.Interaction):
        if not interaction.user.voice:
            await interaction.response.send_message(
                "You need to be in a voice channel to use this command!",
                ephemeral=True
            )
            return
        
        guild_id = interaction.guild_id
        if guild_id not in players:
            players[guild_id] = MusicPlayer(guild_id)
        
        player = players[guild_id]
        
        current_playlist = playlist_manager.get_current_playlist()
        if not current_playlist:
            await interaction.response.send_message(
                "No playlist available! Please create a playlist folder first.",
                ephemeral=True
            )
            return
        
        voice_client = interaction.guild.voice_client
        if not voice_client:
            try:
                voice_client = await interaction.user.voice.channel.connect()
            except Exception as e:
                await interaction.response.send_message(
                    f"Failed to connect to voice channel: {str(e)}",
                    ephemeral=True
                )
                return
        
        if not player.queue and not player.is_playing:
            tracks = playlist_manager.get_tracks()
            if not tracks:
                await interaction.response.send_message(
                    f"No tracks found in playlist '{current_playlist}'!",
                    ephemeral=True
                )
                return
            player.add_tracks(tracks)
        
        await interaction.response.defer()
        started = await player.start_playback(voice_client)
        
        if started:
            track_name = player.current_track.stem if player.current_track else "Unknown"
            embed = discord.Embed(
                title="Now Playing",
                description=f"**{track_name}**",
                color=discord.Color.green()
            )
            embed.add_field(name="Playlist", value=current_playlist, inline=True)
            embed.add_field(name="Queue", value=f"{len(player.queue)} tracks", inline=True)
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("Already playing or queue is empty!")
