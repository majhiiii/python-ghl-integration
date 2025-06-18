# app/api/v1/contacts.py
from fastapi import APIRouter, HTTPException
from app.core.config import config
import httpx

router = APIRouter()

BASE_URL = "https://services.leadconnectorhq.com"


def get_headers():
    if not config.access_token:
        raise HTTPException(status_code=401, detail="No access token available.")
    return {
        "Authorization": f"Bearer {config.access_token}",
        "Content-Type": "application/json",
        "Version": "2021-07-28"
    }


@router.post("/create")
async def create_contact(payload: dict):
    """Create a new contact (locationId required in body)."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/contacts/",
                json=payload,
                headers=get_headers()
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@router.get("/{contact_id}")
async def get_contact(contact_id: str):
    """Get contact details by ID."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/contacts/{contact_id}",
                headers=get_headers()
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@router.put("/{contact_id}")
async def update_contact(contact_id: str, payload: dict):
    """Update contact by ID."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{BASE_URL}/contacts/{contact_id}",
                json=payload,
                headers=get_headers()
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@router.delete("/{contact_id}")
async def delete_contact(contact_id: str):
    """Delete contact by ID."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{BASE_URL}/contacts/{contact_id}",
                headers=get_headers()
            )
            response.raise_for_status()
            return {"message": f"Contact {contact_id} deleted successfully."}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
