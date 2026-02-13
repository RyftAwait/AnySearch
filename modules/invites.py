import sqlite3

from discord.app_commands.commands import check
from discord.app_commands import CheckFailure
from discord import Interaction
from typing import TypeVar, Callable


conn = sqlite3.connect('data/data.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS invites (
        user INT,
        inviter INT
    )
''')
conn.commit()
conn.close()


def get(user):
    conn = sqlite3.connect('data/data.db')
    c = conn.cursor()
    try:
        c.execute("SELECT inviter FROM invites WHERE user = ?;", (user,))
        result = c.fetchone()
        if result:
            return result[0]
        else:
            return None
    finally:
        conn.close()


def set(user, inviter):
    conn = sqlite3.connect('data/data.db')
    c = conn.cursor()
    try:
        c.execute("UPDATE invites SET inviter = ? WHERE user = ?;", (inviter, user,))
        if c.rowcount == 0:
            raise ValueError("User does not exist in the database.")
        return True
    except:
        c.execute("INSERT INTO invites (user, inviter) VALUES (?, ?);", (user, inviter,))
        return False
    finally:
        conn.commit()
        conn.close()

        
def delete(user):
    conn = sqlite3.connect('data/data.db')
    c = conn.cursor()
    try:
        c.execute("DELETE FROM invites WHERE user = ?;", (user,))
        if c.rowcount == 0:
            raise ValueError("User does not exist in the database.")
        return True
    except:
        return False
    finally:
        conn.commit()
        conn.close()