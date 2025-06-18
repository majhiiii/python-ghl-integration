from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from app.services.ghl_oauth import GHLAuthService
import json

router = APIRouter()

@router.get("/login")
async def login():
    """Redirect to GHL authorization page."""
    auth_url = GHLAuthService.get_authorization_url()
    return RedirectResponse(url=auth_url)

@router.get("/callback")
async def callback(code: str):
    """Handle GHL callback and exchange code for token."""
    try:
        token_data = await GHLAuthService.get_access_token(code)
        return token_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Callback error: {str(e)}")

@router.post("/get-access-token")
async def get_access_token():
    """Retrieve stored GHL access token."""
    try:
        return GHLAuthService.get_stored_token()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Access token error: {str(e)}")

@router.post("/refresh-token")
async def refresh_token():
    """Refresh GHL access token."""
    try:
        return await GHLAuthService.refresh_token()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token refresh error: {str(e)}")

@router.post("/webhook")
async def webhook(request: Request):
    try:
        headers = dict(request.headers)
        body = await request.body()

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            data = {"raw": body.decode()}

        log_entry = {
            "headers": headers,
            "data": data
        }

        print("📥 Webhook received:", json.dumps(log_entry, indent=2))

        with open("webhookResponse.txt", "a") as f:
            f.write(json.dumps(log_entry, indent=2) + "\n\n")

        return {"message": "Webhook data logged"}
    except Exception as e:
        print(f"❌ Webhook error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Webhook error: {str(e)}")


