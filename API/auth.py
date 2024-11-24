from fastapi import APIRouter
from models import UserRegister, UserLogin
from database import register_user, authenticate_user

router = APIRouter()


@router.post("/register")
async def register(user: UserRegister):
    user_id = await register_user(user.email, user.password)
    return {"user_id": user_id}


@router.post("/login")
async def login(user: UserLogin):
    user_id = await authenticate_user(user.email, user.password)
    return {"user_id": user_id}
