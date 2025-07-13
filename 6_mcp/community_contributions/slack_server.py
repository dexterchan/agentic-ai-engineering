import os
from dotenv import load_dotenv

from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

#mcp server filter out SLACK OAUTH token. We should dynamically load the token here by load_dotenv
load_dotenv(override=True)

slack_channel_id:str = str(os.getenv("SLACK_AGENT_CHANNEL_ID"))
slack_oauth_token = str(os.getenv("SLACK_BOT_AGENT_OAUTH_TOKEN"))
slack_client = WebClient(token=slack_oauth_token)

import logging

class PushModelArgs(BaseModel):
    message: str = Field(description="A brief message to push")


mcp = FastMCP("push_server")

@mcp.tool()
def push(args: PushModelArgs) -> str:
    """Send a push slack notification to the user"""
    try:
        print(f"Push: {args.message}")
        response = slack_client.chat_postMessage(channel=slack_channel_id, text=args.message)
        
        return {"status": str(response.status_code)}
    except SlackApiError as e:
        # Handle any errors that occur
        print(f"Error sending slack message: {e.response['error']} {e.response['error']['message']}")
        return {"status": "error", "message": str(e.response['error'])}
    
# @mcp.tool()
# def push_directly(msg: str) -> str:
#     """Send a push slack notification to the user"""
#     try:
#         logging.critical(msg)
#         logging.critical(slack_channel_id)
#         logging.critical(slack_oauth_token)
#         response = slack_client.chat_postMessage(channel=slack_channel_id, text="rubbish")
#         return "ok"
#         # return f"Push notification sent with {response.status_code}"
#     except SlackApiError as e:
#         # Handle any errors that occur
#         print(f"Error sending slack message: {e.response['error']} {e.response['error']['message']}")
#         return f"Push notification error with {str(e.response['error'])}"
    
if __name__ == "__main__":
    mcp.run(transport="stdio")
    # # args = PushModelArgs(message="Hello, world!")
    # # push(args)
    # push_directly("Hello, world!")