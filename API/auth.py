from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from api.database import (
    register_user,
    authenticate_user,
    add_business,
    get_user_businesses,
    get_business_by_id
)

router = APIRouter()

class UserRegisterRequest(BaseModel):
    email: str
    password: str

class UserAuthRequest(BaseModel):
    email: str
    password: str

class BusinessRequest(BaseModel):
    user_id: str
    name: str
    sphere: str
    size: str
    type_: str
    specialization: str

@router.post("/register")
async def register_user_api(request: UserRegisterRequest):
    try:
        user_id = await register_user(request.email, request.password)
        return {"user_id": user_id}
    except HTTPException as e:
        raise e

@router.post("/authenticate")
async def authenticate_user_api(request: UserAuthRequest):
    try:
        user_id = await authenticate_user(request.email, request.password)
        return {"user_id": user_id}
    except HTTPException as e:
        raise e

@router.post("/add_business")
async def add_business_api(request: BusinessRequest):
    try:
        await add_business(
            request.user_id,
            request.name,
            request.sphere,
            request.size,
            request.type_,
            request.specialization
        )
        return {"message": "Business added successfully"}
    except HTTPException as e:
        raise e

@router.get("/user_businesses/{user_id}")
async def get_user_businesses_api(user_id: str):
    try:
        businesses = await get_user_businesses(user_id)
        return {"businesses": businesses}
    except HTTPException as e:
        raise e

@router.get("/business/{business_id}")
async def get_business_by_id_api(business_id: str):
    try:
        business = await get_business_by_id(business_id)
        return {"business": business}
    except HTTPException as e:
        raise e

@router.get("/user_messages/{user_id}")
async def get_all_user_messages_api(user_id: str):
    try:
        messages = await get_all_user_messages(user_id)
        return {"messages": messages}
    except HTTPException as e:
        raise e
