import asyncio

import nest_asyncio
import streamlit as st
from agno.agent import Agent
from agno.memory.agent import AgentRun
from agno.tools.streamlit.components import check_password
from agno.utils.log import logger

from agents.sage import get_exa_support_agent
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

nest_asyncio.apply()

st.set_page_config(
    page_title="Exa Support Engineer",
    page_icon="🛠️",
    layout="wide",
)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
agent_name = "exa_support"


async def header():
    st.markdown("<h1 class='heading'>Exa Support Engineer</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='subheading'>An AI-powered support agent that provides exceptional customer service for Exa products and services.</p>",
        unsafe_allow_html=True,
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
        
        # Display chat messages
        for message in st.session_state[agent_name]["messages"]:
            if message["role"] == "user":
                st.markdown(f"**👤 You:** {message['content']}")
            else:
                st.markdown(f"**🤖 Exa Support:** {message['content']}")
                
                # Display tool calls if present
                if "tool_calls" in message and message["tool_calls"]:
                    display_tool_calls(st.empty(), message["tool_calls"])

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
            
            # Stream the response
            async for resp_chunk in st.session_state[agent_name]["agent"].run(
                prompt, stream=True
            ):
                if resp_chunk.content:
                    response_container.markdown(resp_chunk.content)
                
                if resp_chunk.tools:
                    display_tool_calls(tool_calls_container, resp_chunk.tools)
            
            # Add assistant message to session state
            if st.session_state[agent_name]["agent"] is not None:
                last_run = st.session_state[agent_name]["agent"].memory.get_last_run()
                if last_run and last_run.response:
                    await add_message(
                        agent_name,
                        "assistant",
                        last_run.response.content or "",
                        last_run.response.tools,
                    )

    with col2:
        st.markdown("### 📋 Support Examples")
        
        # Show example inputs
        await example_inputs(agent_name)
        
        st.markdown("### 📊 Support Metrics")
        if st.session_state[agent_name]["messages"]:
            st.metric("Messages", len(st.session_state[agent_name]["messages"]))
            st.metric("Session ID", st.session_state[agent_name].get("session_id", "N/A"))


async def main():
    await initialize_agent_session_state(agent_name)
    await header()
    await body()
    await about_agno()


if __name__ == "__main__":
    asyncio.run(main())
