import asyncio
import click
from common import get_creative_model_client, get_model_client

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination


comedian_knock_knock_agent = AssistantAgent(
    "knock_knock",
    model_client=get_creative_model_client(),
    system_message="You are a funny comedian that can tell knock knock jokes. Make sure that the joke is funny and has a punchline.",
)

# Create the critic agent.
comedian_cross_the_road_agent = AssistantAgent(
    "cross_the_road",
    model_client=get_creative_model_client(),
    system_message="You are a funny comedian that can tell the chicken that crossed the road jokes. Make sure that the joke is funny and has a punchline.",
)

# terminate_on = TextMentionTermination("TERMINATE")

team = RoundRobinGroupChat(
    [comedian_knock_knock_agent, comedian_cross_the_road_agent],
    termination_condition=None,
    max_turns=None,)


async def main():
    # await Console(team.run_stream(task="tell me a joke"))
    res = team.run_stream(task="tell me a joke")
    count = 0
    async for message in res:
        if count % 2 == 0:
            click.echo(click.style(message.content, fg="green"))
        else:
            click.echo(click.style(message.content, fg="yellow"))
        click.echo("")
        count += 1


if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())
