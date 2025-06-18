import asyncio
from app.core.config import config
import httpx

BASE_URL = "https://services.leadconnectorhq.com"
VERSION = "2021-07-28"

def get_headers():
    if not config.access_token:
        raise ValueError("No access token available. Please run the OAuth login flow first.")
    return {
        "Authorization": f"Bearer {config.access_token}",
        "Content-Type": "application/json",
        "Version": VERSION
    }

async def create_demo_contact():
    payload = {
        "firstName": "Demo",
        "lastName": "Contact",
        "name": "Demo Contact",
        "email": "demo@example.com",
        "phone": "+1 9876543210",
        "locationId": config.locationId,
        "city": "Pune",
        "state": "MH",
        "postalCode": "411001",
        "country": "IN",
        "source": "demo_script",
        "tags": ["test", "demo"],
        "dnd": False
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/contacts/",
            json=payload,
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    try:
        print("Creating demo contact...")
        result = asyncio.run(create_demo_contact())
        print(" Contact created successfully:")
        print(result)
    except Exception as e:
        print(f" Error: {str(e)}")
