import telebot
import requests
import json
from environment_control import *

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)

def refresh_settings():
    with open("./json/config.json","r") as config_json:
        config = json.load(config_json)
        config = config["discord_bridge"]
    return config

def create_embed(message):
    config = refresh_settings()
    description = str(message.text)
    name = str(message.from_user.username)
    photos = bot.get_user_profile_photos(message.from_user.id)
    pfp = photos.photos[0][0]
    url = bot.get_file_url(pfp.file_id)


    embed_bridge = requests.post(
                    f"https://discord.com/api/v9/channels/{BRIDGE_CHAT}/messages",
                    headers=headers,
                    json={"embeds": [{"title":f"{message.chat.title}" if config["chat_name_in_title"] else "","description":f"{message.text}","author":{"name":f"{message.from_user.username}","icon_url":url}}]}
                    )
    return embed_bridge

def photo_embed(message):
    config = refresh_settings()
    photos = bot.get_user_profile_photos(message.from_user.id)
    pfp = photos.photos[0][0]
    url = bot.get_file_url(pfp.file_id)
    photo_url = bot.get_file_url(message.photo[-1].file_id)
    print(photo_url)
    embed_bridge = requests.post(
                    f"https://discord.com/api/v9/channels/{BRIDGE_CHAT}/messages",
    headers=headers,
    json={"embeds": [{"title":f"{message.chat.title}" if config["chat_name_in_title"] else "",
                        "description":f"{message.caption if message.caption else ""}",
                        "author":{"name":f"{message.from_user.username}","icon_url":url},
                        "image":{"url":photo_url}
                    }]
        }
    )
    print(embed_bridge.content)
    return embed_bridge

def video_embed(message):
    photos = bot.get_user_profile_photos(message.from_user.id)
    pfp = photos.photos[0][0]
    url = bot.get_file_url(pfp.file_id)
    config = refresh_settings()
    print(message.video)
    video = message.video
    video_url = bot.get_file_url(video.file_id)
    print(video_url)
    embed_bridge = requests.post(
                                f"https://discord.com/api/v9/channels/{BRIDGE_CHAT}/messages",
                                headers=headers,
                                data={"content":f"{message.from_user.username}: {video_url}"}
                                )
    print(embed_bridge.content)