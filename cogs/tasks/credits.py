import discord
from discord.ext import tasks, commands

import json; creditsData = json.load(open('config.json', 'r'))['creditsData']

import modules.credits as creditManager


class credits(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.guild = 1158056896549371934

    
    @tasks.loop(hours=12)
    async def addCredit(self):
        for member in self.bot.get_guild(self.guild).members: # type: ignore
            
            for role in creditsData:
                if role == 'default':
                    break
            
                if discord.utils.get(member.roles, id=int(role)):
                    userID = member.id
                    amount = creditManager.get(userID)
                    creditManager.set(userID, amount+creditsData[role])
                    break

    
    @commands.Cog.listener()
    async def on_ready(self):
        credits(self.bot).addCredit.start()


async def setup(bot: commands.Bot) -> None:
    if bot.is_ready():
        credits(bot).addCredit.start()
    else:
        await bot.add_cog(
            credits(bot)
        )