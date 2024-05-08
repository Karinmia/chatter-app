from contextlib import asynccontextmanager
from typing import Annotated
import time

from fastapi import FastAPI, Request, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient

# from app.database import db
from app.routers.api import api_router
from app.routers.web import web_router
# from app.serializer import convert_doc_list
from app.database import get_channels_list, get_messages_mock
from app.utils import generate_random_user_name, generate_session_token

def timectime(s):
    return time.ctime(s) # datetime.datetime.fromtimestamp(s)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize templates
    app.templates = Jinja2Templates(directory="templates")
    app.templates.env.filters['ctime'] = timectime

    # Connect to the database
    app.mongodb_client = AsyncIOMotorClient("localhost", 27017)  # default connection
    app.db = app.mongodb_client.get_database("chatter_db")
    print("Connected to the MongoDB database!")
    channels = app.db.get_collection("channels")
    print("channels: ", channels)
    
    if not await app.db['channels'].count_documents({}):
        print("No channels found in the database. Creating new channels...")
        await app.db['channels'].insert_many([
            {"name": "Programming"},
            {"name": "Reading Club"},
            {"name": "Cats"},
            {"name": "Swimming"}
        ])
        print(f"Created {await app.db['channels'].count_documents({})} channels")
    yield
    # shut down database client
    app.mongodb_client.close()

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api_router, default_response_class=JSONResponse)
# app.include_router(web_router, include_in_schema=False)


@app.get("/", include_in_schema=False)
async def main(request: Request):
    """Check if user is logged in and redirect to the relevant endpoint"""
    
    context = {}
    session_token = request.cookies.get('X-Chatter-Token')
    if session_token:
        template_name = "app.html"
        context['name'] = request.cookies.get('X-Chatter-Name', generate_random_user_name())
        # get the list of channels from database
        context['channels'] = await get_channels_list(request.app.db)
        context['messages'] = get_messages_mock()
    else:
        template_name = "signup.html"
    
    return request.app.templates.TemplateResponse(
        request=request, name=template_name, context=context
    )


@app.post("/signup")
async def signup(user_name: Annotated[str, Body(embed=True)], request: Request):
    print("api :: signup")
    print(f"{user_name = }")
    if not user_name:
        return HTMLResponse('Name is required', status_code=400)
    
    response = request.app.templates.TemplateResponse(
        request=request, name="app.html", context={}
    )
    response.set_cookie(key="X-Chatter-Token", value=generate_session_token(), max_age=3600*24)
    response.set_cookie(key="X-Chatter-Name", value=user_name, max_age=3600*24)
    response.headers['HX-Redirect'] = 'http://127.0.0.1:8000/'
    return response
