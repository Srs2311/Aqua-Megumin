from dotenv import load_dotenv
import os


load_dotenv("./dev.env")

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
chat_id = str(os.environ.get("TELEGRAM_CHAT"))
TELEGRAM_CHAT = str(os.environ.get("TELEGRAM_CHAT"))
BRIDGE_CHAT = int(os.environ.get("BRIDGE"))
IMAGE_LIBRARY = int(os.environ.get("IMAGE_LIBRARY"))
BRIDGE = os.environ.get("BRIDGE")
ROLE_CHAT = int(os.environ.get("ROLE_CHAT"))

headers = {'Authorization': f"Bot {DISCORD_TOKEN}"}