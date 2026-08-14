import asyncio

from llm import LLMClient
from tools import read_file

import json


async def main():
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
        }
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

            if function == "read_file":
                result = read_file(args["path"])

                messages.append(
                    {
                        "role": "assistant",
                        "content": response.content,
                        "tool_calls": response.tool_calls,
                        "reasoning_details": response.reasoning_details,
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
            print(f"DawnCode: {response.content}")

            message = {"role": "assistant", "content": response.content}

            messages.append(message)


asyncio.run(main())
