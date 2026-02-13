from discord.app_commands.commands import check
from discord.app_commands import CheckFailure
from discord import Interaction
from typing import TypeVar, Callable


class NotWhitelisted(CheckFailure):
    def __init__(self) -> None:
        message = f'Utilisateur non autorisé à exécuter cette commande.'
        super().__init__(message)


T = TypeVar('T')

def is_whitelisted(*whitelisted_users: int) -> Callable[[T], T]:

    def predicate(interaction: Interaction) -> bool:

        if interaction.user.id in whitelisted_users:
            return True    
        
        raise NotWhitelisted()

    return check(predicate)
