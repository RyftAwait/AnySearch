import httpx
import json
import time
import sqlite3

servers:dict = json.loads(open('data/serverList.json', 'r', encoding='UTF-8').read())

conn = sqlite3.connect('data/lastConnect.db')

for key in servers.keys():
    c = conn.cursor()
    c.execute(f'''
        CREATE TABLE IF NOT EXISTS {key} (
            username STRING,
            lastConnection INTEGER
        )
    ''')

conn.commit()
conn.close()

class mcquery:
    async def request(ip:str, port:int=19132):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'https://api.mcsrvstat.us/2/{ip}:{port}', timeout=8)
            data = response.json()
        
            if 'error' in data['debug'] and 'query' in data['debug']['error']:
                return None
            else:
                return data
    
    async def getPlayers(ip:str, port:int=19132):
        data = await mcquery.request(ip, port)
        if data and 'players' in data:
            return data['players'].get('list', [])
        
        return []
    
    async def save():
        timestamp = round(time.time())

        conn = sqlite3.connect('data/lastConnect.db')
        c = conn.cursor()

        for key in servers.keys():
            players = await mcquery.getPlayers(servers[key]['ip'], servers[key]['port'])

            data = [(player, timestamp) for player in players]
            
            if len(data) > 0 : c.executemany(f"""
                INSERT INTO {key} (username, lastConnection) 
                VALUES (?, ?) 
                ON CONFLICT(username) DO UPDATE SET lastConnection=excluded.lastConnection;
            """, data)

        conn.commit()
        conn.close()
    
    async def checkTableExists(dbcon:sqlite3.Connection, server:str):
        dbcur = dbcon.cursor()
        dbcur.execute("""
            SELECT COUNT(*)
            FROM sqlite_master
            WHERE type = 'table' AND name = ?
        """, (server,))
        exists = dbcur.fetchone()[0] == 1
        
        dbcur.close()
        return exists
    
    async def getTimestampFromPlayer(server:str, player:str):
        conn = sqlite3.connect('data/lastConnect.db')
        if not await mcquery.checkTableExists(conn, server):
            return 'error'
        
        c = conn.cursor()
        
        c.execute(f"SELECT lastConnection FROM {server} WHERE username = ?;", (player,))
        result = c.fetchone()
        if result:
            return result[0]
        else:
            return None
    
    async def findPlayer(player:str):
        for key in servers.keys():
            players = [player.lower() for player in await mcquery.getPlayers(servers[key]['ip'], servers[key]['port'])]
            if player.lower() in players:
                return key