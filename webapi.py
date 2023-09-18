import uvicorn

from fastapi import FastAPI, Request, Response
from fastapi.encoders import jsonable_encoder
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from pydantic import BaseModel
from qianfan import QianFan

class RouteLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        print(f"request route: {request.url.path}")

        response = await call_next(request)
        return response

class ChatRequest(BaseModel):
    prompt: str


class ChatResponse(BaseModel):
    message: str


app = FastAPI()
app.add_middleware(RouteLoggingMiddleware)


@app.post("/chat",response_model=ChatResponse)
def chat(request: ChatRequest):
    print(f"get request:  {jsonable_encoder(request)}")
    qianfan = QianFan()
    response = qianfan(request.prompt)
    return {"message":f"{response}"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)