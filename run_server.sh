#!/bin/bash

# Load virtual environment
source venv.sh

# Build command line arguments from environment variables
ARGS=""

if [ ! -z "$GOOGLE_API_KEY" ]; then
    ARGS="$ARGS --google-api-key $GOOGLE_API_KEY"
fi

if [ ! -z "$GOOGLE_ENGINE_KEY" ]; then
    ARGS="$ARGS --google-engine-key $GOOGLE_ENGINE_KEY"
fi

if [ ! -z "$RAY_SEARCH_PROXY_URL" ]; then
    ARGS="$ARGS --proxy $RAY_SEARCH_PROXY_URL"
fi

# Run the server with collected arguments
python server.py $ARGS
