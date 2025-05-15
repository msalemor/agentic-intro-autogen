import asyncio
import click
from common import REVIEWER_SYSTEM_MESSAGE, WRITER_SYSTEM_MESSAGE, get_creative_model_client, get_model_client

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination


doc_writer = AssistantAgent(
    "doc_writer",
    model_client=get_creative_model_client(),
    system_message=WRITER_SYSTEM_MESSAGE,
)

# Create the critic agent.
doc_reviewer = AssistantAgent(
    "doc_reviewer",
    model_client=get_model_client(),
    system_message=REVIEWER_SYSTEM_MESSAGE,
)

# Define a termination condition that stops the task if the critic approves.
text_termination = TextMentionTermination("APPROVE")


async def process(task: str) -> None:
    team = RoundRobinGroupChat(
        [doc_writer, doc_reviewer], termination_condition=text_termination)
    res = team.run_stream(task=task)
    # await Console(res)  # Stream the messages to the console.
    async for message in res:
        # print(message)
        if isinstance(message, str):
            print("String message:", message)
        elif hasattr(message, "content"):
            if hasattr(message, "source"):
                # print("Message role:", message.role)
                click.echo(click.style(message.source +
                           "\n", fg='cyan', bold=True))
            # print("Message content:", message.content)
            if message.source == "doc_writer":
                click.echo(click.style(message.content + "\n", fg="green"))
            else:
                click.echo(click.style(message.content + "\n", fg="yellow"))
        else:
            # print("Other message type:", message)
            try:
                msg = message.messages[-1]
                # print(msg)
                click.echo(click.style(msg.content + "\n", fg="orange"))
            except Exception as e:
                pass


async def main():
    await process("Write a technical document about prompt engineering.")

    # Run the asynchronous function
if __name__ == "__main__":
    asyncio.run(main())
