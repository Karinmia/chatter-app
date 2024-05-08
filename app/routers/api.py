import time
from typing import Annotated, Union

from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect, Response, status
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse

from app.database import get_channels_list
from app.dependencies import verify_session_token
from app.schemas import Channel
from app.utils import generate_random_user_name
from app.websocket import ConnectionManager

api_router = APIRouter(prefix="/api")


@api_router.get("/db")
async def healthcheck(request: Request):
    print("api :: db")
    collections = await request.mongodb_client.list_database_names()
    return {
        "message": "Connected to database!",
        "collections": collections
    }


@api_router.get("/channels", dependencies=[Depends(verify_session_token)])
async def channels(request: Request) -> list[Channel]:
    return await get_channels_list(request.app.db)

@api_router.get("/channels/{channel_id}/messages", dependencies=[Depends(verify_session_token)])
async def messages(channel_id: str, request: Request):
    messages = [
        {
            "channel_id": channel_id,
            "author": generate_random_user_name(),
            "content": "Hi there! This is a test message!",
            "timestamp": time.time()
        },
        {
            "channel_id": channel_id,
            "author": generate_random_user_name(),
            "content": "Hi! What's up?",
            "timestamp": time.time()
        },
        {
            "channel_id": channel_id,
            "author": generate_random_user_name(),
            "content": "Hi guys. I'm learning FastAPI here. Wanna join?",
            "timestamp": time.time()
        }
    ]
    return request.app.templates.TemplateResponse(
        request=request, name="messages.html", context={'messages': messages}
    )

manager = ConnectionManager()

@api_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            print(f"--- received message from websocket: {data}")
            # await manager.send_personal_message(data, websocket)
            await manager.broadcast_json(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # await manager.broadcast(f"Client ??? left the chat")