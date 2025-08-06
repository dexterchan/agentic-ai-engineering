import os
import asyncio
import jwt
import time
from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport
from dotenv import load_dotenv

load_dotenv()

# --- Token Generation ---
# Use the same secret key as the server.
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable not set")
JWT_ALGORITHM = "HS256"
SERVER_URL = "http://127.0.0.1:8080/api/mcp"

def create_jwt_token() -> str:
    """
    Creates a new JWT token signed with the HS256 algorithm.
    """
    payload = {
        "sub": "mcp-client-user",  # Subject of the token
        "iat": int(time.time()),      # Issued at time
        "exp": int(time.time()) + 3600, # Expiration time (1 hour)
        "scope": "read write"         # Example scope
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    print(f"Generated JWT: {token}\n")
    return token

async def main():
    """
    Creates a client, authenticates with a JWT, and calls the 'add' tool.
    """
    # 1. Generate the JWT Bearer token
    token = create_jwt_token()

    # 2. Set up the authorization header
    auth_headers = {
        "Authorization": f"Bearer {token}"
    }

    # 3. Configure the client to use the HTTP transport with the auth header
    transport = StreamableHttpTransport(url=SERVER_URL, headers=auth_headers)

    # 4. Create a client and connect to the server
    async with Client(transport=transport) as client:
        print("Client connected to the server.")

        # 5. Call the 'add' tool with parameters
        try:
            result = await client.call_tool("add", {"a": 10, "b": 32})
            print(f"Successfully called 'add' tool.")
            # The actual result is nested inside the tool result object
            if result :
                 print(f"Result of 10 + 32 is: {result.structured_content['result']}")
            elif result.error:
                print(f"Error calling tool: {result.error}")
            else:
                print("No result or error returned from the tool call.")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())