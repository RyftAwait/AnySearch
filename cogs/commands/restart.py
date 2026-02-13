import discord
from discord.ext import commands
from discord import app_commands
import subprocess
import sys
import os

class RestartCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="restart", description="redémarre le bot en cas de problème.")
    async def restart(self, interaction):
        if interaction.user.id in [828006097196679218, 1086299223991009280]:
            await interaction.response.send_message('Redémarrage en cours...', ephemeral=True)
            await self.do_restart()
            
        else:
            await interaction.response.send_message('Vous n\'avez pas la permission de redémarrer le bot.', ephemeral=True)

    async def do_restart(self, interaction):
        try:
           
            script_name = sys.argv[0]
            
            
            subprocess.Popen([sys.executable, script_name])
            
            
            await self.bot.close()
            
            sys.exit(0)
        except Exception as e:
            print(f"Erreur lors du redémarrage : {e}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RestartCog(bot))
