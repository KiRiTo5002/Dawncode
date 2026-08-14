# DawnCode

A lightweight coding agent built from scratch to explore how AI coding assistants work under the hood.

DawnCode is a learning project inspired by tools like Claude Code. The goal is to understand and implement the core ideas behind an AI coding agent rather than relying on a framework that hides the underlying mechanics.

## Current Status

DawnCode currently supports:

* Asynchronous LLM communication through OpenRouter
* Configurable LLM provider settings
* Conversation history
* Interactive terminal chat
* Basic filesystem access through a `read_file` tool

The project is intentionally being built incrementally. Features are added when they are needed rather than starting with a large framework or complex architecture.

## Tech Stack

* Python
* OpenAI Python SDK
* OpenRouter
* `python-dotenv`
* AsyncIO

## Project Structure

```text
DawnCode/
├── main.py
├── llm.py
├── config.py
├── tools.py
├── .env
└── README.md
```

## How It Works

The current architecture is intentionally small:

```text
User
  │
  ▼
main.py
  │
  ▼
LLMClient
  │
  ▼
OpenRouter
  │
  ▼
LLM
  │
  ▼
Response
```

Conversation history is maintained as a list of messages and sent back to the model with each request.

The next stage is to allow the model to request tools and have DawnCode execute those tools on its behalf.

## Setup

Clone the repository and create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install openai python-dotenv
```

Create a `.env` file:

```env
OPEN_ROUTER_API_KEY=your_api_key
BASE_URL=https://openrouter.ai/api/v1
MODEL=your_model
```

Then run:

```bash
python main.py
```

## Example

```text
input: hello
DawnCode: Hello! How can I help you?

input: what is Python?
DawnCode: Python is a general-purpose programming language...

input: exit
```

## Roadmap

The project will gradually evolve from a simple LLM chat interface into a functional coding agent.

* [x] Basic LLM client
* [x] Async LLM requests
* [x] Conversation history
* [x] Interactive CLI
* [x] Basic file reading capability
* [ ] LLM tool calling
* [ ] File editing
* [ ] Shell command execution
* [ ] Agent loop
* [ ] Project context
* [ ] Permission and safety controls
* [ ] Git integration
* [ ] Better terminal interface
* [ ] Context management
* [ ] More advanced agent capabilities

## Goal

The goal of DawnCode is not simply to build another AI wrapper.

It is to understand how coding agents work internally:

```text
LLM
 │
 ├── Understand the task
 │
 ├── Decide whether a tool is needed
 │
 ├── Request a tool
 │
 ├── Receive the result
 │
 ├── Continue reasoning
 │
 └── Produce the final response
```

The implementation will remain deliberately small and understandable as the project grows.

## License

This project is currently a personal learning project.
