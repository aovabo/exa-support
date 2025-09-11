from typing import Any, Callable, Dict, List, Optional, Union

import streamlit as st
from agno.agent import Agent
from agno.document import Document
from agno.document.reader import Reader
from agno.document.reader.csv_reader import CSVReader
from agno.document.reader.docx_reader import DocxReader
from agno.document.reader.pdf_reader import PDFReader
from agno.document.reader.text_reader import TextReader
from agno.document.reader.website_reader import WebsiteReader
from agno.utils.log import logger


async def initialize_agent_session_state(agent_name: str):
    logger.info(f"---*--- Initializing session state for {agent_name} ---*---")
    st.session_state[agent_name] = {
        "agent": None,
        "session_id": None,
        "messages": [],
    }


async def initialize_team_session_state(team_name: str):
    logger.info(f"---*--- Initializing session state for {team_name} ---*---")
    st.session_state[team_name] = {
        "team": None,
        "session_id": None,
        "messages": [],
    }


async def initialize_workflow_session_state(workflow_name: str):
    logger.info(f"---*--- Initializing session state for {workflow_name} ---*---")
    st.session_state[workflow_name] = {
        "workflow": None,
        "session_id": None,
        "messages": [],
    }


async def selected_model() -> str:
    """Display a model selector in the sidebar."""
    st.markdown("#### 🤖 AI Model")
    
    model_options = {
        "gpt-4o": "GPT-4o (Recommended)",
        "gpt-4o-mini": "GPT-4o Mini (Fast)",
    }
    
    selected_model = st.selectbox(
        "Choose AI Model",
        options=list(model_options.keys()),
        index=0,
        key="model_selector",
        help="Select the AI model for the support agent"
    )
    
    # Show model info
    if selected_model == "gpt-4o":
        st.info("**GPT-4o**: Best performance, comprehensive responses")
    else:
        st.info("**GPT-4o Mini**: Faster responses, good for simple queries")
    
    return selected_model  # Return the actual model ID, not the descriptive text


async def add_message(
    agent_name: str,
    role: str,
    content: str,
    tool_calls: Optional[List[Dict[str, Any]]] = None,
) -> None:
    """Safely add a message to the Agent's session state."""
    # if role == "user":
    #     logger.info(f"👤  {role} → {agent_name}: {content}")
    # else:
    #     logger.info(f"🤖  {agent_name} → user: {content}")
    st.session_state[agent_name]["messages"].append({"role": role, "content": content, "tool_calls": tool_calls})


def display_tool_calls(tool_calls_container, tools):
    """Display tool calls in a streamlit container with expandable sections.

    Args:
        tool_calls_container: Streamlit container to display the tool calls
        tools: List of tool call dictionaries containing name, args, content, and metrics
    """
    if not tools:
        return

    try:
        with tool_calls_container.container():
            for tool_call in tools:
                if hasattr(tool_call, 'tool_name'):
                    # Handle object with attributes
                    tool_name = tool_call.tool_name
                    tool_args = tool_call.tool_args
                    content = tool_call.result if hasattr(tool_call, 'result') else None
                    metrics = getattr(tool_call, "metrics", None)
                else:
                    # Handle dictionary
                    tool_name = tool_call.get("tool_name", "Unknown Tool")
                    tool_args = tool_call.get("tool_args", {})
                    content = tool_call.get("content")
                    metrics = tool_call.get("metrics", {})

                # Add timing information
                execution_time_str = "N/A"
                try:
                    if metrics:
                        execution_time = metrics.time
                        if execution_time is not None:
                            execution_time_str = f"{execution_time:.2f}s"
                except Exception as e:
                    logger.error(f"Error displaying tool calls: {str(e)}")
                    pass

                # Use custom CSS classes for better styling
                st.markdown(
                    f"""
                    <div class="tool-call">
                        <div class="tool-name">🛠️ {tool_name.replace('_', ' ').title() if tool_name else 'Tool'} ({execution_time_str})</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Show query with syntax highlighting
                if isinstance(tool_args, dict) and tool_args.get("query"):
                    st.code(tool_args["query"], language="sql")

                # Display arguments in a more readable format
                if tool_args and tool_args != {"query": None}:
                    st.markdown("**Arguments:**")
                    st.json(tool_args)

                if content:
                    st.markdown("**Results:**")
                    try:
                        # Check if content is already a dictionary or can be parsed as JSON
                        if isinstance(content, dict) or (
                            isinstance(content, str) and content.strip().startswith(("{", "["))
                        ):
                            st.json(content)
                        else:
                            # If not JSON, show as markdown
                            st.markdown(content)
                    except Exception:
                        # If JSON display fails, show as markdown
                        st.markdown(content)
    except Exception as e:
        logger.error(f"Error displaying tool calls: {str(e)}")
        tool_calls_container.error(f"Failed to display tool results: {str(e)}")


async def example_inputs(agent_name: str) -> None:
    """Show example inputs for an Agent."""
    st.markdown("#### 💡 Try these examples:")
    
    # Agent-specific examples
    if agent_name == "exa_support":
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 How do I use Exa search?", key="exa_search_example"):
                await add_message(
                    agent_name,
                    "user",
                    "How do I use Exa search? I'm trying to find information about a topic.",
                )
            if st.button("🔑 My API key isn't working", key="api_key_example"):
                await add_message(
                    agent_name,
                    "user",
                    "My API key isn't working. I'm getting authentication errors.",
                )
        
        with col2:
            if st.button("💰 What are Exa's pricing plans?", key="pricing_example"):
                await add_message(
                    agent_name,
                    "user",
                    "What are Exa's pricing plans? I need to understand the costs.",
                )
            if st.button("🔧 How do I integrate Exa?", key="integration_example"):
                await add_message(
                    agent_name,
                    "user",
                    "How do I integrate Exa with my application? I need step-by-step instructions.",
                )
        
        # Additional examples
        col3, col4 = st.columns(2)
        
        with col3:
            if st.button("📚 Show me RAG examples", key="rag_example"):
                await add_message(
                    agent_name,
                    "user",
                    "Can you show me examples of how to use Exa for RAG applications?",
                )
            if st.button("🚀 What's new in Exa?", key="new_features_example"):
                await add_message(
                    agent_name,
                    "user",
                    "What are the latest features and updates in Exa?",
                )
        
        with col4:
            if st.button("⚡ Performance optimization", key="performance_example"):
                await add_message(
                    agent_name,
                    "user",
                    "How can I optimize the performance of my Exa searches?",
                )
            if st.button("🛡️ Security best practices", key="security_example"):
                await add_message(
                    agent_name,
                    "user",
                    "What are the security best practices when using Exa?",
                )
    elif agent_name == "sage":
        if st.button("Tell me about Agno"):
            await add_message(
                agent_name,
                "user",
                "Tell me about Agno. Github repo: https://github.com/agno-agi/agno. Documentation: https://docs.agno.com",
            )
    elif agent_name == "scholar":
        if st.button("Tell me about the US tariffs"):
            await add_message(
                agent_name,
                "user",
                "Tell me about the US tariffs",
            )


async def knowledge_widget(agent_name: str, agent: Agent) -> None:
    """Display a knowledge widget in the sidebar."""
    st.markdown("#### 📚 Knowledge Base")
    
    if not agent.knowledge:
        st.info("No knowledge base configured for this agent.")
        return

    # Knowledge base info
    knowledge_type = type(agent.knowledge).__name__
    st.markdown(f"**Type:** {knowledge_type}")
    
    if hasattr(agent.knowledge, 'vector_db'):
        vector_db_type = type(agent.knowledge.vector_db).__name__
        st.markdown(f"**Vector DB:** {vector_db_type}")
    
    # Search functionality
    st.markdown("#### 🔍 Search Knowledge")
    search_query = st.text_input(
        "Search knowledge base",
        placeholder="Enter search terms...",
        key="knowledge_search"
    )
    
    if search_query and st.button("Search", key="search_knowledge_btn"):
        try:
            # Perform search
            results = agent.knowledge.search(search_query, num_results=3)
            
            if results:
                st.markdown("#### 📖 Search Results")
                for i, result in enumerate(results, 1):
                    with st.expander(f"Result {i}: {result.metadata.get('title', 'No title')}", expanded=False):
                        st.markdown(f"**Source:** {result.metadata.get('source', 'Unknown')}")
                        st.markdown(f"**Content:** {result.content[:200]}...")
            else:
                st.info("No results found.")
        except Exception as e:
            st.error(f"Search failed: {str(e)}")
    
    # Knowledge base management
    st.markdown("#### ⚙️ Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Refresh", key="refresh_knowledge_btn"):
            st.info("Knowledge base refresh initiated...")
            # This would typically trigger a refresh of the knowledge base
    
    with col2:
        if st.button("📊 Stats", key="knowledge_stats_btn"):
            st.info("Knowledge base statistics:")
            st.markdown("• Documents: Loading...")
            st.markdown("• Index size: Loading...")
            st.markdown("• Last updated: Loading...")


async def session_selector(agent_name: str, agent: Agent, get_agent: Callable, user_id: str, model_id: str) -> None:
    """Display a session selector in the sidebar, if a new session is selected, the agent is restarted with the new session."""

    if not agent.storage:
        return

    try:
        # Get all agent sessions.
        agent_sessions = agent.storage.get_all_sessions()
        if not agent_sessions:
            st.info("No saved sessions found.")
            return

        # Get session names if available, otherwise use IDs.
        sessions_list = []
        for session in agent_sessions:
            session_id = session.session_id
            session_name = session.session_data.get("session_name", None) if session.session_data else None
            display_name = session_name if session_name else session_id
            sessions_list.append({"id": session_id, "display_name": display_name})

        # Display session selector.
        st.markdown("#### 💬 Session Management")
        
        # Current session info
        current_session = st.session_state[agent_name]["session_id"]
        if current_session:
            st.markdown(f"**Current:** {current_session[:8]}...")
        else:
            st.markdown("**Current:** New Session")
        
        # Session selector
        selected_session = st.selectbox(
            "Load Session",
            options=[s["display_name"] for s in sessions_list],
            key="session_selector",
            help="Select a saved session to load"
        )
        
        # Find the selected session ID.
        selected_session_id = next(s["id"] for s in sessions_list if s["display_name"] == selected_session)
        
        # Update the agent session if it has changed.
        if st.session_state[agent_name]["session_id"] != selected_session_id:
            if st.button("Load Session", key="load_session_btn"):
                logger.info(f"---*--- Loading {agent_name} session: {selected_session_id} ---*---")
                st.session_state[agent_name]["agent"] = get_agent(
                    user_id=user_id,
                    model_id=model_id,
                    session_id=selected_session_id,
                )
                st.rerun()

        # Show the rename session widget.
        st.markdown("#### ✏️ Rename Session")
        
        # Initialize session_edit_mode if needed.
        if "session_edit_mode" not in st.session_state:
            st.session_state.session_edit_mode = False

        # Show the session name.
        if st.session_state.session_edit_mode:
            new_session_name = st.text_input(
                "New Session Name",
                value=agent.session_name,
                key="session_name_input",
                help="Enter a new name for the current session"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✓ Save", key="save_session_name", type="primary"):
                    if new_session_name:
                        agent.rename_session(new_session_name)
                        st.session_state.session_edit_mode = False
                        st.success("Session renamed!")
                        # Trigger a rerun to refresh the sessions list
                        st.rerun()
            
            with col2:
                if st.button("✗ Cancel", key="cancel_session_edit"):
                    st.session_state.session_edit_mode = False
                    st.rerun()
        else:
            st.markdown(f"**Session Name:** {agent.session_name}")
            if st.button("✎ Rename", key="edit_session_name"):
                st.session_state.session_edit_mode = True
                st.rerun()
                
    except Exception as e:
        logger.error(f"Error in session selector: {str(e)}")
        st.error("Failed to load sessions")


def export_chat_history(agent_name: str):
    """Export chat history in markdown format.

    Returns:
        str: Formatted markdown string of the chat history
    """
    if "messages" not in st.session_state[agent_name] or not st.session_state[agent_name]["messages"]:
        return f"# {agent_name} - Chat History\n\nNo messages to export."

    chat_text = f"# {agent_name} - Chat History\n\n"
    for msg in st.session_state[agent_name]["messages"]:
        role_label = "🤖 Assistant" if msg["role"] == "assistant" else "👤 User"
        chat_text += f"### {role_label}\n{msg['content']}\n\n"

        # Include tool calls if present
        if msg.get("tool_calls"):
            chat_text += "#### Tool Calls:\n"
            for i, tool_call in enumerate(msg["tool_calls"]):
                if hasattr(tool_call, 'tool_name'):
                    tool_name = tool_call.tool_name
                    chat_text += f"**{i + 1}. {tool_name}**\n\n"
                    if tool_call.tool_args is not None:
                        chat_text += f"Arguments: ```json\n{tool_call.tool_args}\n```\n\n"
                    if tool_call.result is not None:
                        chat_text += f"Results: ```\n{tool_call.result}\n```\n\n"
                else:
                    tool_name = tool_call.get("name", "Unknown Tool")
                    chat_text += f"**{i + 1}. {tool_name}**\n\n"
                    if "arguments" in tool_call:
                        chat_text += f"Arguments: ```json\n{tool_call['arguments']}\n```\n\n"
                    if "content" in tool_call:
                        chat_text += f"Results: ```\n{tool_call['content']}\n```\n\n"

    return chat_text


async def utilities_widget(agent_name: str, agent: Agent) -> None:
    """Display a utilities widget in the sidebar."""
    st.markdown("#### 🛠️ Utilities")
    
    # Create a container for utilities
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 New Chat", key="new_chat_btn"):
                restart_agent(agent_name)
        
        with col2:
            fn = f"{agent_name}_chat_history.md"
            if "session_id" in st.session_state[agent_name]:
                fn = f"{agent_name}_{st.session_state[agent_name]['session_id']}.md"
            
            if st.download_button(
                "📥 Export Chat",
                export_chat_history(agent_name),
                file_name=fn,
                mime="text/markdown",
                key="export_chat_btn"
            ):
                st.success("✅ Chat history exported!")
    
    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Show agent info
    st.markdown("#### ℹ️ Agent Info")
    st.markdown(f"**Name:** {agent.name}")
    st.markdown(f"**ID:** {agent.agent_id}")
    if agent.session_id:
        st.markdown(f"**Session:** {agent.session_id[:8]}...")
    else:
        st.markdown("**Session:** New")
    
    # Show tools info
    st.markdown("#### 🔧 Available Tools")
    for tool in agent.tools:
        tool_name = getattr(tool, 'name', type(tool).__name__)
        st.markdown(f"• {tool_name}")


def restart_agent(agent_name: str):
    logger.debug("---*--- Restarting Agent ---*---")
    st.session_state[agent_name]["agent"] = None
    st.session_state[agent_name]["session_id"] = None
    st.session_state[agent_name]["messages"] = []
    if "url_scrape_key" in st.session_state[agent_name]:
        st.session_state[agent_name]["url_scrape_key"] += 1
    if "file_uploader_key" in st.session_state[agent_name]:
        st.session_state[agent_name]["file_uploader_key"] += 1
    st.rerun()


async def about_agno():
    """Show information about Agno in the sidebar"""
    with st.sidebar:
        st.markdown("### About Agno ✨")
        st.markdown("""
        Agno is an open-source library for building Multimodal Agents.

        [GitHub](https://github.com/agno-agi/agno) | [Docs](https://docs.agno.com)
        """)

        st.markdown("### Need Help?")
        st.markdown(
            "If you have any questions, catch us on [discord](https://agno.link/discord) or post in the community [forum](https://agno.link/community)."
        )


async def footer():
    st.markdown("---")
    st.markdown(
        "<p style='text-align: right; color: gray;'>Built using <a href='https://github.com/agno-agi/agno'>Agno</a></p>",
        unsafe_allow_html=True,
    )
