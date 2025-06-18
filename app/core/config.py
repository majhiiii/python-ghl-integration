from pydantic import BaseModel
from pathlib import Path
import json

class AppConfig(BaseModel):
    baseUrl: str
    clientId: str
    clientSecret: str
    sharedSecretKey: str
    sos: str
    code: str
    access_token: str
    refreshToken: str
    userType: str
    companyId: str
    locationId: str
    scope: str
    expires_in: int
    userId: str

class ConfigManager:
    CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.json"

    @staticmethod
    def load_config() -> AppConfig:
        with open(ConfigManager.CONFIG_PATH, "r") as f:
            config_data = json.load(f)
        return AppConfig(**config_data)

    @staticmethod
    def save_config(config: AppConfig):
        with open(ConfigManager.CONFIG_PATH, "w") as f:
            json.dump(config.dict(), f, indent=4)

config = ConfigManager.load_config()
