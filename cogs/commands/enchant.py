import discord
from discord import app_commands
from discord.ext import commands

import json; data = json.load(open('config.json', 'r'))
import logging

import modules.log as log; logger = log.setup('backup', level=logging.ERROR)

class enchant(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.letters = {
            '.': '._.',
            'a': 'ᔑ',
            'b': 'ʖ',
            'c': 'ᓵ',
            'd': '↸',
            'e': 'ᒷ',
            'f': '⎓',
            'g': '⊣',
            'h': '⍑',
            'im': '╎',
            'j': '⋮',
            'k': 'ꖌ',
            'l': 'ꖎ',
            'm': 'ᒲ',
            'n': 'リ',
            'o': '𝙹',
            'p': '!¡',
            'q': 'ᑑ',
            'r': '∷',
            's': 'ᓭ',
            't': 'ℸ',
            'u': '⚍',
            'v': '⍊',
            'w': '∴',
            'x': '̇/',
            'y': '||',
            'z': '⨅'
        }
    
    
    @app_commands.command(name="enchant", description="Traduire un message en Standard Galactic Alphabet (Minecraft)")
    async def enchant(
        self,
        interaction: discord.Interaction,
        message: str
    ) -> None:
        await interaction.response.defer(ephemeral=True, thinking=True)

        for letter in self.letters:
            message = message.replace(letter, self.letters[letter])
        
        embed = discord.Embed(colour=0x2d2d31, description=f'## {message}\n\u200b') # type: ignore
        
        await interaction.followup.send(embed=embed)
        
    @enchant.error
    async def enchant_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.errors.AppCommandError
    ):
        embed = discord.Embed(description=f'### {str(error)}.', colour=0x2d2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.error('\033[38;2;255;0;0m' + str(error))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        enchant(bot)
    )
