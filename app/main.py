from fastapi import FastAPI
import uvicorn
from controller.main_controller import router as get_data
from starlette.middleware.cors import CORSMiddleware
import os


app = FastAPI(
    title="TrendWise",
    description="Anlys topic and get trends",
    version="1.0.0"
)

allowed_methods = ["POST", "PUT", "GET"]

app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_methods=allowed_methods, allow_headers=["*"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("UVICORN_PORT", 8080)), reload=True)


@app.get("/healthz")
def get_request():
    return "Healthy"



routes=[get_data]
for route in routes:
  app.include_router(route)



