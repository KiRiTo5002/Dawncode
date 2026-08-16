import json

from openai import APIError

from src.models.llm import LLMClient
from src.tools.filesystem import (
    edit_file_tool,
    execute_command_tool,
    list_directory_tool,
    read_file_tool,
    write_file_tool,
)
from src.utils.terminal import Terminal


async def stream_response(client, terminal, messages, tool_schemas):
    """Stream an LLM response and collect any tool calls."""
    response = await client.chat_completion_stream(
        messages=messages,
        tools=tool_schemas,
    )
    assistant_content = ""
    tool_calls = {}
    started_content = False

    try:
        async for chunk in response:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta

            if delta.tool_calls:
                for call in delta.tool_calls:
                    if call.index not in tool_calls:
                        tool_calls[call.index] = {
                            "id": call.id,
                            "name": call.function.name,
                            "arguments": call.function.arguments or "",
                        }
                    else:
                        tool_calls[call.index]["arguments"] += (
                            call.function.arguments or ""
                        )

            if delta.content:
                if not started_content:
                    if not delta.content.strip():
                        continue
                    terminal.start_assistant()
                    started_content = True

                terminal.stream_assistant(delta.content)
                assistant_content += delta.content
                
                
    finally:
        await response.close()

    if started_content:
        terminal.end_assistant()

    return assistant_content, tool_calls


def build_assistant_tool_calls(tool_calls):
    """Convert accumulated tool calls into API message format."""
    return [
        {
            "id": call["id"],
            "type": "function",
            "function": {
                "name": call["name"],
                "arguments": call["arguments"],
            },
        }
        for call in tool_calls.values()
    ]


def execute_tool_calls(tool_calls, tools, messages):
    """Execute tool calls and append their results to the conversation."""
    for call in tool_calls.values():
        function_name = call["name"]
        arguments = json.loads(call["arguments"])

        for tool in tools:
            if tool.name == function_name:
                result = tool.execute(**arguments)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call["id"],
                        "content": result,
                    }
                )
                break


async def agent():
    client = LLMClient()
    terminal = Terminal()
    tools = [
        read_file_tool,
        list_directory_tool,
        write_file_tool,
        edit_file_tool,
        execute_command_tool
    ]
    tool_schemas = [tool.to_schema() for tool in tools]
    messages = []

    try:
        while True:
            user_input = terminal.user_input().strip()

            if user_input.lower() == "exit":
                break

            messages.append(
                {
                    "role": "user",
                    "content": user_input,
                }
            )

            while True:
                try:
                    assistant_content, tool_calls = await stream_response(
                        client=client,
                        terminal=terminal,
                        messages=messages,
                        tool_schemas=tool_schemas,
                    )

                    if not tool_calls:
                        messages.append(
                            {
                                "role": "assistant",
                                "content": assistant_content,
                            }
                        )
                        break
            

                    messages.append(
                        {
                            "role": "assistant",
                            "content": assistant_content,
                            "tool_calls": build_assistant_tool_calls(tool_calls),
                        }
                    )

                    execute_tool_calls(
                        tool_calls=tool_calls,
                        tools=tools,
                        messages=messages,
                    )
                except APIError as e:
                    terminal.error(f"LLM Request Failed:{e}")
    finally:
        await client.close()