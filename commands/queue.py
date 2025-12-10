import discord
from discord import app_commands
from typing import Dict
from music import MusicPlayer


async def setup_queue_command(tree: app_commands.CommandTree, players: Dict[int, MusicPlayer]):
    @tree.command(name="queue", description="Show the current music queue")
    async def queue(interaction: discord.Interaction):
        guild_id = interaction.guild_id
        
        if guild_id not in players:
            await interaction.response.send_message(
                "No music player active!",
                ephemeral=True
            )
            return
        
        player = players[guild_id]
        
        embed = discord.Embed(
            title="Music Queue",
            color=discord.Color.blue()
        )
        
        if player.current_track:
            status = "Paused" if player.is_paused else "Playing"
            embed.add_field(
                name="Now Playing",
                value=f"{status} **{player.current_track.stem}**",
                inline=False
            )
        else:
            embed.add_field(name="Now Playing", value="Nothing", inline=False)
        
        queue_list = player.get_queue_list()
        if queue_list:
            tracks_display = "\n".join([
                f"{i+1}. {track.stem}"
                for i, track in enumerate(queue_list[:10])
            ])
            if len(queue_list) > 10:
                tracks_display += f"\n... and {len(queue_list) - 10} more"
            
            embed.add_field(
                name=f"Up Next ({len(queue_list)} tracks)",
                value=tracks_display,
                inline=False
            )
        else:
            embed.add_field(name="Up Next", value="Queue is empty", inline=False)
        
        await interaction.response.send_message(embed=embed)
