import discord
from discord.ext import commands
from discord import app_commands

import json; data = json.load(open('config.json', 'r'))
import logging
import re

import modules.hideIP as hideIP
import modules.log as log; logger = log.setup('hideMyIP', level=logging.ERROR)


class hideMyIPCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    hideGroup = app_commands.Group(name='hide', description='...')
    group = app_commands.Group(name='my', description='...', parent=hideGroup)


    @app_commands.checks.has_any_role(*data['hideMyIP'])

    @group.command(name="ip")
    async def hideMyIP(self, interaction: discord.Interaction, ip: str):
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",ip):
            hideIP.set(interaction.user.id, ip)
            embed = discord.Embed(description=f'### L\'ip ||{ip}|| a été masquée avec succès', colour=0xffffff)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        embed = discord.Embed(description=f'### Format de l\'ip invalide.', colour=0x2d2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    
    @hideMyIP.error
    async def hideMyIP_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.errors.AppCommandError
    ):
        if isinstance(error, app_commands.MissingAnyRole):
            embed = discord.Embed(description=f'### Vous n\'avez pas la permission d\'exécuter cette commande.', colour=0x2d2d31)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description=f'### {str(error)}.', colour=0x2d2d31)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            logger.error('\033[38;2;255;0;0m' + str(error))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(hideMyIPCog(bot))