from fastapi import Response
from src.schemas.users import  Token
from src.helpers.jwt import create_access_token
from src.helpers.hash import compare_password
from src.helpers.api_responses import APIResponses
from src.repository.users import UserRepository
from src.config.config import settings



# TOKEN_COOKIE_NAME = os.getenv("TOKEN_COOKIE_NAME")
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))



async def login( email: str, password: str, response: Response = None):
    #Verifica credenciales y devuelve token JWT
  
    user = await UserRepository.get_by_email( email)
    if not user:
        raise APIResponses(404, "Invalid credentials")
    
    # Verificar contraseña
    if not compare_password(password, user.password):
        raise APIResponses(401, "Invalid credentials")
    
    # Crear token (usamos email como identificador)
    access_token = create_access_token(data={
        "sub": user.email,
        "user_id": str(user.id),
        "is_admin": user.role
    })
    
    # Si se proporciona response, establecer cookie
    if response:
        response.set_cookie(
            key=settings.token_cookie_name,
            value=access_token,
            httponly=True,
            max_age=settings.access_token_expire_minutes * 60,
            secure=False,  # Cambia a True en producción con HTTPS
            samesite="None",
            # domain="localhost",  # Cambia según el dominio
            path="/",
        )
    
    return Token(access_token=access_token, token_type="bearer")

def logout(response: Response):
    response.delete_cookie(key=settings.token_cookie_name)
    return {"message": "Logout successful"}