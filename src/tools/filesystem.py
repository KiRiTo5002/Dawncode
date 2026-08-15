from pathlib import Path

from src.tools.base import Tool


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


read_file_tool = Tool(
    name="read_file",
    description="Read the contents of a file.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The path of the file to read.",
            }
        },
        "required": ["path"],
    },
    function=read_file,
)

list_directory_tool = Tool(
    name="list_directory",
    description="List the contents of a directory.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The path of the directory to list.",
            }
        },
        "required": ["path"],
    },
    function=list_directory,
)
