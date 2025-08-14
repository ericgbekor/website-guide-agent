# Cloud Run ADK Agent Chat Application

A Streamlit-based chat interface for interacting with Google ADK (Agent Development Kit) agents deployed on Google Cloud Run. This application provides a user-friendly web interface to test and communicate with your deployed ADK agents with support for streaming responses, tool usage visualization, and session management.

## ✨ Features

- **Multi-endpoint Support**: Automatically tries multiple endpoint patterns (`/run_sse`, `/run`, `/chat`, `/`)
- **Streaming Responses**: Real-time streaming with Server-Sent Events (SSE) support
- **Tool Usage Visualization**: Display function calls and responses from ADK agents
- **Session Management**: Create and manage conversation sessions
- **Response Processing**: Parse ADK event format with tool call extraction
- **Debug Mode**: View raw responses for troubleshooting
- **Containerized**: Ready for deployment to Google Cloud Run

## 🏗️ Architecture

- **Frontend**: Streamlit web application
- **Backend Communication**: HTTP requests to Cloud Run ADK agents
- **Response Format**: ADK event stream processing
- **Deployment**: Docker containerization with Google Cloud Run

## 📋 Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- Google Cloud SDK (for deployment)
- Docker (for local containerization and deployment)
- ADK agent deployed on Google Cloud Run

## 💻 Local Development Setup

### 1. Clone and Navigate
```bash
git clone https://github.com/ericgbekor/website-guide-agent
cd chat-ui
```

### 2. Install Dependencies
Using uv (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -r requirements.txt
# or
pip install streamlit>=1.48.0 requests>=2.32.4
```

### 3. Run Locally
```bash
# Using uv
uv run streamlit run app.py

# Or using streamlit directly
streamlit run app.py
```

The application will be available at `http://localhost:8501`

### 4. Configure Your ADK Agent
1. Open the sidebar in the Streamlit interface
2. Enter your Cloud Run service URL (e.g., `https://your-service-123abc-uc.a.run.app`)
3. Enter your ADK app name (e.g. website-agent-app)
4. Click "Save Configuration"
5. Optionally create a session or start chatting directly

## ☁️ Cloud Run Deployment

### 🔐 Google Cloud Permissions Required

Your Google Cloud account needs the following IAM roles:

**Essential Roles:**
- `Cloud Run Admin` - Deploy and manage Cloud Run services
- `Artifact Registry Administrator` - Create and manage Docker repositories
- `Storage Admin` - Access to Cloud Build artifacts
- `Service Account User` - Use default compute service account

**Additional Roles (if not using default service account):**
- `Project Editor` or specific service permissions
- `Cloud Build Editor` (if using Cloud Build)

**APIs to Enable:**
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### 🚀 Recommended: Using deploy.sh Script

The simplest way to deploy the Chat UI is using the included deployment script:

#### Quick Deployment

1. **Set up environment variables** in `.env`:
   ```bash
   # Required variables
   PROJECT_ID=your-gcp-project-id
   LOCATION=us-central1
   SERVICE_NAME=adk-chat-ui
   REPO_NAME=adk-chat-repo
   IMAGE_TAG=latest

   # Optional variables (with defaults)
   MIN_INSTANCES=0
   MAX_INSTANCES=4
   MEMORY=512Mi
   CPU=1
   PORT=8000
   ```

2. **Deploy with one command**:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

   The deployment script automatically:
   - ✅ Validates all environment variables
   - 🔐 Sets up Google Cloud authentication
   - 📦 Creates Artifact Registry repository
   - 🚀 Builds and pushes Docker image
   - ☁️ Deploys to Cloud Run
   - 🌐 Outputs the service URL

3. **Access your chat interface**:
   The script will display the Chat UI URL when deployment completes.

### 4. Manual Deployment (Alternative)

If you prefer manual deployment:

```bash
# Build and push image
docker buildx build --platform linux/amd64 -t gcr.io/PROJECT_ID/adk-chat-ui .
docker push gcr.io/PROJECT_ID/adk-chat-ui

# Deploy to Cloud Run
gcloud run deploy adk-chat-ui \
  --image gcr.io/PROJECT_ID/adk-chat-ui \
  --region=us-central1 \
  --allow-unauthenticated \
  --port=8000
```

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PROJECT_ID` | Yes | - | Google Cloud Project ID |
| `LOCATION` | Yes | - | Deployment region (e.g., us-central1) |
| `SERVICE_NAME` | Yes | - | Cloud Run service name |
| `REPO_NAME` | Yes | - | Artifact Registry repository name |
| `IMAGE_TAG` | Yes | - | Docker image tag |
| `MIN_INSTANCES` | No | 0 | Minimum Cloud Run instances |
| `MAX_INSTANCES` | No | 4 | Maximum Cloud Run instances |
| `MEMORY` | No | 512Mi | Memory allocation |
| `CPU` | No | 1 | CPU allocation |
| `PORT` | No | 8000 | Application port |

## 🎯 Usage

### Basic Chat
1. Configure your ADK agent URL in the sidebar
2. Start typing messages in the chat input
3. The application will automatically try different endpoints to find the working one

### Session Management
- **Create Session**: Establishes a stateful conversation with your ADK agent
- **New Session**: Starts fresh conversation history
- **No Session**: Use temporary sessions for one-off interactions

### Tool Usage
- View function calls made by your ADK agent
- Inspect tool arguments and responses
- Debug mode shows raw response data

## 🔌 ADK Agent Endpoints Supported

The application automatically detects and uses the appropriate endpoint:

1. **`/run_sse`** - Server-Sent Events for streaming (preferred)
2. **`/run`** - Standard ADK endpoint with event processing
3. **`/chat`** - Simple chat endpoint
4. **`/`** - Root endpoint fallback

## 🔧 Troubleshooting

### Common Issues

**"All endpoints failed"**
- Verify your Cloud Run service URL is correct
- Check if your ADK agent is deployed and running
- Ensure the service allows unauthenticated requests

**Authentication errors during deployment**
- Run `gcloud auth application-default login`
- Verify you have the required IAM permissions
- Check that APIs are enabled in your project

**Docker build fails**
- Ensure Docker is running
- Check your internet connection for dependency downloads
- Verify uv.lock file is present

**Deployment timeouts**
- Increase Cloud Run timeout settings
- Check service logs: `gcloud run logs read SERVICE_NAME --region=REGION`

### Debug Mode
Enable debug mode in the UI to see:
- Raw API responses
- Endpoint selection process
- Detailed error messages

## 🛠️ Development

### Project Structure
```
chat-ui/
   app.py              # Main Streamlit application
   pyproject.toml      # Python dependencies
   uv.lock            # Dependency lock file
   Dockerfile         # Container configuration
   deploy.sh          # Cloud Run deployment script
   .env               # Environment variables (create this)
   README.md          # This file
```

### Adding Features
- Modify `CloudRunADKClient` class for new endpoint support
- Update `process_response` method for different response formats
- Extend Streamlit UI in the `main()` function

## 🔒 Security Considerations

- This application allows unauthenticated access by default
- For production use, implement proper authentication
- Secure your ADK agent endpoints appropriately
- Review IAM permissions regularly


## 💬 Support

For issues and questions:
- Check the troubleshooting section above
- Review Google Cloud Run and ADK documentation
- Create an issue in this repository