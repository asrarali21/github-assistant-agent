import os
from dotenv import load_dotenv



load_dotenv()
class Settings :
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    SEARXNG_URL = os.getenv("SEARXNG_URL", "http://localhost:8080")
    
    def validate(self):
        if not self.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")
        if not self.GITHUB_TOKEN:
            raise ValueError("GITHUB_TOKEN is required")

settings = Settings()
settings.validate()