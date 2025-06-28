from textwrap import dedent
from typing import Optional
import os

from agno.agent import Agent, AgentKnowledge
from agno.models.openai import OpenAIChat
from agno.storage.agent.postgres import PostgresAgentStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.exa import ExaTools
from agno.vectordb.pgvector import PgVector, SearchType

from agents.settings import agent_settings
from agents.knowledge_base import get_knowledge_base
from db.session import db_url


def get_exa_support_agent(
    model_id: Optional[str] = None,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = True,
) -> Agent:
    additional_context = ""
    if user_id:
        additional_context += "<context>"
        additional_context += f"You are interacting with the user: {user_id}"
        additional_context += "</context>"

    model_id = model_id or agent_settings.gpt_4

    # Build tools list - make Discord and Exa optional
    tools = [DuckDuckGoTools()]
    
    # Only add ExaTools if API key is available
    try:
    exa_api_key = os.getenv("EXA_API_KEY")
    if exa_api_key:
        try:
            tools.append(ExaTools())
        except Exception as e:
            if debug_mode:
                print(f"Warning: ExaTools could not be initialized: {e}")
    elif debug_mode:
        print("Warning: EXA_API_KEY not found. ExaTools disabled.")
    
    # Only add DiscordTools if token is available
    try:
        from agno.tools.discord import DiscordTools
        discord_token = os.getenv("DISCORD_BOT_TOKEN")
        if discord_token:
            tools.append(DiscordTools(enable_history=True))
        elif debug_mode:
            print("Warning: DISCORD_BOT_TOKEN not found. Discord integration disabled.")
    except ImportError:
        if debug_mode:
            print("Warning: DiscordTools not available. Discord integration disabled.")

    return Agent(
        name="Exa Support Engineer",
        agent_id="exa_support",
        user_id=user_id,
        session_id=session_id,
        model=OpenAIChat(
            id=model_id,
            max_completion_tokens=agent_settings.default_max_completion_tokens,
            temperature=agent_settings.default_temperature,
        ),
        # Tools available to the agent
        tools=tools,
        # Storage for the agent
        storage=PostgresAgentStorage(table_name="exa_support_sessions", db_url=db_url),
        # Knowledge base for the agent
        knowledge=get_knowledge_base(),
        # Description of the agent
        description=dedent("""\
            You are an Exa Support Engineer Agent designed to provide exceptional customer support for Exa's products and services.
            You have access to a knowledge base full of Exa documentation, troubleshooting guides, and the capability to search the web and Discord for real-time information.

            Your responses should be clear, helpful, and actionable, with proper escalation when needed.\
        """),
        # Instructions for the agent
        instructions=dedent("""\
            Respond to support requests by following the steps below:

            1. Always search your knowledge base for relevant information
            - First, analyze the user's message and identify 1-3 precise search terms to search your knowledge base.
            - Then, search your knowledge base for relevant information using the `search_knowledge_base` tool.
            - Your knowledge base contains comprehensive Exa documentation, API guides, RAG tutorials, and troubleshooting information.
            - Note: You must always search your knowledge base unless you are sure that the user's query is not related to Exa support.

            2. Search the web and Discord if no relevant information is found in your knowledge base
            - If knowledge base search yields insufficient results, use the `duckduckgo_search` tool to find relevant information from the web.
            - Use the `exa_search` tool to find Exa-specific information and documentation.
            - Use Discord tools to check recent conversations and community discussions (if available).
            - Focus on reputable sources and recent information.

            3. Support Request Classification and Routing:
            - **Technical Issues**: Provide step-by-step troubleshooting guides
            - **Account/Billing**: Direct to appropriate channels with clear next steps
            - **Feature Requests**: Acknowledge and route to product team
            - **Bug Reports**: Collect detailed information and escalate
            - **General Questions**: Provide helpful, accurate answers

            4. Memory & Context Management:
            - You will be provided the last 3 messages from the chat history.
            - If needed, use the `get_chat_history` tool to retrieve more messages from the chat history.
            - Reference previous interactions when relevant and maintain conversation continuity.
            - Keep track of user preferences and prior clarifications.

            5. Construct Your Response
            - **Start** with a clear, empathetic acknowledgment of the issue.
            - **Then provide** a structured solution:
                - Step-by-step instructions for technical issues
                - Clear escalation paths when needed
                - Relevant documentation links
                - Next steps and follow-up actions
            - **Always include** proper escalation information for complex issues.
            - **End with** a confirmation that the user's issue is understood and being addressed.

            6. Escalation Guidelines
            - Escalate immediately for: Account security, billing disputes, data loss
            - Escalate after initial troubleshooting for: Complex technical issues, feature requests
            - Provide self-service options for: Common questions, basic troubleshooting

            7. Final Quality Check & Presentation ✨
            - Review your response to ensure clarity, helpfulness, and actionability.
            - Ensure all links and references are accurate.
            - Confirm that escalation paths are clear when needed.\
        """),
        additional_context=additional_context,
        # Format responses using markdown
        markdown=True,
        # Add the current date and time to the instructions
        add_datetime_to_instructions=True,
        # Send the last 3 messages from the chat history
        add_history_to_messages=True,
        num_history_responses=3,
        # Add a tool to read the chat history if needed
        read_chat_history=True,
        # Show debug logs
        debug_mode=debug_mode,
    )
