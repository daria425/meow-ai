
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.services.cat_cartoonizer import CatCartoonizerAgent
from app.config.settings import app_settings
from app.models.generation_run import GenerationRun

app=FastAPI()

origins=["http://localhost:3000", "http://localhost:5173", "https://some-public-frontend.vercel.app"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return RedirectResponse(url="/api/health")
@app.get("/api/health")
def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "ok", "message": "API is running"}

@app.get("/api/cartoonize-cat", response_model=GenerationRun)
def get_cartoonized_cat(iterations:int):
    models=app_settings.models
    agent= CatCartoonizerAgent(
        models=models, 
    )
    if iterations>app_settings.max_iterations:
        iterations=app_settings.max_iterations
    results=agent.run_generation_loop(iterations=iterations)  
    return results