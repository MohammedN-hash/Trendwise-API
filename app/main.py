from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from starlette.middleware.cors import CORSMiddleware
from controller.getData import router as get_data


app = FastAPI(
    title="TrendWise",
    description="Anlys topic and get trends",
    version="1.0.0"
)

allowed_methods = ["POST", "GET"]

app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_methods=allowed_methods, allow_headers=["*"])


@app.get("/healthz")
def get_request():
    return PlainTextResponse("Healthy")


routes=[get_data]
for route in routes:
  app.include_router(route)
