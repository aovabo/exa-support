# Exa Support Platform

This repository contains an AI-powered customer support system built with **agno** that provides exceptional customer service for Exa products and services.

## 🎯 Project Overview

This platform demonstrates the skills needed for Exa's Support Engineer role:
- **Technical Troubleshooting** - Step-by-step problem resolution
- **Customer Communication** - Clear, empathetic support responses  
- **Issue Classification** - Intelligent routing and escalation
- **Knowledge Management** - Building comprehensive support resources
- **Automation** - Reducing manual support workload

## 🚀 Features

### 🤖 AI Support Agent
- **ExaTools Integration** - Uses Exa's own search and content tools
- **Discord Integration** - Monitor and respond to community discussions
- **Knowledge Base** - Access to Exa documentation and troubleshooting guides
- **Multi-Source Search** - Web search and real-time information gathering
- **Issue Classification** - Intelligent routing and escalation

### 🔍 Support Scenarios
- **Authentication Issues** - API key problems and authentication errors
- **Search Optimization** - Exa search strategies and best practices
- **Billing & Pricing** - Pricing plans and billing questions
- **Integration Support** - Step-by-step developer guidance
- **Bug Reports** - Detailed information collection and routing
- **Feature Requests** - Acknowledgment and product team routing

## 🛠️ Built With

- **agno** - AI agent development framework
- **ExaTools** - Exa's own search and content tools
- **DiscordTools** - Community monitoring and engagement
- **Streamlit** - Beautiful, interactive web interface
- **PostgreSQL** - Reliable data storage and session management

## 📚 Knowledge Base

The system includes a comprehensive knowledge base with:
- **Exa API Documentation** - Complete API reference and guides
- **Troubleshooting Guides** - Common issues and solutions
- **Integration Examples** - Code samples and implementation guides
- **Best Practices** - Optimization and usage recommendations
- **Community Knowledge** - Discord conversations and user experiences

## 🚀 Setup

1. [Install uv](https://docs.astral.sh/uv/#getting-started) for managing the python environment.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create a virtual environment and install dependencies:

```sh
./scripts/dev_setup.sh
```

3. Activate virtual environment

```
source .venv/bin/activate
```

## 🏃‍♂️ Run application locally using docker

1. Install [docker desktop](https://www.docker.com/products/docker-desktop)

2. Export API keys

Required: Set the `OPENAI_API_KEY` and `EXA_API_KEY` environment variables:

```sh
export OPENAI_API_KEY=***
export EXA_API_KEY=***
```

3. Start the workspace:

```sh
ag ws up
```

- This will run 3 containers:
  - Streamlit on [localhost:8501](http://localhost:8501)
  - FastAPI on [localhost:8000](http://localhost:8000/docs)
  - Postgres on [localhost:5432](http://localhost:5432)
- Open [localhost:8501](http://localhost:8501) to view the Exa Support Platform
- Open [localhost:8000/docs](http://localhost:8000/docs) to view the FastAPI docs

4. Stop the workspace using:

```sh
ag ws down
```

## 🎯 Perfect for Support Engineers

This project showcases:
- **Agent Development** - Building intelligent AI systems with agno
- **Tool Integration** - Using Exa's own products to solve problems
- **Customer Support Automation** - Reducing manual workload
- **Knowledge Management** - Building and maintaining support resources
- **Technical Problem Solving** - Step-by-step troubleshooting automation

## 📖 More Information

Learn more about this application and how to customize it in the [Agno Workspaces](https://docs.agno.com/workspaces) documentation.
