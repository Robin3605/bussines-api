from src.models.users import Users
from src.schemas.users import  UserUpdate
from src.helpers.api_responses import DBError



class UserRepository:
    @staticmethod
    def serialize_user(user):
        data = user.dict()
        data["_id"] = str(user.id)
        data["cart_id"] = str(user.cart_id) if user.cart_id else None
        data.pop("id", None)
        return data

    @staticmethod
    async def create_user(user: Users):
        try:
            saved_user = await user.insert()
            await saved_user.create_cart()

            print("🧠 ID real:", saved_user.id)

            user_dict = saved_user.dict()
            user_dict["_id"] = str(saved_user.id) if saved_user.id else None
            user_dict["cart_id"] = str(saved_user.cart_id) if saved_user.cart_id else None
            user_dict.pop("id", None)

            print("✅ user_dict final:", user_dict)
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