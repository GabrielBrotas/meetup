from fastapi import FastAPI
import routes
import uvicorn

import models
import database

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()
app.include_router(routes.categoriesRouter)

@app.get("/health-check")
async def health_check():
    return {"success": True, "version": '0.0.0'}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4001)