from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.auth import router as auth_router
from app.api.v1.contact import router as contact_router  # ✅ NEW

app = FastAPI(title="GHL OAuth FastAPI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(contact_router, prefix="/api/v1/contact", tags=["contact"])  # ✅ NEW

@app.get("/")
async def root():
    return {"message": "GHL OAuth FastAPI is running"}
