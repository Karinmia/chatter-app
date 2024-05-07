from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# from app.database import client

web_router = APIRouter()

# @web_router.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):
#     print("web router")
#     return templates.TemplateResponse(
#         request=request, name="index.html"
#         # request=request, name="index.html", context={"id": id}
#     )
