import asyncio
import click
from dataclasses import dataclass
from datetime import datetime
from typing import List
from dataclasses_json import dataclass_json

from common import REVIEWER_SYSTEM_MESSAGE, WRITER_SYSTEM_MESSAGE, completion


@dataclass_json
@dataclass
class Message:
    agent: str
    role: str
    content: str
    ts: datetime


class BaseAgent:
    """
    BaseAgent is a foundational class for creating agents that share a common context and interact with a system prompt.    
    """

    def __init__(self):
        # Agents share context **THIS IS IMPORTANT**
        self.name: str | None = None
        self.shared_context: List[Message] = []
        self.system_prompt: str | None = None

    def switch_context(self, context):
        # if the agent share_context has a systm prompt already, remove it, and add the current system prompt as first one on the list
        if self.shared_context and self.shared_context[0].role == "system":
            self.shared_context.pop(0)
        if self.system_prompt:
            self.shared_context.insert(
                0, Message(agent=self.name, role="system", content=self.system_prompt, ts=datetime.now()))

    async def process(self, task: str | None = None, messages: List[Message] = None):
        print(f"Agent: {self.name}")
        self.shared_context = messages if messages else []

        # Switch system message based on agent
        self.switch_context(self.system_prompt)

        if task:
            self.shared_context.append(
                Message(agent=self.name, role="user", content=task, ts=datetime.now()))

        # Call the LLM
        result = await completion(self.serialized_messages())

        # add result to context
        self.shared_context.append(
            Message(agent=self.name, role="user", content=result, ts=datetime.now()))

        return self.shared_context

    def serialized_messages(self) -> List[dict]:
        serializable_messages = [message.to_dict()
                                 for message in self.shared_context]
        return serializable_messages


class Agent(BaseAgent):
    """
    Represents an agent in a multi-agent system.
    """

    def __init__(self, name: str, system: str | None = None):
        super().__init__()
        self.name = name
        self.system_prompt = system


class AgentManager:
    """
    The AgentManager class is responsible for managing and executing a sequence of agents in a pipeline. 
    """

    def __init__(self):
        self.agent_list: List[BaseAgent] = []

    def register(self, agent: BaseAgent):
        """
        Registers an agent in the agent list.
        Args:
            agent (BaseAgent): The agent to be registered.
        """
        self.agent_list.append(agent)

    async def process(self, task: str) -> List[Message]:
        """
        Executes a sequence of agents in a pipeline, sharing a common message context.
        """

        # Note: sharing messages between agents
        # this is key as the message context is shared between agents
        shared_message_context = [Message(agent="user", role="user",
                                          content=task, ts=datetime.now())]
        for agent in self.agent_list:
            # run the agent
            context = await agent.process(messages=shared_message_context)
            shared_message_context = context
        shared_message_context.append(
            Message(agent="runner", role="runner", content="Done", ts=datetime.now()))
        print("Final context:")
        for message in shared_message_context:
            if message.agent == "doc_author":
                click.echo(click.style(
                    f"{message.agent} <-> {message.role}:\n{message.content}", fg="green"))
            else:
                click.echo(click.style(
                    f"{message.agent} <-> {message.role}:\n{message.content}", fg="yellow"))
            # print(f"{message.agent} <-> {message.role}:\n{message.content}")
        return shared_message_context


async def main():
    manager = AgentManager()

    # Create two agents
    document_author = Agent(
        "doc_author", system=WRITER_SYSTEM_MESSAGE)
    document_reviewer = Agent(
        "doc_reviewer", system=REVIEWER_SYSTEM_MESSAGE)

    manager.register(document_author)
    manager.register(document_reviewer)

    await manager.process(
        "Write a technical document about prompt engineering.")

if __name__ == "__main__":

    asyncio.run(main())
