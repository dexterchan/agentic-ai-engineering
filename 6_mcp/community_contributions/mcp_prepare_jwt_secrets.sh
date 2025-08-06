#!/bin/bash
# This script sets up the environment for the MCP server and client, including JWT secret generation.
#Create the jwt secret for HMAC256:
cat << EOF | tee .env
    JWT_SECRET_KEY=$(openssl rand -base64 32)
EOF
