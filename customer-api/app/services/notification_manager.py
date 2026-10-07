from typing import Any, Dict, List

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections.setdefault(user_id, []).append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: str):
        if user_id in self.active_connections:
            self.active_connections[user_id] = [connection for connection in self.active_connections[user_id] if connection != websocket]
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send(self, user_id: str, payload: Dict[str, Any]):
        for connection in self.active_connections.get(user_id, []):
            await connection.send_json(payload)


manager = ConnectionManager()
