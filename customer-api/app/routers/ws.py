from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ..services.notification_manager import manager

router = APIRouter(prefix='/api/ws', tags=['websocket'])


@router.websocket('/notifications')
async def notifications_socket(websocket: WebSocket):
    user_id = websocket.query_params.get('user_id') or 'dev-user-id'
    await manager.connect(websocket, user_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
