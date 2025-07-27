set -a
source .env
set +a

docker build \
  --build-arg OPENAI_API_KEY=$OPENAI_API_KEY \
  --build-arg CATS_API_KEY=$CATS_API_KEY \
  --build-arg STABILITY_API_KEY=$STABILITY_API_KEY\
  -t meow-ai-api .