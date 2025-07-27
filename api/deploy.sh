#!/bin/bash

set -e

PROJECT_ID="meow-ai"
REGION="europe-west2"
REPO_NAME="meow-ai-api"
IMAGE_NAME="meow-ai-api"
SERVICE_NAME="meow-ai-api"
OPENAI_API_KEY="OPEN_AI_API_KEY"
STABILITY_API_KEY="STABILITY_API_KEY"
CATS_API_KEY="CATS_API_KEY"
# Tag image
docker tag $IMAGE_NAME $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME

# Push image
gcloud auth configure-docker $REGION-docker.pkg.dev
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME

# Deploy
gcloud run deploy $SERVICE_NAME \
  --image=$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME \
  --region=$REGION \
  --platform=managed \
  --memory=512Mi \
  --cpu=0.5 \
  --timeout=600 \
  --min-instances=0 \
  --max-instances=3 \
  --allow-unauthenticated \
  --set-secrets=OPENAI_API_KEY=OPENAI_API_KEY:latest \
  --set-secrets=STABILITY_API_KEY=STABILITY_API_KEY:latest \
  --set-secrets=CATS_API_KEY=CATS_API_KEY:latest