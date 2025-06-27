import asyncio

import nest_asyncio
import streamlit as st
from agno.tools.streamlit.components import check_password

from ui.css import CUSTOM_CSS
from ui.utils import about_agno, footer

nest_asyncio.apply()

st.set_page_config(
    page_title="Exa Support Platform",
    page_icon="🛠️",
    layout="wide",
)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


async def header():
    st.markdown("<h1 class='heading'>Exa Support Platform</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='subheading'>AI-powered customer support automation for Exa products and services.</p>",
        unsafe_allow_html=True,
    )


async def body():
    if not check_password():
        return

    st.markdown("## 🚀 Welcome to Exa Support")

    st.markdown("""
    This platform demonstrates an intelligent support system built with **agno** that provides exceptional customer service for Exa products.

    ### ✨ Key Features
    
    - **🤖 AI-Powered Support Agent** - Intelligent responses to customer inquiries
    - **🔍 Multi-Source Knowledge** - Access to Exa documentation and web resources
    - **💬 Discord Integration** - Monitor and respond to community discussions
    - **📊 Support Analytics** - Track and analyze support interactions
    - **🛠️ Knowledge Management** - Build and maintain support knowledge base

    ### 🎯 Perfect for Support Engineers
    
    This system showcases the skills needed for Exa's Support Engineer role:
    - **Technical Troubleshooting** - Step-by-step problem resolution
    - **Customer Communication** - Clear, empathetic support responses
    - **Issue Classification** - Intelligent routing and escalation
    - **Knowledge Management** - Building comprehensive support resources
    - **Automation** - Reducing manual support workload

    ### 🛠️ Built With
    
    - **agno** - AI agent development framework
    - **ExaTools** - Exa's own search and content tools
    - **DiscordTools** - Community monitoring and engagement
    - **Streamlit** - Beautiful, interactive web interface
    - **PostgreSQL** - Reliable data storage and session management

    ### 🚀 Get Started
    
    Navigate to the **Exa Support Engineer** page to interact with the AI support agent and see it in action!
    """)

    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🤖 AI Support Agent
        - Intelligent problem diagnosis
        - Step-by-step troubleshooting
        - Context-aware responses
        - Multi-language support
        """)
    
    with col2:
        st.markdown("""
        ### 🔍 Knowledge Integration
        - Exa documentation access
        - Web search capabilities
        - Community knowledge
        - Real-time updates
        """)
    
    with col3:
        st.markdown("""
        ### 📊 Support Analytics
        - Issue tracking
        - Response metrics
        - Knowledge gaps
        - Performance insights
        """)

    st.markdown("---")
    
    st.markdown("### 🎯 Support Scenarios")
    
    scenarios = [
        {
            "title": "🔑 Authentication Issues",
            "description": "Help users resolve API key problems and authentication errors"
        },
        {
            "title": "🔍 Search Optimization", 
            "description": "Guide users on effective Exa search strategies and best practices"
        },
        {
            "title": "💰 Billing & Pricing",
            "description": "Explain pricing plans and help with billing-related questions"
        },
        {
            "title": "🔧 Integration Support",
            "description": "Provide step-by-step integration guidance for developers"
        },
        {
            "title": "🐛 Bug Reports",
            "description": "Collect detailed information and route to appropriate teams"
        },
        {
            "title": "💡 Feature Requests",
            "description": "Acknowledge requests and route to product development"
        }
    ]
    
    for i, scenario in enumerate(scenarios):
        if i % 2 == 0:
            cols = st.columns(2)
            with cols[0]:
                st.markdown(f"**{scenario['title']}**\n{scenario['description']}")
        else:
            with cols[1]:
                st.markdown(f"**{scenario['title']}**\n{scenario['description']}")


async def main():
    await header()
    await body()
    await footer()
    await about_agno()


if __name__ == "__main__":
    asyncio.run(main())
