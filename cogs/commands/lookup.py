import discord
from discord.ext import commands
from discord import app_commands

import json; data = json.load(open('config.json', 'r'))
import time
import asyncio
import logging
import requests

import modules.credits as creditManager
import modules.log as log; logger = log.setup('lookup', level=logging.ERROR)


class Lookup(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.cooldown = {}

    def look(self, ip):
        data = json.loads(requests.request("GET", f"https://api.ipregistry.co/{ip}?key=eox72cn13nraqqzx").text)
        
        if data["security"]["is_vpn"]:
            vpn = 'Oui'
        else:
            vpn = 'Non'
    
        if data["security"]["is_proxy"]:
            proxy = 'Oui'
        else:
            proxy = 'Non'
    
        return discord.Embed(description=f'''\
## INFORMATIONS
### IP
{data["ip"]}
### TYPE
{data["type"]}
\u200b
## LOCALISATION
### CONTINENT
{data["location"]["continent"]["name"]}
### PAYS
{data["location"]["country"]["name"]}
### REGION
{data["location"]["region"]["name"]}
### VILLE
{data["location"]["city"]}
\u200b
## AUTRES
### VPN ?
{vpn}
### PROXY ?
{proxy}
''', colour=0xffffff)

    def getCooldown(self, cooldownData, userRoles):
        for role in cooldownData:
            if role == 'default':
                return cooldownData['default']
            
            if discord.utils.get(userRoles, id=int(role)):
                return cooldownData[role]
    
    
    @creditManager.has_enough_credits(1)

    @app_commands.command(name="lookup", description="Récupérer les informations d'une IP.")
    async def lookup(self, interaction: discord.Interaction, ip: str):
        if interaction.user.id in self.cooldown:
            timeCooldown = self.getCooldown(data['lookup']['cooldown'], interaction.user.roles) # type: ignore
            cooldown = timeCooldown - round(time.time() - self.cooldown[interaction.user.id], 1)
            
            if cooldown < 0:
                embed = discord.Embed(description=f'### S\'il vous plaît, veuillez attendre que la commande antérieure soit terminée.', colour=0x2d2d31)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            embed = discord.Embed(description=f'### S\'il vous plaît, veuillez attendre `{cooldown}`s avant de refaire cette commande.', colour=0x2d2d31)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        self.cooldown[interaction.user.id] = time.time()
        
        await interaction.response.defer(ephemeral=True, thinking=True)
        

        result = self.look(ip)
        await interaction.followup.send(embed=result)

        
        timeCooldown = self.getCooldown(data['lookup']['cooldown'], interaction.user.roles) # type: ignore
        cooldown = timeCooldown - round(time.time() - self.cooldown[interaction.user.id], 1)
        
        userID = interaction.user.id
        amount = creditManager.get(userID)
        creditManager.set(userID, amount-1)

        if cooldown < 0:
            return
        
        await asyncio.sleep(cooldown)
        self.cooldown.pop(interaction.user.id, None)
    
    @lookup.error
    async def lookup_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.errors.AppCommandError
    ):
        if isinstance(error, app_commands.MissingAnyRole):
            embed = discord.Embed(description=f'### Vous n\'avez pas la permission d\'exécuter cette commande.', colour=0x2d2d31)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            self.cooldown.pop(interaction.user.id, None)
            logger.error('\033[38;2;255;0;0m' + str(error))
            embed = discord.Embed(description=f'### {str(error)}', colour=0x2d2d31)
            await interaction.followup.send(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Lookup(bot))