# Introduction to Agentic solutions with AutoGen

## What is Agentic System

An agentic system is an autonomous artificial intelligence designed to operate independently, making decisions and performing tasks without human intervention. These systems continuously learn and adapt using techniques like reinforcement learning and deep learning, allowing them to improve their decision-making capabilities over time. They are versatile, with applications in areas such as process automation, healthcare, supply chain management, and business intelligence. While agentic systems offer significant benefits, including increased productivity and innovation, they also present risks like potential bias and errors, necessitating careful development and regulation.


## What is AutoGen (0.5.1)

A framework for building AI agents and applications.

Reference:
- [AutoGen](https://microsoft.github.io/autogen/stable/index.html)

### Top concepts

- Agent definition
- Termination
- Message observability and handling

### What is AutoGenChat

AgentChat is a high-level API for building multi-agent applications. It is built on top of the autogen-core package. 

Reference:
- [AutoGen AgentChat](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/index.html)

### What is AutoGen Core

AutoGen core offers an easy way to quickly build event-driven, distributed, scalable, resilient AI agent systems.

Reference:
- [AutoGen Core](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/index.html)

## Demos

### Writer/Reviewer without AutoGen

[Writer/Reviewer - No Agents](https://github.com/msalemor/agentic-intro-autogen/blob/main/demos/writer-reviewer.py)

### Write/Reviewer - Poor man's Agentic system

[Writer/Reviewer - Poor man's Agentic system](https://github.com/msalemor/agentic-intro-autogen/blob/main/demos/writer-reviewer-poor.py)

### Writer/Reviewer with AutoGen

[Agentic - Writer/Reviewer](https://github.com/msalemor/agentic-intro-autogen/blob/main/demos/writer-reviewer-agents.py)

### KQL Writer with AutoGen (more advanced solution)

[Agentic - KQL Writer](https://github.com/msalemor/agentic-intro-autogen/blob/main/demos/kql-write-agents.py)

### Demo 4 - Autogen Studio

Reference:
- [AutoGen Studio](https://microsoft.github.io/autogen/stable/user-guide/autogenstudio-user-guide/index.html)
