from fastapi import FastAPI
import uvicorn
from controller.getData import router as get_data
from starlette.middleware.cors import CORSMiddleware
import os
import subprocess


app = FastAPI(
    title="TrendWise",
    description="Anlys topic and get trends",
    version="1.0.0"
)

allowed_methods = ["POST", "PUT", "GET"]

app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_methods=allowed_methods, allow_headers=["*"])




if __name__ == "__main__":
    routes=[get_data]
    for route in routes:
        app.include_router(route)

    @app.get("/healthz")
    def get_request():
        return "Healthy"

    # start uvicorn in a separate process
    uvicorn_command = [
        "uvicorn",
        "main:app",
        "--host", "0.0.0.0",
        "--port", str(int(os.environ.get("UVICORN_PORT", 8080))),
        "--reload",
    ]
    uvicorn_process = subprocess.Popen(uvicorn_command)

    # start the Streamlit app
    streamlit_command = [
        "streamlit", "run", "my_app.py",
        "--server.enableCORS", "false",
        "--server.port", "8501",
    ]
    streamlit_process = subprocess.Popen(streamlit_command)

    # wait for both processes to finish
    uvicorn_process.wait()
    streamlit_process.wait()


