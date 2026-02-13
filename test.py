async def searchFile(file_path, keyword): # type: ignore
    try:
        pattern = re.compile(re.escape(keyword.lower()))
        async with aiofiles.open(file_path, 'r', encoding='latin-1') as f: # type: ignore
            line_number = 0
            async for line in f:
                line_number += 1
                if pattern.search(line.lower()):
                    yield (line.replace('\n', ''), line_number)
    except UnicodeDecodeError:
        logger.error(f"\033[38;2;255;0;0mErreur d'encodage: {file_path}")