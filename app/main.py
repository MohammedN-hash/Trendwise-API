from fastapi import FastAPI
import uvicorn
from controller.getData import router as get_data




app = FastAPI(
    title="TrendWise",
    description="Anlys topic and get trends",
    version="1.0.0"
)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("UVICORN_PORT", 8080)), reload=True)


@app.get("/healthz")
def get_request():
    return "Healthy"



routes=[get_data]
for route in routes:
  app.include_router(route)



