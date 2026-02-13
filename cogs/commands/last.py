import discord
from discord import app_commands
from discord.ext import commands

import time
import logging
import typing
import json; data = json.load(open('config.json', 'r'))

import modules.credits as creditManager
from modules.mcquery import mcquery as queryManager
import modules.log as log; logger = log.setup('last', level=logging.ERROR)

class last(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.elements = json.load(open('data/serverList.json', 'r')).keys()
    
    
    group = app_commands.Group(name="last", description="...")
    
    
    @app_commands.describe(server='Serveur', username='Nom du joueur')
    
    @creditManager.has_enough_credits(1)
    
    @group.command(name="connect", description="Obtenir la date de dernière connexion d'un joueur")
    async def lastConnect(
        self,
        interaction: discord.Interaction,
        server:str,
        username:str
    ) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)
        
        timestamp:int = await queryManager.getTimestampFromPlayer(server, username)
        
        if timestamp is None:
            embed = discord.Embed(description=f'### Ce joueur ne s\'est pas connecté au serveur', colour=0x2d2d31)
        elif timestamp == 'error':
            embed = discord.Embed(description=f'### Serveur introuvable', colour=0x2d2d31)
        else:
            embed = discord.Embed(description=f'### Ce joueur s\'est connecté pour la dernière fois le <t:{timestamp}:f>', colour=0x2d2d31)
        
        userID = interaction.user.id
        amount = creditManager.get(userID)
        creditManager.set(userID, amount-1)
        
        await interaction.followup.send(embed=embed)
    
    @lastConnect.autocomplete('server')
    async def lastConnect_autocomplete(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        data = []
        for element in self.elements:
            if current.lower() in element.lower().replace('_', ' '):
                data.append(app_commands.Choice(name=element.replace('_', ' '), value=element))
                if len(data) > 15:
                    return data

        return data
    
    @lastConnect.error
    async def lastConnect_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.errors.AppCommandError
    ):
        if isinstance(error, creditManager.MissingCredits):
            embed = discord.Embed(description=f'### Vous n\'avez pas suffisamment de crédits.', colour=0x2d2d31)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            logger.error('\033[38;2;255;0;0m' + str(error))
            embed = discord.Embed(description=f'### {str(error)}', colour=0x2d2d31)
            await interaction.followup.send(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        last(bot)
    )
