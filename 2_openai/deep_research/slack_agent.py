import os
from typing import Dict, Any
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


from agents import Agent, function_tool

slack_channel_id:str = str(os.getenv("SLACK_AGENT_CHANNEL_ID"))
slack_oauth_token = os.getenv("SLACK_BOT_AGENT_OAUTH_TOKEN")
slack_client = WebClient(token=slack_oauth_token)

def _fmt_blocks(subject: str, markdown_body: str) -> list[dict[str, Any]]:

    return  [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": subject
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": markdown_body
                }
            }
        ]


@function_tool
def send_message(subject: str, markdown_body: str) -> Dict[str, str]:
    """ Send an email with the given subject and markdown body """
    try:
        # Attempt to send the message
        #print(f"Sending slack message: {subject} {markdown_body}")
        response = slack_client.chat_postMessage(channel=slack_channel_id, blocks=_fmt_blocks(subject, markdown_body))
        return {"status": str(response.status_code)}
    except SlackApiError as e:
        # Handle any errors that occur
        print(f"Error sending slack message: {e.response['error']} {e.response['error']['message']}")
        return {"status": "error", "message": str(e.response['error'])}

@function_tool
def send_message_no_subject(markdown_body: str) -> Dict[str, str]:
    """ Send an email with the given subject and markdown body """
    try:
        # Attempt to send the message
        #response = slack_client.chat_postMessage(channel=slack_channel_id, text=markdown_body)
        response = slack_client.chat_postMessage(channel=slack_channel_id, blocks=_fmt_blocks("No subject", markdown_body))
        return {"status": str(response.status_code)}
    except SlackApiError as e:
        # Handle any errors that occur
        print(f"Error sending slack message: {e.response['error']}")
        return {"status": "error", "message": str(e.response['error'])}


INSTRUCTIONS = """You will be given a detailed report in markdown format. Derive the subject line. Directly return the subject line.
                send the message to slack using the send_message tool. Do not include any other text in your response.
"""

slack_agent = Agent(
    name="Slack agent",
    instructions=INSTRUCTIONS,
    tools=[send_message],
    model="gpt-4o-mini",
)
