#!/bin/bash

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found"
    exit 1
fi

# Load environment variables
set -a
source .env
set +a

# Function to check if required variables are set
check_required_vars() {
    local required_vars=("GCLOUD_PROJECT_ID" "GCLOUD_REGION" "SERVICE_NAME" "REPO_NAME" "IMAGE_TAG")
    local missing_vars=()

    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done

    if [ ${#missing_vars[@]} -ne 0 ]; then
        echo "Error: Missing required environment variables: ${missing_vars[*]}"
        exit 1
    fi
}

# Function to setup Google Cloud authentication
setup_gcloud() {
    echo "🔐 Setting up Google Cloud authentication..."
    gcloud auth application-default login
    gcloud config set project $GCLOUD_PROJECT_ID
}

# Function to setup Artifact Registry
setup_artifact_registry() {
    echo "📦 Setting up Artifact Registry..."
    gcloud services enable artifactregistry.googleapis.com
    
    # Create repository if it doesn't exist
    if ! gcloud artifacts repositories describe $REPO_NAME --location=$GCLOUD_REGION >/dev/null 2>&1; then
        gcloud artifacts repositories create $REPO_NAME \
            --repository-format=docker \
            --location=$GCLOUD_REGION
    fi
    
    gcloud auth configure-docker $GCLOUD_REGION-docker.pkg.dev
}

# Function to build and push Docker image
build_and_push() {
    echo "🏗️  Building and pushing Docker image..."
    docker buildx build \
        --platform linux/amd64 \
        -f Dockerfile \
        -t $GCLOUD_REGION-docker.pkg.dev/$GCLOUD_PROJECT_ID/$REPO_NAME/$SERVICE_NAME:$IMAGE_TAG \
        --push .
}

# Function to deploy to Cloud Run
deploy_to_cloud_run() {
    echo "🚀 Deploying to Cloud Run..."
    gcloud run deploy ${SERVICE_NAME} \
        --image ${GCLOUD_REGION}-docker.pkg.dev/${GCLOUD_PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}:${IMAGE_TAG} \
        --region=${GCLOUD_REGION} \
        --min-instances=${MIN_INSTANCES:-0} \
        --max-instances=${MAX_INSTANCES:-4} \
        --memory=${MEMORY:-512Mi} \
        --cpu=${CPU:-1} \
        --port=${PORT:-8000} \
        --allow-unauthenticated
}

main() {
    echo "🚀 Starting deployment process..."
    
    # Check required variables
    check_required_vars
    
    # Run deployment steps
    setup_gcloud
    setup_artifact_registry
    build_and_push
    deploy_to_cloud_run
    
    echo "✅ Deployment completed successfully!"
}

# Run main function
main