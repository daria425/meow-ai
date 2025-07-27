
import asyncio
import signal
from contextlib import asynccontextmanager
from typing import Union
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse

from app.services.cat_cartoonizer import CatCartoonizerAgent
from app.services.websocket_manager import WebsocketManager
from app.config.settings import app_settings
from app.models.generation_run import GenerationRunComplete, GenerationRunError

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.background_tasks = set()
    def handle_exit(sig, frame):
        for task in app.state.background_tasks:
            task.cancel()
    
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    
    yield

    for task in app.state.background_tasks:
        task.cancel()

app=FastAPI(lifespan=lifespan)
ws_manager_instance=WebsocketManager()

origins=["http://localhost:3000", "http://localhost:5173", "https://responsible-youth-production.up.railway.app"]
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


@app.get("/api/cartoonize-cat/live/{session_id}", response_model=Union[GenerationRunComplete, GenerationRunError ])
async def get_cartoonized_cat_live(iterations:int, session_id:str):
    models=app_settings.models
    agent= CatCartoonizerAgent(
        models=models, 
    )
    if iterations>app_settings.max_iterations:
        iterations=app_settings.max_iterations
    results=await agent.run_generation_loop_live(iterations=iterations, session_id=session_id, ws_manager=ws_manager_instance)  
    if results.get("status")=="error":
        return JSONResponse(status_code=500, content=results)

    return results 

@app.websocket("/ws/cartoonize-cat/{session_id}")
async def ws_endpoint(websocket: WebSocket, session_id: str):
    await ws_manager_instance.connect(websocket=websocket, session_id=session_id)
    try:
        while True:
            await asyncio.sleep(60)  
    except WebSocketDisconnect:
        await ws_manager_instance.disconnect(session_id)

