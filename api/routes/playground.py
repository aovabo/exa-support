from os import getenv

from agno.playground import Playground

from agents.exa_support import get_exa_support_agent
from workspace.dev_resources import dev_fastapi

######################################################
## Router for the Playground Interface
######################################################

exa_support_agent = get_exa_support_agent(debug_mode=True)

# Create a playground instance
playground = Playground(agents=[exa_support_agent])

# Register the endpoint where playground routes are served with agno.com
if getenv("RUNTIME_ENV") == "dev":
    playground.serve(f"http://localhost:{dev_fastapi.host_port}")

playground_router = playground.get_async_router()
