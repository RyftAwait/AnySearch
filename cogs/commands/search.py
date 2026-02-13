import discord
from discord.ext import commands
from discord import app_commands

import json; data = json.load(open('config.json', 'r'))
import os
import time
import re
import aiofiles
import asyncio
import logging

import modules.hideIP as hideIP
import modules.credits as creditManager
import modules.log as log; logger = log.setup('search', level=logging.ERROR)


class Search(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.cooldown = {}

    
    def getCooldown(self, cooldownData, userRoles):
        for role in cooldownData:
            if role == 'default':
                return cooldownData['default']
            
            if discord.utils.get(userRoles, id=int(role)):
                return cooldownData[role]
    
    async def searchFile(file_path, keyword): # type: ignore
        matching_lines = []
        try:
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            async with aiofiles.open(file_path, 'r', encoding='latin-1') as f: # type: ignore
                for line_number, line in enumerate(await f.readlines()):
                    if pattern.search(line):
                        matching_lines.append((line.replace('\n', ''), line_number + 1))
            return matching_lines
        except UnicodeDecodeError:
            logger.error(f"\033[38;2;255;0;0mErreur d'encodage: {file_path}")
            return []
    
    
    @app_commands.choices(
        directory = [
            app_commands.Choice(name='MCBE', value='DB/MCBE'),
            app_commands.Choice(name='MC Java', value='DB/Java'),
            app_commands.Choice(name='FiveM', value='DB/FiveM')
        ]
    )
    
    
    @creditManager.has_enough_credits(2)
    
    @app_commands.describe(keyword='mot-clé', directory='Dossier spécifique')
    
    @app_commands.command(name="search", description="Chercher dans les bases de données.")
    async def searcher(self, interaction: discord.Interaction, directory: str, keyword: str):
        if interaction.user.id in self.cooldown:
            timeCooldown = self.getCooldown(data['search']['cooldown'], interaction.user.roles) # type: ignore
            cooldown = timeCooldown - round(time.time() - self.cooldown[interaction.user.id], 1)
            
            if cooldown < 0:
                embed = discord.Embed(description=f'### S\'il vous plaît, veuillez attendre que la commande antérieure soit terminée.', colour=0x2d2d31)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            embed = discord.Embed(description=f'### S\'il vous plaît, veuillez attendre `{cooldown}`s avant de refaire cette commande.', colour=0x2d2d31)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        self.cooldown[interaction.user.id] = time.time()
        
        keyword = keyword.lower()
        start = time.time()
        
        if len(keyword) < data["search"]['limit']:
            embed = discord.Embed(description=f'### Le message doit faire minimum {data["searcher"]["limit"]} caractères.', colour=0x2d2d31)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True, thinking=True)
        
        files = [f'{directory}/{file}' for file in os.listdir(directory)]

        result = f'## Recherche: `{keyword}`\n\u200b\n```'
        for file in files:
            output = await Search.searchFile(file, keyword) # type: ignore
            if len(output) > 0:
                result += f'\n{os.path.basename(file)}\n'
                for element in output:
                    result += f' {element[1]:<4}   {element[0]}\n'

        result = result[:4000] + '```'

        for ip in hideIP.getAll():
            if ip in result:
                result = result.replace(ip, 'xx.xx.xx.xx')

        end = time.time()
        duration = round(end - start, 1)
        
        if result == f'## Recherche: `{keyword}`\n\u200b\n``````':
            embed = discord.Embed(description=f'### Aucun résultat trouvé pour `{keyword}`.', colour=0xffffff)
        else:
            embed = discord.Embed(description=result, colour=0xffffff)
        
        await interaction.followup.send(embed=embed.set_footer(text=f'La recherche a duré {duration}s.'))
        log = interaction.guild.get_channel(1158056897493073994)
        embed3 = discord.Embed(description=f"## <@{interaction.user.id}> a utilisé(e) `/search`\n\u200b\n### Dossier: `{directory}`\n\n### Recherche: `{keyword}`", colour=0xffffff)
        await log.send(embed=embed3)


        timeCooldown = self.getCooldown(data['search']['cooldown'], interaction.user.roles) # type: ignore
        cooldown = timeCooldown - round(time.time() - self.cooldown[interaction.user.id], 1)
        
        userID = interaction.user.id
        amount = creditManager.get(userID)
        creditManager.set(userID, amount-2)

        if cooldown < 0:
            self.cooldown.pop(interaction.user.id, None) 
            return
        
        await asyncio.sleep(cooldown)
        self.cooldown.pop(interaction.user.id, None)
    
    @searcher.error
    async def searcher_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.errors.AppCommandError
    ):
        if isinstance(error, creditManager.MissingCredits):
            embed = discord.Embed(description=f'### Vous n\'avez pas suffisamment de crédits.', colour=0x2d2d31)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            self.cooldown.pop(interaction.user.id, None)
            logger.error('\033[38;2;255;0;0m' + str(error))
            embed = discord.Embed(description=f'### {str(error)}', colour=0x2d2d31)
            await interaction.followup.send(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Search(bot))