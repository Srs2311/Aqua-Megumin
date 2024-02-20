import json
from dotenv import load_dotenv
import os


load_dotenv("./dev.env")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT = str(os.environ.get("TELEGRAM_CHAT"))
IMAGE_LIBRARY = int(os.environ.get("IMAGE_LIBRARY"))
DISCORD_BRIDGE_CHANNEL = os.environ.get("DISCORD_BRIDGE_CHANNEL")
ROLE_CHAT = int(os.environ.get("ROLE_CHAT"))

def create_new_config():
    
    sample_config = {
    "discord_bridge": {
        "use_embeds": True,
        "chat_name_in_title": False,
        "discord_bridge_chat": DISCORD_BRIDGE_CHANNEL
    },
    "telegram_bridge": {
        "bridge_nsfw_channels": False,
        "telegram_chat": TELEGRAM_CHAT,
        "ignored_channels": [
            {
            }
        ],
        "ignored_users": [
            {}
        ]
    },
    "discord_settings": {
        "image_library": IMAGE_LIBRARY,
        "role_chat": ROLE_CHAT
    },
    "tokens": {
        "telegram": TELEGRAM_TOKEN,
        "discord": DISCORD_TOKEN
    }
}
    with open("./json/config.json","w") as settings:
        json.dump(sample_config,settings)

def refresh_settings():
    settings = {}
    try:
        with open("./json/config.json","r") as settings:
            settings = json.load(settings)
    except(FileNotFoundError):
        create_new_config()
        with open("./json/config.json","r") as settings:
            settings = json.load(settings)
    
    return settings

def get_ignored_discord_channels():
    settings = refresh_settings
    ignored_channel_ids = []
    for channel in settings["telegram_bridge"]["ignored_channels"]:
        ignored_channel_ids.append(channel.get("id",None))
    return ignored_channel_ids

refresh_settings()