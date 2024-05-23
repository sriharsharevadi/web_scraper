# main.py

from fastapi import FastAPI
from database import database, engine
from models import Base
from views import router

app = FastAPI()


# Startup and shutdown events for database connection
@app.on_event("startup")
async def startup():
    await database.connect()
    Base.metadata.create_all(bind=engine)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Mount the router onto your FastAPI instance
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
