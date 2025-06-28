import asyncio

import nest_asyncio
import streamlit as st
from agno.agent import Agent
from agno.memory.agent import AgentRun
from agno.tools.streamlit.components import check_password
from agno.utils.log import logger
from dotenv import load_dotenv

from agents.exa_support import get_exa_support_agent
from ui.css import CUSTOM_CSS
from ui.utils import (
    about_agno,
    add_message,
    display_tool_calls,
    example_inputs,
    initialize_agent_session_state,
    knowledge_widget,
    selected_model,
    session_selector,
    utilities_widget,
)

load_dotenv()

nest_asyncio.apply()

st.set_page_config(
    page_title="Exa Support Engineer",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
agent_name = "exa_support"


async def header():
    st.markdown("<h1 class='heading'>Exa Support Engineer</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='subheading'>An AI-powered support agent that provides exceptional customer service for Exa products and services.</p>",
        unsafe_allow_html=True,
    )
    
    # Status indicator
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 2rem;">
                <span class="status-indicator status-online"></span>
                <span style="color: #059669; font-weight: 600;">🟢 Agent Online</span>
                <span style="margin-left: 1rem; color: #6b7280;">Ready to help with Exa support</span>
            </div>
            """,
            unsafe_allow_html=True
        )


async def body():
    if not check_password():
        return

    # Initialize session state
    await initialize_agent_session_state(agent_name)

    # Sidebar
    with st.sidebar:
        st.markdown("### 🛠️ Support Configuration")
        
        # Model selection
        model_id = await selected_model()
        
        # Session management
        if st.session_state[agent_name]["agent"] is not None:
            await session_selector(
                agent_name,
                st.session_state[agent_name]["agent"],
                get_exa_support_agent,
                "exa_user",
                model_id,
            )
        
        # Knowledge base management
        if st.session_state[agent_name]["agent"] is not None:
            await knowledge_widget(agent_name, st.session_state[agent_name]["agent"])
        
        # Utilities
        if st.session_state[agent_name]["agent"] is not None:
            await utilities_widget(agent_name, st.session_state[agent_name]["agent"])

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 💬 Support Chat")
        
        # Chat container
        with st.container():
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            # Display chat messages
            for message in st.session_state[agent_name]["messages"]:
                if message["role"] == "user":
                    st.markdown(
                        f"""
                        <div class="chat-message user-message">
                            <div class="message-header user-header">
                                👤 You
                            </div>
                            <div class="message-content">
                                {message['content']}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="chat-message assistant-message">
                            <div class="message-header assistant-header">
                                🤖 Exa Support
                            </div>
                            <div class="message-content">
                                {message['content']}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    # Display tool calls if present
                    if "tool_calls" in message and message["tool_calls"]:
                        display_tool_calls(st.empty(), message["tool_calls"])

            st.markdown('</div>', unsafe_allow_html=True)

        # Chat input
        if prompt := st.chat_input("Describe your issue or ask a question..."):
            # Add user message
            await add_message(agent_name, "user", prompt)
            
            # Get or create agent
            if st.session_state[agent_name]["agent"] is None:
                st.session_state[agent_name]["agent"] = get_exa_support_agent(
                    model_id=model_id, debug_mode=True
                )
            
            # Create a container for the response
            response_container = st.empty()
            tool_calls_container = st.empty()
            
            # Variables to capture the final response
            final_content = ""
            final_tools = []
            
            # Stream the response
            run_response = await st.session_state[agent_name]["agent"].arun(
                prompt, stream=True
            )
            async for resp_chunk in run_response:
                if resp_chunk.content:
                    final_content += resp_chunk.content
                    response_container.markdown(
                        f"""
                        <div class="chat-message assistant-message">
                            <div class="message-header assistant-header">
                                🤖 Exa Support
                            </div>
                            <div class="message-content">
                                {final_content}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                if resp_chunk.tools:
                    final_tools.extend(resp_chunk.tools)
                    display_tool_calls(tool_calls_container, resp_chunk.tools)
            
            # Add assistant message to session state
            if final_content or final_tools:
                await add_message(
                    agent_name,
                    "assistant",
                    final_content,
                    final_tools,
                )

    with col2:
        st.markdown("### 📋 Support Examples")
        
        # Examples container
        with st.container():
            st.markdown('<div class="examples-container">', unsafe_allow_html=True)
            
            # Show example inputs
            await example_inputs(agent_name)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### 📊 Support Metrics")
        
        # Metrics container
        with st.container():
            if st.session_state[agent_name]["messages"]:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(
                        f"""
                        <div class="metric-container">
                            <div class="metric-label">Messages</div>
                            <div class="metric-value">{len(st.session_state[agent_name]["messages"])}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                with col2:
                    session_id = st.session_state[agent_name].get("session_id")
                    session_display = session_id[:8] + "..." if session_id else "New Session"
                    st.markdown(
                        f"""
                        <div class="metric-container">
                            <div class="metric-label">Session ID</div>
                            <div class="metric-value" style="font-size: 1rem;">{session_display}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.markdown(
                    """
                    <div class="info-message">
                        No messages yet. Start a conversation to see metrics!
                    </div>
                    """,
                    unsafe_allow_html=True
                )


async def main():
    await initialize_agent_session_state(agent_name)
    await header()
    await body()
    await about_agno()


if __name__ == "__main__":
    asyncio.run(main())
