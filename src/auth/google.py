from fastapi import HTTPException
from datetime import datetime
from src.models.users import Users
from src.helpers.google import verify_google_token
from src.helpers.jwt import create_access_token  #  función para crear JWT

async def login_with_google(google_token: str):
    # 1️ Verificamos el token
    user_data = await verify_google_token(google_token)

    # 2️ Buscamos si ya existe el usuario en DB
    existing_user = await Users.find_one({"email": user_data["email"]})

    # 3️ Si no existe, lo creamos
    if not existing_user:
        new_user = Users(
            username=user_data["username"],
            email=user_data["email"],
            google_id=user_data["google_id"],
            created_at=datetime.utcnow(),
        )
        await new_user.insert()
        user = new_user
    else:
        user = existing_user

    # 4️ Creamos el token JWT (con el ID del usuario)
    access_token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role,
        },
    }