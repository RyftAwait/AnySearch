import discord
from discord.ext import commands
from discord import app_commands

import json; data = json.load(open('config.json', 'r'))
import logging
import os

from modules.obfuscate import message as obfuscateMessage
import modules.log as log; logger = log.setup('obfuscate', level=logging.ERROR)


class obfuscateCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    
    @app_commands.command(name="obfuscate", description="Obfuscer un message")
    async def obfuscate(self, interaction: discord.Interaction, message: str):
        await interaction.response.defer(thinking=True, ephemeral=True)
        
        fileName = obfuscateMessage(message)
        await interaction.followup.send(file=discord.File(f'temp/{fileName}.txt'), ephemeral=True)
        
        os.remove(f'temp/{fileName}.txt')
    
    @obfuscate.error
    async def obfuscate_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.errors.AppCommandError
    ):
        if isinstance(error, app_commands.MissingPermissions):
            embed = discord.Embed(description=f'### Vous n\'avez pas la permission d\'exécuter cette commande.', colour=0x2d2d31)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description=f'### {str(error)}.', colour=0x2d2d31)
            await interaction.followup.send(embed=embed)
            logger.error('\033[38;2;255;0;0m' + str(error))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(obfuscateCog(bot))