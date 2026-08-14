import asyncio

from llm import LLMClient


async def main():
    client = LLMClient()

    messages = []

    while True:
        user_input = input("input:").strip()

        if user_input.lower() == "exit":
            break
        
        message = {"role": "user", "content": user_input}

        messages.append(message)

        response = await client.chat_completion(messages)

        if response:
            print(f"Dawncode:{response}")
            message = {"role": "assistant", "content": response}

            messages.append(message)


asyncio.run(main())
