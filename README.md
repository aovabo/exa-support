# Exa Support Engineer Demo

## Why You Should Hire Me

I built a real support platform that uses the Exa API, modern AI tools, and a clean user interface. I can:
- Build and ship real AI support tools
- Integrate APIs like Exa for search and knowledge
- Make user-friendly, beautiful UIs
- Write clear code and documentation
- Understand customer needs and technical details

## What This App Does

This is an AI-powered support platform for Exa. It helps users get answers about Exa products, troubleshoot issues, and find documentation. The app can:
- Answer questions about Exa and its API
- Help with setup, pricing, and integration
- Search Exa docs and the web for up-to-date info
- Show example questions and metrics
- Let users export chat history

## How It Works

- The app uses the **Exa API** to search Exa documentation and the web. This means answers are always current and relevant.
- It uses **Streamlit** for the web UI. The interface is modern, dark-themed, and easy to use.
- The AI agent is built with **Agno**, which lets it use tools like Exa, DuckDuckGo, and more.
- All chat history and knowledge are stored in a **Postgres** database with vector search for fast lookups.
- The app can also connect to Discord and other sources if needed.

## How We Use the Exa API

- The agent uses Exa's `/search` endpoint to find the best docs and web pages for any question.
- It can use `/contents` to pull in the actual content from those pages.
- It can use `/findsimilar` to suggest related resources.
- The knowledge base is built by crawling Exa docs and loading them into a vector database. This makes the agent smart about Exa.
- All API calls are handled securely and efficiently.

## Tech Stack

- **Python** for all backend and agent logic
- **Streamlit** for the UI
- **Agno** for agent framework and tool integration
- **Exa API** for search and knowledge
- **Postgres** and **PgVector** for storage and fast search
- **Docker** for easy local development

## Why This Matters

- Shows I can build real, useful support tools
- Proves I can work with Exa's API and docs
- Demonstrates good UI/UX and technical writing
- Ready to help Exa customers and improve support

## How to Run

1. Clone the repo
2. Set your `OPENAI_API_KEY` and `EXA_API_KEY` in a `.env` file
3. Run `streamlit run ui/pages/Exa_Support.py`
4. Try asking questions or using the example buttons

---

If you want a support engineer who can build, explain, and support Exa products, I am the right choice. This project is proof.
