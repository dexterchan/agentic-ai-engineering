import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

slack_channel_id:str = str(os.getenv("SLACK_AGENT_CHANNEL_ID"))
slack_oauth_token = os.getenv("SLACK_BOT_AGENT_OAUTH_TOKEN")
slack_client = WebClient(token=slack_oauth_token)

def push(text: str):
    """Send a push slack notification to the user"""
    try:
        response = slack_client.chat_postMessage(channel=slack_channel_id, text=text)
        return {"status": str(response.status_code)}
    except SlackApiError as e:
        # Handle any errors that occur
        print(f"Error sending slack message: {e.response['error']} {e.response['error']['message']}")
        return {"status": "error", "message": str(e.response['error'])}