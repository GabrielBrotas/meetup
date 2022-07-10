from fastapi import FastAPI
import routes
import uvicorn

import models
import database

app = FastAPI()
app.include_router(routes.categoriesRouter)

def bind_models():
    print("models binding....")
    try:
        models.Base.metadata.create_all(bind=database.engine)
    except Exception as err:
        print("error on bind db")
        print(err)

@app.get("/health-check")
async def health_check():
    return {"success": True, "version": '0.0.0'}

if __name__ == "__main__":
    bind_models()
    print("app running")
    uvicorn.run(app, host="0.0.0.0", port=4001)