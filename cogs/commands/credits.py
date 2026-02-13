import discord
import random
import asyncio
import time
from discord.ext import commands
from discord import app_commands

import json; data = json.load(open('config.json', 'r'))
import logging

import modules.credits as creditManager
import modules.log as log; logger = log.setup('credits', level=logging.ERROR)


class creditsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.cooldowns = {}

    
    group = app_commands.Group(name='credits', description='...')


    @app_commands.command(name='mycredits', description='Voir ses crédits')
    async def credits(self, interaction: discord.Interaction):
        userID = interaction.user.id
        amount = creditManager.get(userID)
        embed = discord.Embed(description=f'### Vous avez {amount} crédit(s)', colour=0xffffff)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    

    
    @app_commands.checks.has_permissions(administrator=True)

    @app_commands.describe(user='Utilisateur', credits='Quantité de crédits')

    @group.command(name="add", description='Ajouter des crédits')
    async def add(self, interaction: discord.Interaction, user:discord.User, credits: int):
        userID = user.id
        amount = creditManager.get(userID)
        creditManager.set(userID, amount+credits)
        embed = discord.Embed(description=f'### <@{userID}> a maintenant {amount+credits} crédit(s)', colour=0xffffff)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @add.error
    async def add_error(
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

    

    @app_commands.checks.has_permissions(administrator=True)

    @app_commands.describe(user='Utilisateur', credits='Quantité de crédits')

    @group.command(name="remove", description='Retirer des crédits')
    async def remove(self, interaction: discord.Interaction, user:discord.User, credits: int):
        userID = user.id
        amount = creditManager.get(userID)
        creditManager.set(userID, amount-credits)
        embed = discord.Embed(description=f'### <@{userID}> a maintenant {amount-credits} crédit(s)', colour=0xffffff)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @remove.error
    async def remove_error(
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
    


    @app_commands.checks.has_permissions(administrator=True)

    @app_commands.describe(user='Utilisateur', credits='Quantité de crédits')

    @group.command(name="set", description='Assigner une quantité de crédits')
    async def set(self, interaction: discord.Interaction, user:discord.User, credits: int):
        userID = user.id
        creditManager.set(userID, credits)
        embed = discord.Embed(description=f'### <@{userID}> a maintenant {credits} crédit(s)', colour=0xffffff)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @set.error
    async def set_error(
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
    


    @app_commands.checks.has_permissions(administrator=True)

    @app_commands.describe(user='Utilisateur')

    @group.command(name="see", description='Voir les crédits d\'un utilisateur')
    async def see(self, interaction: discord.Interaction, user:discord.User):
        userID = user.id
        amount = creditManager.get(userID)
        embed = discord.Embed(description=f'### <@{userID}> a {amount} crédit(s)', colour=0xffffff)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @see.error
    async def see_error(
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
    await bot.add_cog(creditsCog(bot))