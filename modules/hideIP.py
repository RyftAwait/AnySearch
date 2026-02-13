import sqlite3


conn = sqlite3.connect('data/data.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS hideIP (
        user INT,
        ip STRING
    )
''')
conn.commit()
conn.close()


def getAll():
    conn = sqlite3.connect('data/data.db')
    c = conn.cursor()
    try:
        c.execute("SELECT ip FROM hideIP")
        ips = [value[0] for value in c.fetchall()]
        if len(ips) > 0:
            return ips
        else:
            return []
    finally:
        conn.close()


def get(user):
    conn = sqlite3.connect('data/data.db')
    c = conn.cursor()
    try:
        c.execute("SELECT amount FROM hideIP WHERE user = ?;", (user,))
        result = c.fetchone()
        if result:
            return result[0]
        else:
            return None
    finally:
        conn.close()


def set(user, ip):
    conn = sqlite3.connect('data/data.db')
    c = conn.cursor()
    try:
        c.execute("UPDATE hideIP SET ip = ? WHERE user = ?;", (ip, user,))
        if c.rowcount == 0:
            raise ValueError("User does not exist in the database.")
        return True
    except:
        c.execute("INSERT INTO hideIP (user, ip) VALUES (?, ?);", (user, ip,))
        return False
    finally:
        conn.commit()
        conn.close()

        
def delete(user):
    conn = sqlite3.connect('data/data.db')
    c = conn.cursor()
    try:
        c.execute("DELETE FROM hideIP WHERE user = ?;", (user,))
        if c.rowcount == 0:
            raise ValueError("User does not exist in the database.")
        return True
    except:
        return False
    finally:
        conn.commit()
        conn.close()