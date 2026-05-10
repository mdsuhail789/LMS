import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def get_tasks():
    client = AsyncIOMotorClient('mongodb://127.0.0.1:27017')
    db = client.learnflow
    tasks = await db.tasks.find({}).to_list(None)
    for t in tasks:
        print(f"Task: {t.get('title')}, Status: {t.get('status')}, Duration: {t.get('duration_minutes')}, Deadline: {t.get('deadline_date')} / {t.get('deadline')}")

asyncio.run(get_tasks())
