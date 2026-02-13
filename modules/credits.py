import sqlite3

from discord.app_commands.commands import check
from discord.app_commands import CheckFailure
from discord import Interaction
from typing import TypeVar, Callable


conn = sqlite3.connect('data/data.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS credits (
        user INT,
        amount INT
    )
''')
conn.commit()
conn.close()


def getAll():
    conn = sqlite3.connect('data/data.db')
    c = conn.cursor()
    try:
        c.execute("SELECT amount FROM credits")
        credits = [value[0] for value in c.fetchall()]
        if len(credits) > 0:
            return sum(credits)
        else:
            return 0
    finally:
        conn.close()

def get(user):
    conn = sqlite3.connect('data/data.db')
    c = conn.cursor()
    try:
        c.execute("SELECT amount FROM credits WHERE user = ?;", (user,))
        result = c.fetchone()
        if result:
            return result[0]
        else:
            return 0
    finally:
        conn.close()


def set(user, amount):
    conn = sqlite3.connect('data/data.db')
    c = conn.cursor()
    try:
        c.execute("UPDATE credits SET amount = ? WHERE user = ?;", (amount, user,))
        if c.rowcount == 0:
            raise ValueError("User does not exist in the database.")
        return True
    except:
        c.execute("INSERT INTO credits (user, amount) VALUES (?, ?);", (user, amount,))
        return False
    finally:
        conn.commit()
        conn.close()

        
def delete(user):
    conn = sqlite3.connect('data/data.db')
    c = conn.cursor()
    try:
        c.execute("DELETE FROM credits WHERE user = ?;", (user,))
        if c.rowcount == 0:
            raise ValueError("User does not exist in the database.")
        return True
    except:
        return False
    finally:
        conn.commit()
        conn.close()


class MissingCredits(CheckFailure):
    def __init__(self) -> None:
        message = f'Crédits insuffisants'
        super().__init__(message)


T = TypeVar('T')

def has_enough_credits(credits: int) -> Callable[[T], T]:

    def predicate(interaction: Interaction) -> bool:

        if get(interaction.user.id) >= credits:
            return True    
        
        raise MissingCredits()

    return check(predicate)