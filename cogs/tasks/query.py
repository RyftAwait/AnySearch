from discord.ext import tasks, commands

import json; creditsData = json.load(open('config.json', 'r'))['creditsData']

from modules.mcquery import mcquery as queryManager


class query(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    
    @tasks.loop(minutes=1)
    async def save(self):
        try:
            await queryManager.save()
        except: pass

    
    @commands.Cog.listener()
    async def on_ready(self):
        query(self.bot).save.start()


async def setup(bot: commands.Bot) -> None:
    if bot.is_ready():
        query(bot).save.start()
    else:
        await bot.add_cog(
            query(bot)
        )