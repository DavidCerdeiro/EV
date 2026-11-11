import base64
from fastapi import APIRouter, Depends, HTTPException
import httpx
from requests import Session
from app.services.chat_service import response_to_user
from app.schemas.chat_schema import ChatRequest, ChatResponse
from fastapi.responses import RedirectResponse
import urllib.parse
from app.core.config import settings
from app.schemas.auth_schema import TokenPayload
from app.services.token_service import upsert_token
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get(
    "/google/login",
    summary="Initiate Google OAuth",
    response_description="Redirects the user to Google's OAuth service for authentication"
)
async def google_oauth():
    """
    Initiates the OAuth flow for Google authentication by redirecting the user to Google's OAuth service.

    **Parameters:**
    - None
    **Returns:**
    - A redirect response to Google's OAuth service.

    """
    params = urllib.parse.urlencode({
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/calendar.readonly https://www.googleapis.com/auth/gmail.readonly",
        "access_type": "offline",
        "prompt": "consent select_account",
        })
    return RedirectResponse(url="https://accounts.google.com/o/oauth2/v2/auth?" + params,
                            )

@router.get(
    "/google/callback",
    summary="Handle Google OAuth callback",
    response_description="Handles the callback from Google's OAuth service"
)
async def google_callback(code: str = None, 
    error: str = None, 
    db: Session = Depends(get_db)):
    """
    Handles the callback from Google's OAuth service.

    **Parameters:**
    - **request**: An object containing the authorization code returned by Google after user authentication.
    **Returns:**
    - None. The function processes the authorization code and stores the token in the database.
    """
    if error:
        raise HTTPException(status_code=400, detail=f"Acceso denegado: {error}")
    
    if not code:
        raise HTTPException(status_code=400, detail="No se recibió el código de autorización")

    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.GOOGLE_REDIRECT_URI
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=payload)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Error al intercambiar el token con Google")
        
    token_data = response.json()

    token = TokenPayload(
        application="google", 
        token=token_data.get("access_token"),
        refresh_token=token_data.get("refresh_token")
    )
    upsert_token(db, token)

    return {"message": "Autenticación completada con éxito. Ya puedes cerrar esta ventana."}

@router.get(
    "/spotify/login",
    summary="Initiate Spotify OAuth",
    response_description="Redirects the user to Spotify's OAuth service for authentication"
)
async def spotify():
    """
    Initiates the OAuth flow for Spotify authentication by redirecting the user to Spotify's OAuth service.

    **Parameters:**
    - None
    **Returns:**
    - A redirect response to Spotify's OAuth service.
    """

    params = urllib.parse.urlencode({
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
        "response_type": "code",
        "scope": "user-read-playback-state user-modify-playback-state user-read-currently-playing",
        })
    return RedirectResponse(url="https://accounts.spotify.com/authorize?" + params,
                            )


@router.get(
    "/spotify/callback",
    summary="Handle Spotify OAuth callback",
    response_description="Handles the callback from Spotify's OAuth service"
)
async def spotify_callback(code: str = None, 
    error: str = None, 
    db: Session = Depends(get_db)):
    """
    Handles the callback from Spotify's OAuth service.

    **Parameters:**
    - **request**: An object containing the authorization code returned by Spotify after user authentication.
    **Returns:**
    - None. The function processes the authorization code and stores the token in the database.
    """
    if error:
            raise HTTPException(status_code=400, detail=f"Acceso denegado: {error}")
        
    if not code:
        raise HTTPException(status_code=400, detail="No se recibió el código de autorización")
    
    token_url = "https://accounts.spotify.com/api/token"
    
    auth_string = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=payload, headers=headers)
        
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Error al intercambiar el token con Spotify")
            
    token_data = response.json()
    
    token = TokenPayload(
        application="spotify", 
        token=token_data.get("access_token"),
        refresh_token=token_data.get("refresh_token")
    )
    upsert_token(db, token)
    
    return {"message": "Autenticación completada con éxito. Ya puedes cerrar esta ventana."}
