from __future__ import annotations
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
from IPython.display import display, Markdown

load_dotenv(override=True)







async def pi() -> str:
    instructions = "You are mathematic expert. Help me with my math problems. " 
    request = "Help me to calculate PI with 1000000 iteration with most accuracy. Then, send the result to slack push notification."
    model = "gpt-4.1-mini"
    pi_params = {"command": "uv", "args": ["run", "calc_pi_server.py"]}
    slack_params = {"command": "uv", "args": ["run", "slack_server.py"]}
    async with MCPServerStdio(params=pi_params, client_session_timeout_seconds=30) as pi_mcp_server:
        async with MCPServerStdio(params=slack_params, client_session_timeout_seconds=30) as slack_mcp_server:
            agent = Agent(name="pi_calculation", instructions=instructions, model=model, mcp_servers=[pi_mcp_server, slack_mcp_server])
            with trace("pi_calculation"):
                result = await Runner.run(agent, request)
            return (result.final_output)

async def write_to_slack(message: str) -> str:
    """A mock function to simulate writing to Slack."""
    params = {"command": "uv", "args": ["run", "slack_server.py"]}

    instructions = "You are helpful agent of communication"
    request = f"Send a  message as '{message}'"
    model = "gpt-4.1-mini"
    async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as mcp_server:
        agent = Agent(name="send_msg", instructions=instructions, model=model, mcp_servers=[mcp_server])
        with trace("send_msg"):
            result = await Runner.run(agent, request)
        
    return result.final_output

pi_result = (asyncio.run(pi()))

#print(asyncio.run(write_to_slack(pi_result)))
