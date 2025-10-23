from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import HTTPException
from src.config.config import settings

# GOOGLE_CLIENT_ID = "TU_GOOGLE_CLIENT_ID.apps.googleusercontent.com"

async def verify_google_token(token: str):
    """
    Verifica la validez del token de Google y devuelve la info del usuario.
    """
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.google_client_id)

        if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
            raise HTTPException(status_code=400, detail="Token de Google inválido")

        # Retorna la información principal del usuario
        return {
            "google_id": idinfo["sub"],
            "email": idinfo["email"],
            "username": idinfo.get("name", idinfo["email"].split("@")[0]),
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error verificando token de Google: {e}")