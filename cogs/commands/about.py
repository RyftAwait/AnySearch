import discord
from discord import app_commands
from discord.ext import commands

import time
import json; data = json.load(open('config.json', 'r'))


class about(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.start = round(time.time())
    
    
    @app_commands.command(name="about", description="About the bot")
    async def about(
        self,
        interaction: discord.Interaction
    ) -> None:
        await interaction.response.defer(thinking=True)

        embed = discord.Embed(colour=0x2d2d31, description=f'## {self.bot.user.display_name}\n\u200b') # type: ignore

        timestamp = round(time.time())
        elapsed_time = timestamp - self.start
        elapsed_days = elapsed_time // (24 * 3600)
        elapsed_time %= (24 * 3600)
        elapsed_hours = elapsed_time // 3600
        elapsed_time %= 3600
        elapsed_minutes = elapsed_time // 60
        elapsed_seconds = elapsed_time % 60
        elapsed_time_str = f"{int(elapsed_days)}d {int(elapsed_hours)}h {int(elapsed_minutes)}m {int(elapsed_seconds)}s"
        embed.add_field(name=f'Bot lancé depuis', value=f'`{elapsed_time_str}`', inline=True)
        
        count = 0
        async for _ in self.bot.get_channel(1158056897493073994).history(limit=None): # type: ignore
            count += 1
        embed.add_field(name=f'Recherches effectuées', value=f'`{count}` recherches', inline=True)

        count = 0
        async for _ in self.bot.get_channel(1162116458252345467).history(limit=None): # type: ignore
            count += 1
        embed.add_field(name=f'Lookup effectuées', value=f'`{count}` lookup', inline=True)
        
        embed.add_field(name=f'Version', value=f'`{data["version"]}`', inline=True)
        
        await interaction.followup.send(embed=embed)
        
    @about.error
    async def about_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.errors.AppCommandError
    ):
        print(f'\033[38;2;255;0;0m{error}')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        about(bot)
    )
