# Website Navigation Agent API

A FastAPI-based service that provides website navigation and service information. This API serves as a backend for retrieving navigation menu items and available services for the Fiction Solutions website.

## 🏗️ Architecture

- **Framework**: FastAPI with Python 3.12+
- **Logging**: Google Cloud Logging with console fallback
- **Data Storage**: Static JSON files for navigation and services
- **Deployment**: Google Cloud Run with Docker containerization
- **Package Management**: UV for fast Python package management

## 📁 Project Structure

```
site-api/
   app.py                    # API route definitions
   main.py                   # FastAPI application entry point
   config/
      settings.py          # Configuration and environment variables
      logging.py           # Google Cloud Logging setup
   service/
      website.py           # Business logic for website data
   data/
      website-navigation.json  # Navigation menu items
      website-services.json   # Available services
   deploy.sh                # Google Cloud Run deployment script
   Dockerfile               # Container configuration
   pyproject.toml          # Python dependencies and project metadata
   .env                    # Environment variables (create this)
```

## 🔗 API Endpoints

### Base URL
- **Local**: `http://localhost:8000`
- **Production**: `https://your-service-url.run.app`

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check endpoint |
| GET | `/website/services` | Get all available services |
| GET | `/website/navigation/{section}` | Get URL for specific navigation section |
| GET | `/api/docs` | Interactive API documentation (Swagger UI) |
| GET | `/api/redocs` | Alternative API documentation (ReDoc) |

### Example Responses

**GET /website/services**
```json
[
  {
    "id": 1,
    "name": "Web development",
    "description": "Full-stack web development services including frontend and backend solutions."
  }
]
```

**GET /website/navigation/about**
```json
{
  "url": "http://fictionsolutions.com/about"
}
```

## 💻 Local Development Setup

### Prerequisites

- Python 3.12 or higher
- UV package manager
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ericgbekor/website-guide-agent
   cd site-api
   ```

2. **Install UV (if not already installed)**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Create environment file**
   ```bash
   cp .env.example .env  # If example exists, or create manually
   ```

5. **Configure environment variables** (see [Environment Variables](#environment-variables))

6. **Run the development server**
   ```bash
   uv run python main.py
   ```

   The API will be available at `http://localhost:8000`

### Development Commands

```bash
# Install new dependency
uv add package-name

# Run with auto-reload
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run tests (if available)
uv run pytest

# Format code (if formatter is configured)
uv run black .
```

## ⚙️ Environment Variables

Create a `.env` file in the project root with the following variables:

### Required Variables

```bash
# Google Cloud Configuration
GCLOUD_PROJECT_ID=your-project-id
GCLOUD_REGION=europe-west2

# Google Cloud Logging (JSON string format)
GOOGLE_APPLICATION_CREDENTIALS={"type":"service_account","project_id":"your-project",...}

# For deployment only
SERVICE_NAME=website-api
REPO_NAME=docker-repo
IMAGE_TAG=latest
```

### Optional Variables

```bash
# CORS Configuration
ALLOWED_ORIGINS=*

# Logging Level
LOG_LEVEL=INFO

# Cloud Run Configuration (for deployment)
MIN_INSTANCES=0
MAX_INSTANCES=4
MEMORY=512Mi
CPU=1
PORT=8000
```

### Setting up Google Cloud Credentials

1. **Create a service account** in Google Cloud Console
2. **Download the JSON key file**
3. **Convert to single-line JSON string**:
   - Remove all line breaks and formatting spaces
   - Escape newlines in the private key (`\n` becomes `\\n`)
   - Example:
     ```bash
     GOOGLE_APPLICATION_CREDENTIALS={"type":"service_account","project_id":"my-project","private_key":"-----BEGIN PRIVATE KEY-----\\nMIIEvQI...\\n-----END PRIVATE KEY-----\\n","client_email":"service@project.iam.gserviceaccount.com"}
     ```

## 🐳 Docker Development

### Build and run locally

```bash
# Build the Docker image
docker build -t website-api .

# Run the container
docker run -p 8000:8000 --env-file .env website-api
```

### Using Docker Compose (if available)

```bash
docker-compose up --build
```

## ☁️ Google Cloud Run Deployment

### 🚀 Recommended: Using deploy.sh Script

The easiest way to deploy the Site API is using the included deployment script:

#### Prerequisites

1. **Google Cloud CLI** installed and configured
2. **Docker** installed and running
3. **Google Cloud Project** with billing enabled
4. **Required APIs** enabled:
   - Cloud Run API
   - Artifact Registry API
   - Cloud Logging API

#### Quick Deployment

1. **Configure environment variables** in `.env`:
   ```bash
   GCLOUD_PROJECT_ID=your-project-id
   GCLOUD_REGION=europe-west2
   SERVICE_NAME=website-api
   REPO_NAME=docker-repo
   IMAGE_TAG=latest
   ```

2. **Deploy with one command**:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

   The script automatically handles:
   - ✅ Environment variable validation
   - 🔐 Google Cloud authentication setup
   - 📦 Artifact Registry repository creation
   - 🚀 Docker image build and push
   - ☁️ Cloud Run service deployment
   - 🌐 Service URL output

3. **Access your deployed API**:
   The script will display the service URL when deployment completes.

### Manual Deployment

If you prefer manual deployment:

```bash
# 1. Enable required APIs
gcloud services enable run.googleapis.com artifactregistry.googleapis.com

# 2. Create Artifact Registry repository
gcloud artifacts repositories create docker-repo \
    --repository-format=docker \
    --location=europe-west2

# 3. Configure Docker authentication
gcloud auth configure-docker europe-west2-docker.pkg.dev

# 4. Build and push image
docker buildx build --platform linux/amd64 \
    -t europe-west2-docker.pkg.dev/PROJECT_ID/docker-repo/website-api:latest \
    --push .

# 5. Deploy to Cloud Run
gcloud run deploy website-api \
    --image europe-west2-docker.pkg.dev/PROJECT_ID/docker-repo/website-api:latest \
    --region=europe-west2 \
    --allow-unauthenticated
```

## 📊 Monitoring & Logging

### Local Development
- Logs are output to console with timestamps
- Debug information available when `LOG_LEVEL=DEBUG`

### Production (Google Cloud Run)
- Logs are sent to Google Cloud Logging
- Structured logging with request tracking
- Monitor through Google Cloud Console > Logging

### Key Log Events
- Service initialization
- API endpoint access
- Data loading operations
- Error conditions and warnings

## ⚙️ Configuration Files

### Data Files

Update the JSON files in the `data/` directory to modify available content:

- `website-navigation.json`: Navigation menu items with sections and URLs
- `website-services.json`: Available services with descriptions

Example navigation item:
```json
{
  "id": 1,
  "section": "Home",
  "url": "/",
  "description": "Optional description"
}
```

## 🧪 Testing

### Manual Testing

1. **Health Check**:
   ```bash
   curl http://localhost:8000/
   ```

2. **Services Endpoint**:
   ```bash
   curl http://localhost:8000/website/services
   ```

3. **Navigation Endpoint**:
   ```bash
   curl http://localhost:8000/website/navigation/about
   ```

### API Documentation

Visit `/api/docs` for interactive Swagger documentation where you can test all endpoints directly.

## 🔧 Troubleshooting

### Common Issues

1. **"Config 'GOOGLE_APPLICATION_CREDENTIALS' has value '{'. Not a valid dict."**
   - Ensure the JSON string is properly escaped and on a single line
   - Check that all quotes are properly escaped

2. **"Google Cloud credentials file not found"**
   - Verify the service account JSON is correctly formatted
   - Ensure all required fields are present in the credentials

3. **Port already in use**
   - Change the port in `main.py` or kill the process using port 8000

4. **Import errors**
   - Run `uv sync` to ensure all dependencies are installed
   - Verify Python version is 3.12+

### Logs and Debugging

- Set `LOG_LEVEL=DEBUG` for detailed logging
- Check Google Cloud Console > Logging for production issues
- Use `/api/docs` to test individual endpoints

## 📝 Development Notes

- The API uses static JSON files for data storage
- CORS is configured to allow all origins by default
- Service automatically falls back to console logging if Google Cloud setup fails
- Navigation URLs are prefixed with `http://fictionsolutions.com` in responses