from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.db.mongodb import close_mongo_connection, connect_to_mongo
from app.routes import auth, courses, dashboard, learnflow, planner, tasks, users


@asynccontextmanager
async def lifespan(_: FastAPI):
    await connect_to_mongo()
    from app.db.mongodb import get_database
    db = get_database()
    if db is not None:
        await db.tasks.create_index([("user_id", 1), ("status", 1)])
        await db.tasks.create_index([("deadline_date", 1), ("deadline", 1)])
        await db.tasks.create_index([("user_id", 1), ("deadline_date", 1)])
        await db.course_progress.create_index([("user_id", 1), ("course_id", 1)])
        await db.planner_blocks.create_index([("user_id", 1), ("day", 1)], unique=True)
    yield
    await close_mongo_connection()


app = FastAPI(title="LearnFlow LMS API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(tasks.router)
app.include_router(planner.router)
app.include_router(dashboard.router)
app.include_router(learnflow.router)


@app.get("/")
async def root() -> dict:
    return {"message": "LMS backend is running"}
