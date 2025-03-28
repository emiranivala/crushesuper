from config import MONGO_DB
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_DB)
db = mongo.shopes
collection = db.shopes_db




async def get_user_data(user_id):
    user_data = await collection.find_one({"_id": user_id})
    
    if user_data:
        user_data["coins"] = user_data.get("coins", 0)
        user_data["reffers_id"] = user_data.get("reffers_id", [])
        user_data["customers"] = user_data.get("customers", [])
        user_data["weekly_rewards"] = user_data.get("weekly_rewards", None)
    else:
        user_data = {
            "_id": user_id,
            "coins": 0,
            "reffers_id": [],
            "customers": [],
            "weekly_rewards": None
        }

    return user_data
    


async def user_store(user_id, coin):
    existing_user = await collection.find_one({"_id": user_id})
    if existing_user:
        await collection.update_one(
            {"_id": user_id},
            {"$inc": {"coins": coin}}
        )
    else:
        await collection.insert_one({"_id": user_id, "coins": coin})




async def add_reffers(user_id, reffer_id):
    await collection.update_one(
        {"_id": user_id},
        {"$addToSet": {"reffers_id": reffer_id}},
        upsert=True
    )


async def weekly_rewards(user_id, time):
    await collection.update_one(
        {'_id' : user_id},
        {'$set' : {'weekly_rewards' : time}},
        upsert=True
    )



async def remove_shop_user(user_id):
    user = await collection.find_one({"_id": user_id})
    
    if user:
        result = await collection.delete_one({"_id": user_id})
        return True
    else:
        return False
        


async def add_customer(user_id, customer_id, customer_name, customer_time, customer_expiry):
    customer_data = {
        "customers.$.customer_id": customer_id,
        "customers.$.customer_name": customer_name,
        "customers.$.customer_time": customer_time,
        "customers.$.customer_expiry": customer_expiry
    }

    result = await collection.update_one(
        {
            "_id": user_id,
            "customers.customer_id": customer_id
        },
        {
            "$set": customer_data
        }
    )

    if result.matched_count == 0:
        customer_data = {
            "customer_id": customer_id,
            "customer_name": customer_name,
            "customer_time": customer_time,
            "customer_expiry": customer_expiry
        }

        await collection.update_one(
            {"_id": user_id},
            {"$push": {"customers": customer_data}},
            upsert=True
        )




async def shop_users():
    id_list = []
    async for user in collection.find():
        id_list.append(user["_id"])
    return id_list



async def remove_customer(user_id, customer_id):
    result = await collection.update_one(
        {"_id": user_id},
        {"$pull": {"customers": {"customer_id": customer_id}}}
    )
    
    if result.matched_count > 0 and result.modified_count > 0:
        return True
    else:
        return False







