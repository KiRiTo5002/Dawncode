# DawnCode

DawnCode is a coding agent built from scratch in Python.

The goal of the project is to understand how AI coding agents work internally by implementing the core agent loop ourselves instead of relying on an agent framework.

DawnCode currently uses NVIDIA Nemotron 3 Ultra 550B through an OpenAI-compatible API.

## Current Capabilities

- Maintain conversation history
- Communicate asynchronously with an LLM
- Stream LLM responses
- Use LLM function/tool calling
- Accumulate streamed tool-call arguments
- Read files from a project
- List directory contents
- Execute tools selected by the LLM
- Send tool results back to the LLM
- Continue the agent loop after tool execution
- Support multiple tools
- Use a `Tool` abstraction for defining tool capabilities

## How It Works

The core agent loop currently looks like:


User
  ↓
LLM
  ↓
Stream response
  ↓
Tool Call
  ↓
Accumulate tool-call data
  ↓
DawnCode executes Python function
  ↓
Tool Result
  ↓
LLM
  ↓
Final Response
`

For example:


User: What is inside src/models/llm.py?
                    ↓
Nemotron decides to use read_file
                    ↓
DawnCode accumulates the streamed tool call
                    ↓
read_file("src/models/llm.py")
                    ↓
DawnCode executes the function
                    ↓
File contents are returned to Nemotron
                    ↓
Nemotron generates the final response


The agent can also chain multiple tool calls when the model needs to explore the project before answering.

For example:


User: What is inside llm.py?
                    ↓
read_file("llm.py")
                    ↓
File not found
                    ↓
list_directory(".")
                    ↓
list_directory("src")
                    ↓
list_directory("src/models")
                    ↓
read_file("src/models/llm.py")
                    ↓
Final response


## Current Tools

### `read_file`

Reads the contents of a file.

python
read_file("src/models/llm.py")


### `list_directory`

Lists the contents of a directory.

python
list_directory("src/models")


Example result:


llm.py
__init__.py
__pycache__


## Tool Architecture

DawnCode uses a small `Tool` abstraction to separate the actual Python function from the information exposed to the LLM.

Each tool contains:

- A name
- A description
- A parameter schema
- The Python function used to execute it

The tool converts itself into an OpenAI-compatible function schema before being passed to the LLM.


Tool
├── name
├── description
├── parameters
└── function


The current tools are implemented in `src/tools/filesystem.py`.

## Project Structure


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
│   │   ├── base.py
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


### `main.py`

Application entry point. Starts the asynchronous DawnCode agent.

### `src/agent/`

Contains the agent loop and conversation handling.

Responsible for:

- User input
- Conversation history
- Streaming LLM responses
- Collecting tool calls
- Tool execution
- Sending tool results back to the LLM

### `src/models/`

Contains the LLM client and API communication.

### `src/tools/`

Contains the capabilities available to DawnCode.

Currently:

- `read_file()`
- `list_directory()`

`base.py` contains the `Tool` abstraction used to define and execute tools.

### `src/utils/`

Contains shared configuration and environment setup.

## LLM

DawnCode currently uses:

**NVIDIA Nemotron 3 Ultra 550B**

through an OpenAI-compatible API.

The LLM decides when a tool is needed and determines the arguments to pass to it.

DawnCode is responsible for:

1. Receiving the streamed response
2. Accumulating tool-call fragments
3. Parsing the tool arguments
4. Executing the requested Python function
5. Returning the result to the LLM

## Configuration

Create a `.env` file based on `.env.example`.

env
NVIDIA_API_KEY=your_api_key
BASE_URL=https://integrate.api.nvidia.com/v1
MODEL=nvidia/nemotron-3-ultra-550b


Never commit the API key to the repository.

## Running DawnCode

Install dependencies with `uv`:

bash
uv sync


Then run:

bash
python main.py


Example:


input: what is inside src/models/llm.py?

DawnCode: The llm.py file contains...


Type `exit` to terminate the session.

## Design Philosophy

DawnCode is intentionally being built incrementally.

The purpose is to understand the mechanics behind coding agents rather than immediately hiding them behind an agent framework.

The architecture currently keeps responsibilities separated without introducing unnecessary abstractions:


Agent
  │
  ├── LLM Client
  │
  └── Tools
       ├── Tool
       │
       ├── read_file
       └── list_directory


New abstractions will be introduced when the complexity of the project actually requires them.

## Roadmap

- [x] LLM communication
- [x] Conversation history
- [x] Function/tool calling
- [x] File reading
- [x] Directory listing
- [x] Tool abstraction
- [x] Direct NVIDIA/Nemotron integration
- [x] Streaming responses
- [x] Streamed tool-call accumulation
- [x] Tool execution loop
- [x] Sending tool results back to the LLM
- [x] Multiple tool calls
- [ ] Improve error handling
- [ ] Write and modify files
- [ ] Search through a codebase
- [ ] Execute shell commands
- [ ] Add project/context awareness
- [ ] Add tests
- [ ] Build more autonomous coding workflows

## Current Status

DawnCode is in early development.

The fundamental:


LLM → Tool Call → Tool Execution → Tool Result → LLM


loop is functional.

DawnCode can currently explore a project using filesystem tools, execute the tools selected by the LLM, and continue the agent loop until it can produce a final response.

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