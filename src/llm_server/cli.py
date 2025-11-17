import typing as t

import httpx
import typer

from llm_server.model import SYSTEM_PROMPT, Message, Model
from llm_server.schemas import Reply

app = typer.Typer()


@app.command("api")
def api_chat(
    host: t.Annotated[str, typer.Option],
    chat_id: t.Annotated[str, typer.Option()],
):
    message = Reply(
        message="SOC",
    )

    print("Enter a message with 'EOC' to end the chat.")

    while message.message != "EOC":
        message = Reply(
            message=input(">>> "),
        )
        if message.message == "EOC":
            break

        # send chat request
        response = httpx.post(
            f"{host}/api/v1/chat/{chat_id}", json=message.model_dump()
        )
        response = Reply.model_validate_json(response.content)

        print(response.message)


@app.command("local")
def local_chat(
    system_prompt: t.Annotated[str, typer.Option()] = SYSTEM_PROMPT,
):
    # Initialize chat
    context = []
    message = Message(
        role="user",
        content="SOC",
    )

    # Initialize model
    model = Model(system_prompt=system_prompt)
    model.load()

    print("Enter a message with 'EOC' to end the chat.")

    while message.content != "EOC":
        message = Message(
            role="user",
            content=input(">>> "),
        )
        if message.content == "EOC":
            break

        response = model.chat(
            message.content,
            context=context,
        )
        print(response.content)

        # Add interaction to context
        context.append(message)
        context.append(response)
