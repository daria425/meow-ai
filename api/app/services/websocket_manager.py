from app.utils.logger import logger
import asyncio
from fastapi.websockets import WebSocket
class WebsocketManager:
    def __init__(self):
        self.clients = {}
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, session_id:str):
        await websocket.accept()
        logger.info(f"Websocket for session {session_id} connected")
        async with self.lock:
            self.clients[session_id]=websocket
    
    async def disconnect(self,session_id:str):
        async with self.lock:
            self.clients.pop(session_id, None)

    async def notify(self, session_id, message):
        async with self.lock:
            ws=self.clients.get(session_id)
            if not ws:
                return False
            try:
                logger.info(f"Sending message from websocket to session {session_id}")
                await ws.send_json(message)
                return True
            except RuntimeError as e:
                if "close" in str(e):
                    logger.warning(f"WebSocket connection closed for session {session_id}: {str(e)}")
                    self.clients.pop(session_id, None)
                    return False
            except Exception as e:
                logger.error(f"Error sending message to session {session_id}: {str(e)}")
                return False
        
    def has_active_connection(self, session_id: str) -> bool:
        return session_id in self.clients