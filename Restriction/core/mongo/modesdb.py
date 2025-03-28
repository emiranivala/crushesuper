from config import MONGO_DB
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_DB)
db = mongo.modes
db = db.modes_db



async def get_mode_status(mode):
    setting = await db.find_one({"mode": mode})
    return setting["status"] if setting else False

async def set_mode_status(mode, status):
    await db.update_one({"mode": mode}, {"$set": {"status": status}}, upsert=True)
    setting = await db.find_one({"mode": mode})
    return setting["status"] if setting else False


