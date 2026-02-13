import discord
from discord.ext import commands
from discord import app_commands

import json; data = json.load(open('config.json', 'r'))
import logging
import typing

import modules.log as log; logger = log.setup('backup', level=logging.ERROR)


class backupCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.elements = json.loads(open('data/backups.json', 'r', encoding='UTF-8').read())
    
    
    @app_commands.command(name="backup")
    async def backup(self, interaction: discord.Interaction, nom: str):
        self.elements[nom]
        await interaction.response.send_message(self.elements[nom], ephemeral=True)

    
    @backup.autocomplete('nom')
    async def backup_autocomplete(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        data = []
        for element in self.elements:
            if current.lower() in element.lower():
                data.append(app_commands.Choice(name=element, value=element))
                if len(data) > 15:
                    return data

        return data
    
    @backup.error
    async def backup_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.errors.AppCommandError
    ):
        if isinstance(error, app_commands.MissingPermissions):
            embed = discord.Embed(description=f'### Vous n\'avez pas la permission d\'exécuter cette commande.', colour=0x2d2d31)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description=f'### {str(error)}.', colour=0x2d2d31)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            logger.error('\033[38;2;255;0;0m' + str(error))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(backupCog(bot))