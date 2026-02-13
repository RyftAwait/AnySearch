import discord
from discord import app_commands
from discord.ext import commands

import json; data = json.load(open('config.json', 'r'))
import logging
import DiscordUtils

import modules.credits as creditManager
import modules.invites as invitesManager
import modules.log as log; logger = log.setup('invites', level=logging.ERROR)
from datetime import datetime


class invites(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.tracker = DiscordUtils.InviteTracker(bot)


    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        inviter:discord.Member = await self.tracker.fetch_inviter(member) # type: ignore
        
        if inviter:
            amount = creditManager.get(inviter.id)
            creditManager.set(inviter.id, amount+data['creditsPerInvite'])

            invitesManager.set(member.id, inviter.id)

            embed = discord.Embed(description=f"### Merci d'avoir invité <@{member.id}>. Vous avez reçu {data['creditsPerInvite']} crédits.", colour=0xffffff)
            await inviter.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_remove(self, member:discord.Member):
        inviter = invitesManager.get(member.id)

        if inviter:
            amount = creditManager.get(inviter)
            creditManager.set(inviter, amount-data['creditsPerInvite'])

            invitesManager.delete(member.id)

            embed = discord.Embed(description=f"### <@{member.id}> a quitté. Vous avez perdu {data['creditsPerInvite']} crédits.", colour=0xffffff)
            await self.bot.get_user(inviter).send(embed=embed) # type: ignore


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        invites(bot)
    )