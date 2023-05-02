from fastapi import FastAPI
from controller.getData import router as get_data
import uvicorn


app = FastAPI(
    title="TrendWise",
    description="Anlys topic and get trends",
    version="1.0.0"
)


if __name__ == "__main__":
  uvicorn.run("server.api:app", host="0.0.0.0", port=8000, reload=True)

  
@app.get("/healthz")
def get_request():
    return "Healthy"


routes=[get_data]
for route in routes:
  app.include_router(route)
