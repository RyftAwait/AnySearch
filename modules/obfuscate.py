import random
import string

def message(message:str) -> str:
    RLO = "\u202E"
    LRO = "\u202D"
    PDF = "\u202C"
    
    obfuscators = [RLO, LRO]
    obfuscated_message = ""
    
    for char in message:
        obfuscated_message += random.choice(obfuscators) + char + PDF
    
    characters = string.ascii_letters + string.digits
    fileName = ''
    
    for _ in range(12):
        fileName = fileName + random.choice(characters)
    
    with open(f"temp/{fileName}.txt", "w") as f:
        f.write(obfuscated_message)
        
    return fileName