# DawnCode

DawnCode is an AI-powered coding assistant that runs in your terminal. It uses a Large Language Model (LLM) to understand your requests and can perform file operations and execute commands in your workspace.

## What the Application Does

DawnCode provides an interactive terminal-based chat interface where you can:

- Ask questions about your codebase
- Request file operations (read, write, edit, list directories)
- Execute shell commands
- Get help with coding tasks

The agent maintains conversation context and can chain multiple tool calls to accomplish complex tasks.

> **This README was written by DawnCode.**
>
> DawnCode inspected its own Python source code, generated this documentation, wrote it to `README.md`, and then read it back to verify the result.

## Current Tool Capabilities

DawnCode currently provides 5 tools that the LLM can invoke:

| Tool | Description |
| ------ | ------------- |
| `list_directory` | List the contents of a directory |
| `read_file` | Read the contents of a file (UTF-8 text files only) |
| `write_file` | Write content to a file, creating parent directories as needed |
| `edit_file` | Replace specific content in a file (requires exact unique match) |
| `execute_command` | Execute a shell command and return exit code, stdout, and stderr |

## How the Agent Loop Works

The agent runs a continuous conversation loop:

1. **User Input** - The terminal prompts for user input
2. **Message History** - User message is added to the conversation history
3. **Stream LLM Response** - The LLM streams a response, which may include:
   - Text content (displayed in real-time)
   - Tool calls (accumulated during streaming)
4. **Handle Tool Calls** - If the LLM made tool calls:
   - Execute each tool call
   - Append tool results to the conversation
   - Loop back to step 3 for the LLM to continue
5. **No Tool Calls** - If the LLM responds without tool calls, the assistant message is added to history and the loop waits for the next user input
6. **Exit** - Type "exit" to quit

The loop handles retries (up to 5 attempts with 2-second delays) for failed LLM requests.

## Project Structure

```
dawncode/
├── main.py                 # Entry point
├── pyproject.toml          # Project configuration
├── .env.example            # Example environment variables
├── src/
│   ├── agent/
│   │   ├── __init__.py
│   │   └── agent.py        # Main agent loop and streaming logic
│   ├── models/
│   │   ├── __init__.py
│   │   └── llm.py          # LLM client wrapper (AsyncOpenAI)
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── base.py         # Tool base class
│   │   └── filesystem.py   # File system and command execution tools
│   └── utils/
│       ├── __init__.py
│       ├── config.py       # Configuration loading from .env
│       └── terminal.py     # Rich-based terminal UI
```

## Main Python Modules and Their Responsibilities

### `main.py`

Entry point. Initializes the terminal UI and runs the async agent loop.

### `src/agent/agent.py`

Core agent logic:

- `stream_response()` - Streams LLM response, accumulates tool calls
- `build_assistant_tool_calls()` - Converts accumulated tool calls to API message format
- `execute_tool_calls()` - Executes tool calls and appends results to conversation
- `agent()` - Main async loop handling user input, LLM interaction, and tool execution

### `src/models/llm.py`

`LLMClient` class wrapping `AsyncOpenAI`:

- Configures client with API key and base URL from environment
- Provides `chat_completion_stream()` with retry logic (5 attempts)
- Sends `enable_thinking: True` and `reasoning_budget: 4096` in extra_body
- Handles cleanup with `close()`

### `src/tools/base.py`

`Tool` base class:

- Stores name, description, parameters schema, and executable function
- `to_schema()` - Returns OpenAI function calling schema
- `execute()` - Calls the wrapped function with provided arguments

### `src/tools/filesystem.py`

Five concrete tool implementations:

- `list_directory(path)` - Returns newline-separated directory entries
- `read_file(path)` - Returns file content or error message
- `write_file(path, content)` - Creates directories, writes file
- `edit_file(path, old_content, new_content)` - Replaces exact unique match only
- `execute_command(command)` - Runs shell command, returns exit code + stdout + stderr

Each tool is instantiated as a `Tool` object with its JSON schema.

### `src/utils/config.py`

Loads configuration from `.env` file using `python-dotenv`:

- `NVIDIA_API_KEY` - API key for NVIDIA API
- `BASE_URL` - API base URL (default: `https://integrate.api.nvidia.com/v1`)
- `MODEL` - Model identifier (default: `nvidia/nemotron-3-ultra-550b`)

### `src/utils/terminal.py`

`Terminal` class using `rich` for UI:

- `show_banner()` - Displays ASCII art banner
- `user_input()` - Prompts for user input with styled prompt
- `start_assistant()` / `stream_assistant()` / `end_assistant()` - Streaming output handling
- `error()` - Displays error messages in red

## How to Configure the Application

1. Copy `.env.example` to `.env`:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your credentials:

   ```env
   NVIDIA_API_KEY=your_actual_api_key
   BASE_URL=https://integrate.api.nvidia.com/v1
   MODEL=nvidia/nemotron-3-ultra-550b
   ```

Required: `NVIDIA_API_KEY` must be set. The other two have defaults shown above.

## How to Run It

### Using uv (recommended)

```bash
uv sync
uv run main.py
```

### Using pip

```bash
pip install -e .
python main.py
```

### Direct execution (if dependencies installed)

```bash
python main.py
```

## Current Limitations

1. **Single model provider** - Only works with OpenAI-compatible APIs (tested with NVIDIA API)
2. **No persistent memory** - Conversation history is lost when the application exits
3. **No file type detection** - `read_file` only works with UTF-8 text files; binary files return an error
4. **Edit tool strictness** - `edit_file` requires the old content to match exactly once; no fuzzy matching
5. **No sandboxing** - `execute_command` runs with full user permissions in the workspace
6. **Fixed retry logic** - Retries are hardcoded to 5 attempts with 2-second delays
7. **No conversation export** - No way to save or load conversation history
8. **Single-threaded** - Only one conversation at a time
9. **No configuration file** - All config via environment variables only
10. **No tests** - No test suite exists in the current codebase
