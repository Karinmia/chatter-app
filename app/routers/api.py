import time
from typing import Annotated, Union

from fastapi import APIRouter, Depends, Request, WebSocket, Body, Response, status
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.dependencies import verify_session_token
from app.utils import generate_session_token, generate_random_user_name

api_router = APIRouter(prefix="/api")

# templates = Jinja2Templates(directory="templates")

@api_router.get("/db")
async def healthcheck(request: Request):
    print("api :: db")
    collections = await request.mongodb_client.list_database_names()
    return {
        "message": "Connected to database!",
        "collections": collections
    }


@api_router.get("/channels", dependencies=[Depends(verify_session_token)])
async def channels(channel_id: str):
    print("api :: channels")
    # context['channels'] = await get_channels_list(request.app.db)
    return {
        "status": "success",
        # "channels": session
    }

@api_router.get("/channels/{channel_id}/messages", dependencies=[Depends(verify_session_token)])
async def messages(channel_id: str, request: Request):
    print("api :: get messages")
    print(f"{channel_id = }")
    # context['channels'] = await get_channels_list(request.app.db)

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
    # return {
    #     "status": "success",
    #     "messages": messages
    # }


# @api_router.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @api_router.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}


# @api_router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was: {data}")