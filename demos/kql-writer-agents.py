import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat
import click
from common import get_model_client


model_client = get_model_client()


async def mock_get_schema(name: str) -> dict:
    if name == "events":
        return {
            "cluster": "loggingevents.contoso.com",
            "database": "logs",
            "table": "events",
            "fields": "id (string),userid (string), ts (timestamp), event (string), systemid (string), type (string)",
            "description": "This table provides information about login events.\ntypes: infra, code, app, security, change",
        }
    if name == "users":
        return {
            "cluster": "loggingevents.contoso.com",
            "database": "logs",
            "table": "users",
            "fields": "userid (string), name (string)",
            "description": "This table provides information about users.",
        }
    if name == "system":
        return {
            "cluster": "master.contoso.com",
            "database": "services",
            "table": "systems",
            "fields": "systemid (string), name (string), ha (boolean)",
            "description": "this table provides system information.",
        }
    return {}


schema_getter_agent = AssistantAgent(
    "get_schema",
    model_client,
    tools=[mock_get_schema],
    system_message="""You are an AI that can get the table or function KQL schema. There are 3 main objects you can use to get the schema:
events: system events related to systems and users
users: user information
system: system information
""",
)

query_classifier_agent = AssistantAgent(
    "query_classifier_agent",
    model_client,
    system_message="""You are a AI that can classify the type of KQL query. Use the provided schema and the following labels to classify the requested query or user ask:

single-table: A query in one cluster for a single table.
multi-table single-cluster: A query that may span multiple tables but only one cluster and may include joining tables.
multi-table multi-cluster: A query that may span multiple tables and multiple clusters and may include joining tables.
Unknown: A query that cannot be classified. Analyze the query and pick the the best label to classify the query.

Output:
Query classification: <classification>
""",
)

example_generator_agent = AssistantAgent(
    "expample_generator",
    model_client,
    system_message="""You are an AI that can generate a KQL examples based on the classification labels that you are provided.

If the classification is 'single-table', the query example is: 
`events | where ts>ago(24h)`

if the classification is 'multi-table single-cluster', the query example is:
`events | join kind=inner (users) on $left.userid == $right.userid | where ts>ago(24h)`

if the classification is 'multi-table multi-cluster', the query example is:
`cluster('master.contoso.com').database('services').systems | join kind=inner (cluster('loggingevents.contoso.com').database('logs').events) on $left.systemid == $right.systemid | where ts>ago(24h)`

Output format:
Query sample: <query example>

""",
)

kql_query_generator_agent = AssistantAgent(
    "gen_kql_query",
    model_client,
    system_message="""You are an AI that can generate a KQL queries based on the user's request, the schema and sample provided. 

Once query is generated finish with 'TERMINATE'.\n""",
)

text_termination = TextMentionTermination("TERMINATE")

team = RoundRobinGroupChat(
    [schema_getter_agent, query_classifier_agent,
        example_generator_agent, kql_query_generator_agent],
    termination_condition=text_termination
)


async def process_agent_messages(task: str):
    res = team.run_stream(task=task)
    # await Console(res)  # Stream the messages to the console.
    print(f"Task:\n{task}\n")
    async for message in res:
        if isinstance(message, str):
            # print("String message:", message)
            pass
        elif hasattr(message, "content"):
            # if hasattr(message, "source"):
            #     # print("Message role:", message.role)
            #     click.echo(click.style(message.source +
            #                "\n", fg='yellow', bold=True))
            # # print("Message content:", message.content)
            click.echo(click.style(message.content + "\n", fg="yellow"))
            # pass
        else:
            # print("Other message type:", message)
            try:
                print("Result:")
                click.echo(click.style(
                    f"{message.messages[-1].content}\n", fg="green"))
            except Exception as e:
                pass


async def main():
    await Console(team.run_stream(
        task="Find all the infra events in the last 1 hour"))
    # await Console(team.run_stream(
    #     task="Find all the infra events in the last 1 hour. Show the user's name"))
    await Console(team.run_stream(
        task="Find all the events by user name and system name in the last 24 hours of type change"))

    # Note: display only the result
    await process_agent_messages(task="Find all the infra events in the last 1 hour")
    # await process_agent_messages(task="Find all the codes events in the last 1 hour. Show the user name.")
    # await process_agent_messages(task="Write a query to find all events by user name and system name in the last 24 hours")

if __name__ == "__main__":
    asyncio.run(main())
