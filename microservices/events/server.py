from fastapi import FastAPI
from .routes import eventRouter

app = FastAPI()
app.include_router(eventRouter)

@app.get("/health-check")
async def health_check():
    return {"success": True, "version": '0.0.0'}
