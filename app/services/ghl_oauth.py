import httpx
from fastapi import HTTPException
from urllib.parse import urlencode
from app.core.config import config, ConfigManager

class GHLAuthService:
    REDIRECT_URI = "http://localhost:8000/api/v1/auth/callback"

    @staticmethod
    def get_authorization_url():
        params = {
            "response_type": "code",
            "redirect_uri": GHLAuthService.REDIRECT_URI,
            "client_id": config.clientId,
            "scope": config.scope
        }
        return f"{config.baseUrl}/oauth/chooselocation?{urlencode(params)}"

    @staticmethod
    async def get_access_token(code: str):
        async with httpx.AsyncClient() as client:
            payload = {
                "client_id": config.clientId,
                "client_secret": config.clientSecret,
                "grant_type": "authorization_code",
                "code": code,
                "user_type": config.userType,
                "redirect_uri": GHLAuthService.REDIRECT_URI
            }
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            response = await client.post("https://services.leadconnectorhq.com/oauth/token", data=payload, headers=headers)
            response.raise_for_status()
            token_data = response.json()

            # Save token to config
            config.code = code
            config.access_token = token_data.get("access_token", "")
            config.refreshToken = token_data.get("refresh_token", "")
            config.expires_in = token_data.get("expires_in", 86399)
            config.userType = token_data.get("userType", config.userType)
            config.companyId = token_data.get("companyId", "")
            config.locationId = token_data.get("locationId", "")
            config.userId = token_data.get("userId", "")
            ConfigManager.save_config(config)

            return token_data

    @staticmethod
    async def refresh_token():
        async with httpx.AsyncClient() as client:
            payload = {
                "client_id": config.clientId,
                "client_secret": config.clientSecret,
                "grant_type": "refresh_token",
                "refresh_token": config.refreshToken,
                "user_type": config.userType
            }
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            response = await client.post("https://services.leadconnectorhq.com/oauth/token", data=payload, headers=headers)
            response.raise_for_status()
            token_data = response.json()

            config.access_token = token_data.get("access_token", "")
            config.refreshToken = token_data.get("refresh_token", config.refreshToken)
            config.expires_in = token_data.get("expires_in", 86399)
            config.userType = token_data.get("userType", config.userType)
            config.companyId = token_data.get("companyId", "")
            config.locationId = token_data.get("locationId", "")
            config.userId = token_data.get("userId", "")
            ConfigManager.save_config(config)

            return token_data

    @staticmethod
    def get_stored_token():
        if not config.access_token:
            raise HTTPException(status_code=400, detail="No access token available. Please authorize first.")
        return {
            "access_token": config.access_token,
            "refresh_token": config.refreshToken,
            "token_type": "Bearer",
            "expires_in": config.expires_in,
            "scope": config.scope,
            "userType": config.userType,
            "companyId": config.companyId,
            "locationId": config.locationId,
            "userId": config.userId
        }
