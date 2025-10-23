from fastapi import APIRouter, Body, Response, Request
from src.auth.google import login_with_google
from src.auth.auth import login, logout
from src.schemas.users import  UserResponse, Token, User_login
from src.auth.auth import get_current_user
from fastapi import HTTPException

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/google-login")
async def google_login(google_token: str = Body(..., embed=True)):
    #Inicia sesión o registra un usuario usando Google.
    return await login_with_google(google_token)

@router.post("/login", response_model=Token)
async def login_user(user_data: User_login,  response: Response = None):
    # print(f"Response object in login_user: {response}")
    return await login( user_data.email, user_data.password, response)

@router.post("/logout")
async def logout_user(response: Response):
    logout(response)

    return {"message": "Logout successful"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    request: Request,
    
):
    #Obtiene el perfil del usuario autenticado
    # print(f"Request cookies: {request.cookies}")
    user = await get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user