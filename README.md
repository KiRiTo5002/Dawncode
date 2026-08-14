# DawnCode

DawnCode is a coding agent built from scratch in Python.

The goal of the project is to understand how AI coding agents work internally by implementing the core agent loop ourselves instead of relying on an agent framework.

DawnCode currently uses NVIDIA Nemotron 3 Ultra 550B through NVIDIA's OpenAI-compatible API.

## Current Capabilities

- Maintain conversation history
- Communicate asynchronously with an LLM
- Use LLM function/tool calling
- Read files from a project
- List directory contents
- Execute tools selected by the LLM
- Send tool results back to the LLM
- Continue the conversation after tool execution
- Use a simple tool registry for multiple tools

## How It Works

The core agent loop currently looks like:

```text
User
  ↓
LLM
  ↓
Tool Call
  ↓
DawnCode executes Python function
  ↓
Tool Result
  ↓
LLM
  ↓
Final Response
```

For example:

```text
User: What is inside src/models/llm.py?
                    ↓
Nemotron decides to use read_file
                    ↓
read_file("src/models/llm.py")
                    ↓
DawnCode executes the function
                    ↓
File contents are returned to Nemotron
                    ↓
Nemotron generates the final response
```

## Current Tools

### `read_file`

Reads the contents of a file.

```python
read_file("src/models/llm.py")
```

### `list_directory`

Lists the contents of a directory.

```python
list_directory("src/models")
```

Example result:

```text
llm.py
__init__.py
__pycache__
```

## Project Structure

```text
DawnCode/
│
├── main.py
│
├── src/
│   ├── agent/
│   │   ├── __init__.py
│   │   └── agent.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── llm.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   └── filesystem.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── config.py
│
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

### `main.py`

Application entry point. Starts the asynchronous DawnCode agent.

### `src/agent/`

Contains the agent loop and conversation handling.

Responsible for:

- User input
- Conversation history
- Tool definitions
- Tool selection
- Tool execution
- Sending tool results back to the LLM

### `src/models/`

Contains the LLM client and API communication.

### `src/tools/`

Contains the capabilities available to DawnCode.

Currently:

- `read_file()`
- `list_directory()`

### `src/utils/`

Contains shared configuration and environment setup.

## LLM

DawnCode currently uses:

**NVIDIA Nemotron 3 Ultra 550B**

through NVIDIA's OpenAI-compatible API.

```text
https://integrate.api.nvidia.com/v1
```

The LLM decides when a tool is needed and determines the arguments to pass to it.

DawnCode is responsible for executing the requested Python function and returning the result.

## Configuration

Create a `.env` file based on `.env.example`.

```env
NVIDIA_API_KEY=your_api_key
BASE_URL=https://integrate.api.nvidia.com/v1
MODEL=nvidia/nemotron-3-ultra-550b
```

Never commit the API key to the repository.

## Running DawnCode

Install dependencies with `uv`:

```bash
uv sync
```

Then run:

```bash
python main.py
```

Example:

```text
input: what is inside src/models/llm.py?

DawnCode: The llm.py file contains...
```

Type `exit` to terminate the session.

## Design Philosophy

DawnCode is intentionally being built incrementally.

The purpose is to understand the mechanics behind coding agents rather than immediately hiding them behind an agent framework.

The architecture currently keeps responsibilities separated without introducing unnecessary abstractions:

```text
Agent
  │
  ├── LLM Client
  │
  └── Tools
       ├── read_file
       └── list_directory
```

New abstractions will be introduced when the complexity of the project actually requires them.

## Roadmap

- [x] LLM communication
- [x] Conversation history
- [x] Function/tool calling
- [x] File reading
- [x] Directory listing
- [x] Tool registry
- [x] Direct NVIDIA/Nemotron integration
- [ ] Improve the agent loop
- [ ] Write and modify files
- [ ] Search through a codebase
- [ ] Execute shell commands
- [ ] Support multiple tool calls
- [ ] Improve error handling
- [ ] Add project/context awareness
- [ ] Add tests
- [ ] Add streaming responses
- [ ] Build more autonomous coding workflows

## Current Status

DawnCode is in early development.

The fundamental:

```text
LLM → Tool Call → Tool Execution → Tool Result → LLM
```

loop is functional.

The next stage is expanding DawnCode's ability to understand and modify an existing codebase.

## Why Build This?

AI coding agents look simple from the outside, but underneath they require several interacting components:

- LLM reasoning
- Tool calling
- Tool execution
- Conversation state
- Context management
- File operations
- Command execution
- Error handling
- Agent loops

DawnCode is an attempt to understand those components by building them directly.

## License

This project is currently a personal learning and experimentation project.