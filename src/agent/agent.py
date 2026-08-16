import json

from src.models.llm import LLMClient
from src.tools.filesystem import (
    edit_file_tool,
    list_directory_tool,
    read_file_tool,
    write_file_tool,
)


async def stream_response(client, messages, tool_schemas):
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

            # Accumulate streamed tool calls.
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

            # Stream assistant content.
            if delta.content and delta.content.strip():
                if not started_content:
                    print("DawnCode: ", end="", flush=True)
                    started_content = True

                print(delta.content, end="", flush=True)
                assistant_content += delta.content

    finally:
        await response.close()

    if started_content:
        print()

    return assistant_content, tool_calls


def build_assistant_tool_calls(tool_calls):
    """Convert accumulated tool calls into API message format."""

    assistant_tool_calls = []

    for call in tool_calls.values():
        assistant_tool_calls.append(
            {
                "id": call["id"],
                "type": "function",
                "function": {
                    "name": call["name"],
                    "arguments": call["arguments"],
                },
            }
        )

    return assistant_tool_calls


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

    tools = [
        read_file_tool,
        list_directory_tool,
        write_file_tool,
        edit_file_tool
    ]

    tool_schemas = [
        tool.to_schema()
        for tool in tools
    ]

    messages = []

    try:
        while True:
            user_input = input("input:").strip()

            if user_input.lower() == "exit":
                break

            messages.append(
                {
                    "role": "user",
                    "content": user_input,
                }
            )

            # One user request can require multiple
            # LLM -> tool -> LLM cycles.
            while True:
                assistant_content, tool_calls = await stream_response(
                    client=client,
                    messages=messages,
                    tool_schemas=tool_schemas,
                )

                # No tool call means this is the final response.
                if not tool_calls:
                    messages.append(
                        {
                            "role": "assistant",
                            "content": assistant_content,
                        }
                    )

                    break

                # Record the assistant's tool-call request.
                assistant_tool_calls = build_assistant_tool_calls(
                    tool_calls
                )

                messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_content,
                        "tool_calls": assistant_tool_calls,
                    }
                )

                # Execute tools and add their results to the conversation.
                execute_tool_calls(
                    tool_calls=tool_calls,
                    tools=tools,
                    messages=messages,
                )

                # Run the LLM again with the tool results.

    finally:
        await client.close()