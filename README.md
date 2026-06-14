# AutoDoc

AutoDoc is an AI-powered code review system that automatically reviews GitHub commits, generates improvements using a local LLM, and raises GitHub Pull Requests containing the suggested changes.

The project is intentionally built using deterministic distributed-system patterns (webhooks, queues, workers, events) rather than a purely agentic architecture in order to learn and demonstrate production-grade backend engineering concepts.

---

# Features

* GitHub Push Webhook Integration
* Redis-backed Event Queues
* Asynchronous Review Workers
* Local LLM Integration via Ollama
* Git Worktree Isolation
* Automated Code Improvements
* Automated Branch Creation
* Automated Pull Request Creation
* Multi-Repository Support

---

# Architecture

```text
GitHub Push
    ↓
Webhook API
    ↓
Redis Queue
    ↓
Review Worker
    ↓
Ollama LLM
    ↓
Git Commit
    ↓
PR Queue
    ↓
PR Worker
    ↓
GitHub Pull Request
```

---

# System Requirements

## Minimum

* Apple Silicon Mac (M1/M2/M3)
* 16 GB RAM
* 20 GB free disk space

## Recommended

* Apple Silicon Mac (M2 Pro / M3 Pro or higher)
* 32 GB RAM

Local LLMs can consume significant memory depending on the model used.

---

# Prerequisites

## Homebrew

Install:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Verify:

```bash
brew --version
```

---

## Python

Install:

```bash
brew install python
```

Verify:

```bash
python3 --version
```

---

## uv

Install:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify:

```bash
uv --version
```

---

## Git

Verify:

```bash
git --version
```

---

## Docker Desktop

Install Docker Desktop and ensure Docker is running.

Verify:

```bash
docker ps
```

---

## Ollama

Install:

```bash
brew install ollama
```

Verify:

```bash
ollama --version
```

Download the default model:

```bash
ollama pull qwen3:14b
```

---

## ngrok

Install:

```bash
brew install ngrok/ngrok/ngrok
```

Authenticate:

```bash
ngrok config add-authtoken <your-token>
```

---

## iTerm2 (Recommended)

AutoDoc includes scripts that automatically launch all services in dedicated tabs.

Install:

```bash
brew install --cask iterm2
```

Recommended Profiles:

* Redis
* Ollama
* API
* Workers
* Ngrok

Optional customizations:

* Unique colors per profile
* Custom tab titles
* Profile badges

Useful shortcuts:

| Action           | Shortcut        |
| ---------------- | --------------- |
| Next Tab         | Cmd + Shift + ] |
| Previous Tab     | Cmd + Shift + [ |
| Vertical Split   | Cmd + D         |
| Horizontal Split | Cmd + Shift + D |
| Search Logs      | Cmd + F         |

---

# Clone Repository

```bash
git clone git@github.com:spar2522/ai_autodoc.git

cd ai_autodoc
```

---

# Environment Variables

Create:

```text
.env
```

Example:

```env
GITHUB_TOKEN=<github_pat_xxxxx>

REDIS_HOST=localhost
REDIS_PORT=6380
REDIS_DB=0
```

---

# Install Dependencies

```bash
uv sync
```

---

# Start Redis

```bash
docker compose up -d
```

Verify:

```bash
docker ps
```

Expected container:

```text
autodoc-redis
```

---

# Start Development Environment

```bash
./scripts/start_dev.sh
```

This launches:

* Redis
* Ollama
* API
* Workers
* ngrok

in dedicated iTerm tabs.

---

# Configure GitHub

## Personal Access Token

Create a Fine-Grained Personal Access Token.

Required permissions:

* Pull Requests
* Contents
* Metadata

Store the token inside:

```text
.env
```

---

## SSH Authentication

Verify:

```bash
ssh -T git@github.com
```

Expected:

```text
Hi <username>! You've successfully authenticated...
```

---

# Configure GitHub Webhook

Start AutoDoc.

Copy the ngrok URL.

Example:

```text
https://example.ngrok-free.app
```

Configure GitHub:

```text
Repository
→ Settings
→ Webhooks
→ Add Webhook
```

Payload URL:

```text
https://example.ngrok-free.app/github/webhook
```

Content Type:

```text
application/json
```

Events:

```text
Push Events
```

---

# Register Repositories

Edit:

```text
configs/registered_configs.yaml
```

Example:

```yaml
repos:

  - github_repo: spar2522/ai-backend
    local_path: /Users/username/ai-lab/ai-backend

  - github_repo: spar2522/ai_autodoc
    local_path: /Users/username/ai-lab/ai_autodoc

model: qwen3:14b

worktree_root: /Users/username/ai-worktrees
```

---

# Development Workflow

1. Push code to GitHub.
2. GitHub sends a webhook.
3. AutoDoc receives the event.
4. Review Worker generates improvements.
5. Changes are committed to a review branch.
6. PR Worker pushes the branch.
7. GitHub Pull Request is created.

---

# Supported File Types

Current:

* Python
* Markdown
* YAML

Planned:

* JavaScript
* TypeScript
* Java
* Go

---

# Troubleshooting

## Ollama Not Running

Verify:

```bash
curl http://localhost:11434/api/tags
```

---

## Redis Connection Errors

Verify:

```bash
docker ps
```

and ensure:

```text
autodoc-redis
```

is running.

---

## GitHub Authentication Errors

Verify:

```bash
ssh -T git@github.com
```

---

## ngrok Not Reachable

Verify:

```bash
http://localhost:9000/docs
```

works before starting ngrok.

---

# Roadmap

* Multi-file dependency analysis
* Review comments on existing PRs
* Agent-based orchestration
* LangGraph integration
* MCP tool integration
* GitHub App authentication
* Cloud deployment
* Human approval workflows
* Multi-model support

---

# Design Philosophy

This project intentionally emphasizes:

* Event-driven architecture
* Distributed systems concepts
* Deterministic workflows
* Queue-based processing
* Observable execution

before introducing autonomous agent orchestration.

The goal is to understand how modern AI systems are built on top of reliable backend infrastructure rather than replacing it.
