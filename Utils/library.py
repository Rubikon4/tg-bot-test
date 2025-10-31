import os



async def read_file(file_path: str) -> str:
    """Читает файлы и возвращает их содержимое в виде строки."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()