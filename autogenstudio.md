# AutoGen Studio Technical Documentation

## Overview

AutoGen Studio is a low-code platform for building, testing, and deploying multi-agent workflows powered by large language models (LLMs). It provides a web-based interface for creating, managing, and evaluating AI agent teams for tasks such as research, content generation, and data analysis.

---

## About AutoGen

AutoGen is a framework for building event-driven, distributed, and scalable AI agent systems. It is designed to enable the rapid development of multi-agent applications, supporting both simple and advanced use cases. AutoGen consists of two main layers:

### 1. AutoGen Core
- **Event-Driven Architecture:** Built on the Actor model, agents communicate through asynchronous messages, supporting both event-driven and request/response patterns.
- **Scalable & Distributed:** Supports building agent networks that can scale across organizational boundaries and run locally or in the cloud.
- **Multi-Language Support:** Python and .NET agents can interoperate, with more languages planned.
- **Modular & Extensible:** Features include custom agents, memory as a service, a tools registry, and a model library.
- **Observability:** Provides tracing and debugging tools for agent systems.

### 2. AgentChat
- **High-Level API:** AgentChat is built on top of AutoGen Core and is recommended for most users. It provides intuitive defaults, such as preset agent behaviors and teams with predefined multi-agent design patterns.
- **Teams and Patterns:** Supports teams of agents using patterns like Selector Group Chat, Swarm, and GraphFlow (workflow through a directed graph of agents).
- **Custom Agents:** Users can create agents with custom behaviors and memory capabilities.
- **Serialization:** Components can be serialized and deserialized for reuse and sharing.
- **Logging:** Built-in logging for traces and internal messages.

#### Resources
- [AgentChat User Guide](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/index.html)
- [Core User Guide](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/index.html)

AutoGen Studio leverages these capabilities to provide a low-code, web-based environment for building, testing, and deploying multi-agent workflows, making advanced AI orchestration accessible to a wide range of users.

---

## Architecture & Key Components

### 1. Web Application
- **Backend:** FastAPI-based API with modular routing (sessions, runs, teams, gallery, validation, settings, authentication, websocket, etc.).
- **Frontend:** Served as static files (UI directory).
- **WebSocket:** Real-time communication for run streaming and agent interaction.
- **Authentication:** Pluggable system supporting multiple providers (see `web/auth/`).

### 2. Database Layer
- **ORM:** SQLModel (built on SQLAlchemy and Pydantic) for type-safe models and queries.
- **Schema Management:** Alembic for migrations and versioning, managed by `SchemaManager`.
- **Manager:** `DatabaseManager` handles connections, CRUD, and schema upgrades.

### 3. Team Management
- **TeamManager:** Loads, creates, and runs agent teams from config files, directories, or dicts.
- **Streaming:** Supports streaming execution results and cancellation.
- **Environment:** Supports injecting environment variables for team runs.
- **Features:**
  - Load team configurations from JSON/YAML files or directories.
  - Create team instances from config dicts or `ComponentModel` objects.
  - Inject environment variables for team execution.
  - Assign custom input functions to user proxy agents for interactive workflows.
  - Run teams with streaming output via `run_stream`, yielding agent messages, events, and results in real time.
  - Supports cancellation tokens for interrupting long-running tasks.
  - Cleans up agent resources after execution.

#### Example Usage
```python
team_manager = TeamManager()
# Load from file
task = "Summarize the latest AI research."
team_config = "/path/to/team_config.json"
async for event in team_manager.run_stream(task=task, team_config=team_config):
    print(event)
```

### 4. Gallery System
- **GalleryBuilder:** Constructs galleries of reusable components (agents, models, tools, terminations, teams).
- **Default Gallery:** Includes OpenAI, Anthropic, Azure, Mistral models, Bing/Google search, calculator, code execution, and more.
- **Extensible:** Users can add custom components and metadata.

### 5. Evaluation System
- **EvalOrchestrator:** Manages evaluation tasks, criteria, and runs (with or without DB persistence).
- **Runners & Judges:** Supports custom evaluation runners and judges for agent/team performance.

### 6. Validation & Testing
- **ValidationService:** Validates component schemas and instantiation.
- **ComponentTestService:** Functional testing for agents, models, tools, teams, and terminations.

---

## Data Models
- **Team, Run, Message, Session, Gallery, Settings:** Core entities for workflow, history, and configuration.
- **GalleryConfig & GalleryComponents:** Structure for organizing and sharing component collections.
- **EnvironmentVariable:** For injecting runtime configuration.

---

## API Endpoints (Selected)
- `/api/sessions/` — Session management
- `/api/runs/` — Run execution and history
- `/api/teams/` — Team configuration
- `/api/gallery/` — Component gallery
- `/api/validate/` — Validation services
- `/api/settings/` — Application settings
- `/api/auth/` — Authentication
- `/api/ws/` — WebSocket endpoints
- `/api/version` — Version info
- `/api/health` — Health check

---

## CLI Usage
- Start the UI server:
  ```bash
  autogenstudio ui --host 127.0.0.1 --port 8081
  ```
- Options: `--appdir`, `--database-uri`, `--auth-config`, `--upgrade-database`, `--reload`, `--workers`, etc.

---

## Extensibility
- **Custom Tools:** Add new tools in `gallery/tools/`.
- **Agent Templates:** Create new agent/team templates.
- **Evaluation:** Implement custom runners/judges in `eval/`.
- **Authentication:** Add providers in `web/auth/providers.py`.

---

## Example: Creating a Team
```python
team_manager = TeamManager()
result = await team_manager.run_stream(
    task="Research quantum computing advances in 2023",
    team_config="/path/to/team_config.json"
)
```

---

## Default Gallery Components
- **Models:** OpenAI GPT-4o, Mistral, Anthropic Claude, Azure OpenAI, etc.
- **Tools:** Calculator, Bing/Google Search, Webpage Fetch, Image Generation, Python Code Execution.
- **Agents:** Assistant, Critic, Web Surfer, Verifier, Summary Agent, User Proxy.
- **Teams:** RoundRobin, Selector, Deep Research, Web Agent Team, etc.
- **Terminations:** Max messages, text mention, logical combinations.

---

## Configuration
- **Environment Variables:** `AUTOGENSTUDIO_DATABASE_URI`, `AUTOGENSTUDIO_APPDIR`, `AUTOGENSTUDIO_AUTH_CONFIG`, etc.
- **App Directory:** Defaults to `~/.autogenstudio/`.
- **Database:** SQLite by default, configurable.

---

## Deployment
- Production: Use a production-grade DB, configure authentication, set host/workers, use a reverse proxy.
- Development: Use `--reload` for hot-reload, enable API docs.

---

## Version
- Current version: 0.4.2 (as of May 14, 2025)

---

## References
- See source code for further details and extension points.

---

## Foundational Concepts for Leveraging AutoGen

When building with AutoGen and AutoGen Studio, keep these foundational concepts in mind:

### 1. Agent Abstraction
- **Agents** are the core building blocks. Each agent encapsulates a role, behavior, and memory, and can use LLMs, tools, or custom logic.
- Agents can be assistants, critics, verifiers, user proxies, or any custom role you define.

### 2. Team Composition
- **Teams** are collections of agents working together using a defined communication pattern (e.g., round-robin, selector, graph flow).
- Teams can be configured via JSON/YAML or Python dicts, and can be dynamically created or loaded from files.

### 3. Communication Patterns
- AutoGen supports multiple team communication patterns:
  - **Selector Group Chat:** A coordinator selects which agent should act next.
  - **Swarm:** Agents act in parallel or in a loosely coordinated fashion.
  - **GraphFlow:** Agents are connected in a directed graph, enabling workflow-like execution.

### 4. Tool Integration
- Agents can be equipped with tools (e.g., search, calculator, code execution) to extend their capabilities beyond LLM-only reasoning.
- Tools are modular and can be added or customized in the gallery.

### 5. Streaming and Interactivity
- Team execution is streamed in real time, allowing for interactive workflows and live feedback.
- User proxy agents can inject human input into the workflow at decision points.

### 6. Extensibility
- You can add new agents, tools, team templates, and evaluation strategies by extending the gallery and evaluation system.
- Custom judges and runners allow for domain-specific evaluation and orchestration.

### 7. Configuration and Environment
- Use environment variables and configuration files to manage API keys, database URIs, and other runtime settings.
- The app directory structure and database are configurable for different deployment scenarios.

### 8. Evaluation and Validation
- Leverage the evaluation system to benchmark agent/team performance using automated or human-in-the-loop judges.
- Use validation and testing services to ensure component correctness before deployment.

### 9. Serialization and Sharing
- Agents, teams, and tools can be serialized for reuse, sharing, or deployment across environments.
- Gallery components can be exported/imported as JSON for collaboration.

### 10. Observability and Debugging
- Built-in logging, tracing, and event streaming make it easy to debug workflows and monitor agent/team behavior.

By understanding and applying these concepts, you can design, build, and evaluate sophisticated multi-agent workflows tailored to your specific needs using AutoGen Studio.

---

### Agent Request Processing and Result Flow

When a request (task) is submitted to a team via the `TeamManager`, the following process occurs:

1. **Team Creation:**
   - The `TeamManager` loads the team configuration (from file, dict, or `ComponentModel`) and instantiates the team, which is typically a group chat or workflow of agents.
   - Environment variables and custom input functions can be injected at this stage.

2. **Task Dispatch:**
   - The task (a string or message sequence) is passed to the team's `run_stream` method.
   - The team orchestrates the flow of messages between agents according to the specified pattern (e.g., round-robin, selector, graph flow).

3. **Agent Processing:**
   - Each agent receives messages, processes them (using LLMs, tools, or custom logic), and generates responses or actions.
   - Agents may call external tools (e.g., search, calculator) or interact with other agents as part of their reasoning.
   - The system supports both event-driven and request/response communication between agents.

4. **Streaming Results:**
   - As agents produce messages, events, or results, these are yielded in real time via the async generator returned by `run_stream`.
   - Consumers (e.g., the web UI or API clients) can display agent responses, intermediate events, and final results as they arrive.
   - The process supports cancellation tokens, allowing long-running or stuck tasks to be interrupted gracefully.

5. **Completion and Cleanup:**
   - When a termination condition is met (e.g., max messages, specific text, or logical combination), the team run ends.
   - Resources for all agents are cleaned up, and the final result is returned as a `TeamResult` object.

#### Example Flow
```python
async for event in team_manager.run_stream(task="Write a summary of the latest AI news", team_config=team_config):
    if isinstance(event, TeamResult):
        print("Final result:", event.task_result)
    else:
        print("Agent/Event:", event)
```

---

### More on the Evaluation Orchestrator

The `EvalOrchestrator` is responsible for managing the evaluation lifecycle of agent teams and their outputs. It provides a flexible and extensible framework for both automated and human-in-the-loop evaluation workflows. Key features include:

- **Task Management:**
  - Create, retrieve, and list evaluation tasks, which define what is to be evaluated (e.g., factual accuracy, helpfulness, completeness).
  - Tasks can be persisted in the database or managed in-memory.

- **Criteria Management:**
  - Define and manage evaluation criteria (e.g., scoring rubrics, qualitative feedback prompts).
  - Criteria can be reused across multiple evaluation runs.

- **Run Management:**
  - Launch evaluation runs that associate a task, runner (the agent/team to be evaluated), judge (the evaluator, which can be an LLM or human), and criteria.
  - Each run tracks its status, configuration, and results.
  - Supports both synchronous and asynchronous execution.

- **Judges and Runners:**
  - Judges can be LLM-based, rule-based, or human evaluators.
  - Runners are the agent teams or workflows being evaluated.
  - The orchestrator coordinates the interaction between runners and judges, collecting scores, feedback, and other metrics.

- **Persistence and Reporting:**
  - Results, scores, and feedback can be stored in the database for later analysis.
  - Supports querying and exporting evaluation results for reporting and comparison.

- **Extensibility:**
  - Users can implement custom runners, judges, and criteria to tailor the evaluation process to specific needs.
  - The orchestrator is designed to be modular, making it easy to plug in new evaluation strategies or integrate with external systems.

#### Example Usage
```python
orchestrator = EvalOrchestrator(db_manager)
task_id = await orchestrator.create_task(EvalTask(...))
criteria_id = await orchestrator.create_criteria(EvalJudgeCriteria(...))
run_id = await orchestrator.create_run(
    task=task_id,
    runner=team_runner,
    judge=llm_judge,
    criteria=[criteria_id],
    name="Team Evaluation Run"
)
```

#### More on Judges

Judges in AutoGen Studio are responsible for evaluating the outputs of agent teams according to specified criteria. The orchestrator supports different types of judges, each suited for various evaluation scenarios:

- **LLM-Based Judges:**
  - Use large language models (such as OpenAI GPT or Anthropic Claude) to automatically assess agent/team outputs.
  - Can be configured with custom prompts, scoring rubrics, and feedback instructions.
  - Useful for automated, scalable, and consistent evaluation of natural language outputs.

- **Rule-Based Judges:**
  - Apply deterministic rules or logic to evaluate outputs (e.g., checking for the presence of required keywords, format compliance, or logical correctness).
  - Suitable for tasks with clear, objective criteria.

- **Human Judges:**
  - Allow human evaluators to review, score, and provide feedback on agent/team outputs via the UI or API.
  - Enable human-in-the-loop workflows for subjective or complex evaluation tasks.

- **Custom Judges:**
  - Users can implement their own judge classes to support domain-specific evaluation logic, integrate with external systems, or combine multiple evaluation strategies.

Judges interact with runners (the agent teams or workflows being evaluated) and criteria (the evaluation metrics or rubrics). The orchestrator coordinates the evaluation process, collects scores and feedback from judges, and stores the results for analysis and reporting.

Judges can be reused across multiple evaluation runs and can be extended to support new evaluation paradigms as needed.
