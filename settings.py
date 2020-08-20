import os

from dotenv import load_dotenv

load_dotenv()


# Class to hold common settings
class Settings:
    TOKEN = os.getenv('DISCORD_TOKEN')
    GOOGLE_SEARCH_ENGINE_KEY = os.getenv('GOOGLE_SEARCH_ENGINE_KEY')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')


# Can be improved to load different setting based on environment like development, production etc
settings = Settings()
