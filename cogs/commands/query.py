import discord
from discord import app_commands
from discord.ext import commands

import logging
import json; data = json.load(open('config.json', 'r'))

import modules.credits as creditManager
from modules.mcquery import mcquery as queryManager
import modules.log as log; logger = log.setup('last', level=logging.ERROR)

class queryCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    
    group = app_commands.Group(name="query", description="...")
    
    @app_commands.describe(username='Nom du joueur')
    
    @creditManager.has_enough_credits(1)
    
    @group.command(name="find", description="Chercher un joueur sur les serveurs disponibles")
    async def find(
        self,
        interaction: discord.Interaction,
        username:str
    ) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)
        
        server:str = await queryManager.findPlayer(username)
        
        if server:
            embed = discord.Embed(description=f'### Ce joueur est connecté à `{server.replace("_", " ")}`', colour=0x2d2d31)
        else:
            embed = discord.Embed(description=f'### Ce joueur n\'est pas connecté', colour=0x2d2d31)
        
        userID = interaction.user.id
        amount = creditManager.get(userID)
        creditManager.set(userID, amount-1)
        
        await interaction.followup.send(embed=embed)
    
    @find.error
    async def find_error(
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
        queryCommand(bot)
    )
