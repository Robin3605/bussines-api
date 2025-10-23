from src.helpers.api_responses import APIResponses, ConflictError
from src.repository.users import UserRepository
from src.schemas.users import UserCreate, UserUpdate
from fastapi import HTTPException, status
from src.models.users import Users
from src.helpers.hash import hash_password
import traceback

class UserController:
    @staticmethod
    async def register_user(user_data: UserCreate):
        try:
            existing = await UserRepository.get_by_email(user_data.email)
            if existing:
                raise ConflictError("Email ya registrado")

            hashed_pwd = None
            if user_data.password:
                hashed_pwd = hash_password(user_data.password)
                
            new_user = Users(
                username=user_data.username,
                email=user_data.email,
                password=hashed_pwd,
            )

            user = await UserRepository.create_user(new_user)
            
            return user
        except Exception as e:
            print("❌ Error exacto al crear usuario:")
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Error creando usuario: {str(e)}")

    @staticmethod
    async def update_user(id: str, user_data: UserUpdate):
        try:
            existing = await UserRepository.get_by_id(id)
            if not existing:
                raise ConflictError("Usuario no encontrado")

            updated_user = await UserRepository.update_one(id, user_data)
            return updated_user
        except Exception as e:
            raise APIResponses(500, f"Error al actualizar usuario: {e}")

    @staticmethod
    async def get_all_users():
        try:
            users = await UserRepository.get_all()
            if not users:
                raise ConflictError("No hay usuarios creados")
            return users
        except Exception as e:
            raise APIResponses(500, f"Error al obtener usuarios: {e}")

    @staticmethod
    async def get_user_by_id(id: str):
        try:
            user = await UserRepository.get_by_id(id)
            if not user:
                raise ConflictError("Usuario no encontrado")
            return user
        except Exception as e:
            raise APIResponses(500, f"Error al obtener usuario: {e}")

    @staticmethod
    async def delete_user(id: str):
        try:
            existing = await UserRepository.get_by_id(id)
            if not existing:
                raise ConflictError("Usuario no encontrado")

            deleted = await UserRepository.delete_one(id)
            return True
        except Exception as e:
            raise APIResponses(500, f"Error al eliminar usuario: {e}")