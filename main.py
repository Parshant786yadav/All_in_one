import os
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

# So LLM Chatbot Backend loads .env and uses correct OAuth redirect URI when mounted
os.environ.setdefault("LLM_CHATBOT_MOUNT_PATH", "/llm-chatbot")

from hirewise.app import app as hirewise_app
from LLM_Chatbot.Backend.main import app as chatbot_app
from personal_ml_chatbot.backend.app import app as ml_chatbot_app


app = FastAPI()


@app.get("/")
def home():
    return {"message": "All AI projects running"}


# Fix for Flask apps running under a prefix
class PrefixMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, prefix: str):
        super().__init__(app)
        self.prefix = prefix

    async def dispatch(self, request, call_next):
        request.scope["root_path"] = self.prefix
        response = await call_next(request)
        return response


# WSGI wrapper so Flask sees SCRIPT_NAME and url_for() generates /hirewise/... URLs
def _wsgi_with_script_name(wsgi_app, prefix: str):
    def wrapped(environ, start_response):
        environ["SCRIPT_NAME"] = prefix.rstrip("/")
        # PATH_INFO should be the path after the prefix (Starlette usually does this)
        return wsgi_app(environ, start_response)
    return wrapped

hirewise_mount = WSGIMiddleware(_wsgi_with_script_name(hirewise_app, "/hirewise"))
app.mount("/hirewise", hirewise_mount)


# Mount LLM Chatbot (FastAPI)
app.mount("/llm-chatbot", chatbot_app)


# Mount ML Chatbot (Flask) with prefix so links work
ml_mount = WSGIMiddleware(_wsgi_with_script_name(ml_chatbot_app, "/ml-chatbot"))
app.mount("/ml-chatbot", ml_mount)