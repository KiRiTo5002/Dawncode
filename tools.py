def read_file(path):
    try:
        with open(path, "r") as file:
            return file.read()

    except FileNotFoundError:
        return f"File not found: {path}"

    except IsADirectoryError:
        return f"Path is a directory, not a file: {path}"
