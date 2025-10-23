from src.models.users import Users
from src.schemas.users import UserCreate, UserUpdate
from passlib.hash import bcrypt
from src.helpers.api_responses import DBError
from fastapi import HTTPException
import traceback

class UserRepository:
    @staticmethod
    async def create_user(user: Users):
        try:
            await user.create()
            await user.create_cart()

        # Convierte ObjectId a string y usa alias correcto
            user_dict = user.dict()
            user_dict["_id"] = str(user_dict.get("id"))  # 👈 importante
            user_dict.pop("id", None)

            return user_dict
        except Exception as e:
            print("❌ Error exacto al crear usuario:", e)
            raise e

    @staticmethod
    async def get_by_email(email: str):
        try:
            return await Users.find_one(Users.email == email)
        except Exception as e:
            raise DBError(f"Error fetching user by email: {e}")

    @staticmethod
    async def get_by_id(id: str):
        try:
            return await Users.get(id)
        except Exception as e:
            raise DBError(f"Error fetching user by id: {e}")

    @staticmethod
    async def get_all():
        try:
            return await Users.find_all().to_list()
        except Exception as e:
            raise DBError(f"Error fetching users: {e}")

    @staticmethod
    async def update_one(id: str, data: UserUpdate):
        try:
            user = await Users.get(id)
            if not user:
                return None

            update_data = data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(user, key, value)

            await user.save()
            return user
        except Exception as e:
            raise DBError(f"Error updating user: {e}")

    @staticmethod
    async def delete_one(id: str):
        try:
            user = await Users.get(id)
            if user:
                await user.delete()
                return True
            return False
        except Exception as e:
            raise DBError(f"Error deleting user: {e}")