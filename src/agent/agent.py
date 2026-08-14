import json

from src.models.llm import LLMClient
from src.tools.filesystem import list_directory, read_file


async def agent():

    tool_functions = {
        "read_file": read_file,
        "list_directory": list_directory,
    }
    client = LLMClient()

    messages = []
    tools = [
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read the contents of a file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path of the file to read.",
                        }
                    },
                    "required": ["path"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_directory",
                "description": "List the contents of a directory.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path of the directory to list.",
                        }
                    },
                    "required": ["path"],
                },
            },
        },
    ]

    while True:
        user_input = input("input:").strip()

        if user_input.lower() == "exit":
            break

        message = {"role": "user", "content": user_input}

        messages.append(message)

        response = await client.chat_completion(messages=messages, tools=tools)
        if response.tool_calls:
            tool_call = response.tool_calls[0]
            function = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            if function in tool_functions:
                result = tool_functions[function](**args)

                messages.append(
                    {
                        "role": "assistant",
                        "content": response.content,
                        "tool_calls": response.tool_calls,
                    }
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    }
                )

                response = await client.chat_completion(
                    messages=messages,
                    tools=tools,
                )

                print(f"DawnCode: {response.content}")
            else:
                print(f"Unknown tool: {function}")

        else:
            print(f"DawnCode: {response.content}")
            message = {"role": "assistant", "content": response.content}
            messages.append(message)
