from pathlib import Path


def read_file(path: str):
    try:
        with open(path, "r") as file:
            return file.read()

    except FileNotFoundError:
        return f"File not found: {path}"

    except IsADirectoryError:
        return f"Path is a directory, not a file: {path}"

def list_directory(path: str):
    try:
        items = []
        dir_path = Path(path)

        for item in dir_path.iterdir():
            items.append(item.name)

        return "\n".join(items)

    except FileNotFoundError:
        return f"Directory not found: {path}"

    except NotADirectoryError:
        return f"Path is not a directory: {path}"
    
