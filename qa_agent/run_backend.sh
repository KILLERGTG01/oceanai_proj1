#!/bin/bash
#!/bin/bash
# We now rely on python-dotenv to load the key from .env if not exported.
# However, we can still check if .env exists or if the var is set.

if [ -z "$GOOGLE_API_KEY" ] && [ ! -f .env ]; then
    echo "Warning: GOOGLE_API_KEY is not set and no .env file found."
    echo "Please create a .env file or export the key."
fi

echo "Starting Backend..."
cd backend
uvicorn main:app --reload
