import os
import asyncio
from fastmcp import FastMCP
from fastmcp.server.auth.providers.bearer import BearerAuthProvider
import uvicorn
from dotenv import load_dotenv

load_dotenv()

# --- Authentication Configuration ---
# This is your secret key for signing and verifying JWTs.
# In a real application, use a strong, securely stored secret.
# JWT configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable not set")
EXPECTED_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "your-api-audience")
EXPECTED_ISSUER = os.getenv("AUTH0_ISSUER", "your-issuer")

JWT_ALGORITHM = "HS256"

# 1. Create a BearerAuthProvider instance for JWT validation
#    We provide the public key (for HS256, it's the secret key) and the algorithm.
auth_provider = BearerAuthProvider(
    public_key=JWT_SECRET_KEY,
    algorithm=JWT_ALGORITHM,
)

# 2. Initialize the FastMCP server with the authentication provider
mcp = FastMCP(
    "CalculatorServer",
    auth=auth_provider,
)

@mcp.tool
async def add(a: int, b: int) -> int:
    """
    Adds two integers and returns the result.
    This tool is protected and requires a valid JWT Bearer token.
    """
    print(f"Received request to add {a} and {b}")
    return a + b

mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8080,
        path="/api/mcp",
        log_level="debug",
    )
# async def main():
#     """
#     Runs the MCP server as an HTTP server on port 8000.
#     """
#     # FINAL CORRECTION: Pass the '.asgi' attribute of the mcp object.
#     # This is the actual ASGI application that Uvicorn can run.
#     config = uvicorn.Config(
#         mcp.asgi, # <-- This is the correct attribute
#         host="127.0.0.1",
#         port=8000,
#         log_level="info",
#     )
#     server = uvicorn.Server(config)
#     print("Starting MCP server on http://127.0.0.1:8000")
#     await server.serve()

# if __name__ == "__main__":
#     asyncio.run(main())