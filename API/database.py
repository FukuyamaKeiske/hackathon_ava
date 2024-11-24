from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from api.utils import hash_password, verify_password

client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client.HelpBusiness

async def register_user(email, password):
    if await db.Users.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(password)
    user_id = await db.Users.insert_one({
        "email": email,
        "password": hashed_password,
        "businesses": []
    })
    return str(user_id.inserted_id)

async def authenticate_user(email, password):
    db_user = await db.Users.find_one({"email": email})
    if not db_user or not verify_password(password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return str(db_user["_id"])

async def add_business(user_id, name, sphere, size, type_, specialization):
    business = {
        "name": name,
        "sphere": sphere,
        "size": size,
        "type": type_,
        "specialization": specialization,
        "messages": []
    }
    result = await db.Users.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"businesses": business}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

async def get_user_businesses(user_id):
    user = await db.Users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.get("businesses", [])

async def get_business_by_id(business_id):
    user = await db.Users.find_one({"businesses._id": ObjectId(business_id)})
    if not user:
        raise HTTPException(status_code=404, detail="Business not found")
    for business in user["businesses"]:
        if business["_id"] == ObjectId(business_id):
            return business
    raise HTTPException(status_code=404, detail="Business not found")
