import subprocess
from pathlib import Path

from src.tools.base import Tool


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


def read_file(path: str):
    try:
        with open(path, "r") as file:
            return file.read()

    except FileNotFoundError:
        return f"File not found: {path}"

    except IsADirectoryError:
        return f"Path is a directory, not a file: {path}"


def write_file(path: str, content: str):
    try:
        file_path = Path(path)

        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w") as file:
            file.write(content)

        return f"Successfully wrote to {path}"

    except OSError as error:
        return f"Failed to write to {path}: {error}"

def edit_file(path: str, old_content: str, new_content: str):
    try:
        with open(path, "r") as file:
            data = file.read()

        count = data.count(old_content)

        if count == 0:
            return f"Could not edit {path}: old content was not found."

        if count > 1:
            return (
                f"Could not edit {path}: old content was found "
                f"{count} times. The match must be unique."
            )

        updated_data = data.replace(old_content, new_content)

        with open(path, "w") as file:
            file.write(updated_data)

        return f"Successfully edited {path}."

    except FileNotFoundError:
        return f"Could not edit {path}: file does not exist."

    except OSError as error:
        return f"Could not edit {path}: {error}"




def execute_command(command: str) -> str:
    """
    Execute a shell command and return its output and exit code.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=False,
        )

        return (
            f"Exit Code: {result.returncode}\n\n"
            f"STDOUT:\n{result.stdout or '[No output]'}\n\n"
            f"STDERR:\n{result.stderr or '[No errors]'}"
        )

    except Exception as e:  # noqa: BLE001
        return (
            "Exit Code: -1\n\n"
            "STDOUT:\n[No output]\n\n"
            f"STDERR:\n{e}"
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

write_file_tool = Tool(
    name="write_file",
    description=(
        "Write content to a file. This replaces the entire existing "
        "contents of the file. Creates the file and any missing parent "
        "directories if they do not exist."
    ),
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The path of the file to write.",
            },
            "content": {
                "type": "string",
                "description": "The complete content to write to the file.",
            },
        },
        "required": ["path", "content"],
    },
    function=write_file,
)

edit_file_tool = Tool(
    name="edit_file",
    description=(
        "Edit an existing file by replacing a specific piece of content "
        "with new content. The old content must exist exactly once in the "
        "file. If it is not found or appears more than once, the file will "
        "not be modified."
    ),
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The path of the file to edit.",
            },
            "old_content": {
                "type": "string",
                "description": (
                    "The exact existing content to replace. "
                    "It must occur exactly once in the file."
                ),
            },
            "new_content": {
                "type": "string",
                "description": "The new content that will replace old_content.",
            },
        },
        "required": ["path", "old_content", "new_content"],
    },
    function=edit_file,
)
execute_command_tool = Tool(
    name="execute_command",
    description=(
        "Execute a shell command in the current workspace. "
        "Returns the command's exit code, standard output, and standard error."
    ),
    parameters={
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The shell command to execute.",
            }
        },
        "required": ["command"],
    },
    function=execute_command,
)