from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Request, HTTPException, status
from src.config.config import settings
from src.models.users import Users
from src.repository.users import UserRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    # 🔥 Convierte cualquier valor que no sea serializable (ObjectId, datetime, etc.)
    for key, value in to_encode.items():
        if not isinstance(value, (str, int, float, bool, type(None))):
            to_encode[key] = str(value)

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def verify_token(token: str):
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[settings.algorithm],
            options={"require_exp": True}  # Obligar a tener tiempo de expiración
        )
        return payload
    except ExpiredSignatureError:
        # Agrega información de depuración
        # print("Token expirado detectado")
        try:
            # Decodificar sin verificar expiración para diagnóstico
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm], options={"verify_exp": False})
            # print(f"Token expirado. Payload: {payload}")
            # print(f"Expirado en: {datetime.fromtimestamp(payload['exp'])}")
            # print(f"Hora actual: {datetime.utcnow()}")
        except Exception:
            pass
            
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        # print(f"JWTError: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )



def get_token_from_request(request: Request):
    # 1. Intentar obtener de headers
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    
    # 2. Intentar obtener de cookies
    cookie_token = request.cookies.get(settings.token_cookie_name)
    if cookie_token:
        # Si el token de la cookie incluye "Bearer", quitarlo
        if cookie_token.startswith("Bearer "):
            return cookie_token.split(" ")[1]
        return cookie_token
    
    return None

async def get_current_user(
    request: Request,  #  Recibe request como parámetro
    # db: Session = Depends(get_db)  # Usa Depends para la sesión
) -> Users:
    token = get_token_from_request(request)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token verification"
        )
    
    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    user = await UserRepository.get_by_email(email)
    # user_id = payload.get("user_id")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

