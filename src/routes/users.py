from fastapi import APIRouter, HTTPException
from src.schemas.users import UserCreate, UserResponse, UserUpdate
from src.controllers.users import UserController
from src.helpers.api_responses import APIResponses
from typing import List
from src.repository.users import UserRepository



router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
async def register_user(user_data: UserCreate):
    try:
        user = await UserController.register_user(user_data)
        return user
    except Exception as e:
        print("❌ Error exacto al crear usuario:", e)
        raise HTTPException(status_code=500, detail=f"Error creando usuario: {e}")

@router.get("/", response_model=List[UserResponse])
async def get_all_users_in_db():
    try:
        users = await UserController.get_all_users()
        return [UserRepository.serialize_user(user) for user in users]
    except Exception as e:
        print("❌ Error exacto al crear usuario:", e)
        raise HTTPException(status_code=500, detail=f"Error creando usuario: {e}")

@router.get("/{id}", response_model=UserResponse)
async def get_one_user_by_id(id: str):
    try:
        user = await UserController.get_user_by_id(id)
        return UserRepository.serialize_user(user)
    except Exception as e:
        print("❌ Error exacto al crear usuario:", e)
        raise HTTPException(status_code=500, detail=f"Error creando usuario: {e}")

@router.put("/{id}", response_model=UserResponse)
async def update_one_user(id: str, user_data: UserUpdate):
    try:
        user = await UserController.update_user(id, user_data)
        return UserRepository.serialize_user(user)
    except Exception as e:
        print("❌ Error exacto al crear usuario:", e)
        raise HTTPException(status_code=500, detail=f"Error creando usuario: {e}")

@router.delete("/{id}")
async def delete_one_user(id: str):
    try:
        user = await UserController.delete_user(id)
        return {"message": "Usuario eliminado correctamente"}
    except Exception as e:
        print("❌ Error exacto al crear usuario:", e)
        raise HTTPException(status_code=500, detail=f"Error creando usuario: {e}")