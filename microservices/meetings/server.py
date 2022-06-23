from fastapi import FastAPI
import routes
import uvicorn

import database

app = FastAPI()
app.include_router(routes.meetingsRouter)

@app.get("/health-check")
async def health_check():
    return {"success": True, "version": '0.0.0'}

if __name__ == "__main__":
    conn = database.create_server_connection()
    database.create_tables(conn)
    uvicorn.run(app, host="0.0.0.0", port=4002)