#!/bin/bash
set -e  # Exit on first error

# -----------------------------
# Configuration
# -----------------------------

# Set your Google Cloud Project ID
export GOOGLE_CLOUD_PROJECT="gen-lang-client-0708164147"

# Set your desired Google Cloud Location
export GOOGLE_CLOUD_LOCATION="europe-west2" # Example location

# Set the path to your agent code directory
export AGENT_PATH="./website_agent_service" # Assuming website_agent_service is in the current directory

# Set a name for your Cloud Run service (optional)
export SERVICE_NAME="website-agent-service"

# Set an application name (optional)
export APP_NAME="website-agent-app"

# -----------------------------
# Deploy to Google Cloud Run
# -----------------------------

echo "🚀 Deploying ADK agent to Cloud Run..."
echo "Project: $GOOGLE_CLOUD_PROJECT"
echo "Region: $GOOGLE_CLOUD_LOCATION"
echo "Service: $SERVICE_NAME"
echo "App Name: $APP_NAME"
echo "Agent Path: $AGENT_PATH"

adk deploy cloud_run \
  --project="$GOOGLE_CLOUD_PROJECT" \
  --region="$GOOGLE_CLOUD_LOCATION" \
  --service_name="$SERVICE_NAME" \
  --app_name="$APP_NAME" \
  --with_ui \
  --trace_to_cloud \
  "$AGENT_PATH"

echo "✅ Deployment complete."
