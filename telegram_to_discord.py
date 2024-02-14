import requests
from environment_control import *
import telebot
import json
from environment_control import *

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)

def refresh_settings():
    with open("./json/config.json","r") as config_json:
        config = json.load(config_json)
        config = config["discord_bridge"]
    return config

def bridge_message_embed(message):
    config = refresh_settings()
    photos = bot.get_user_profile_photos(message.from_user.id)
    pfp = photos.photos[0][0]
    url = bot.get_file_url(pfp.file_id)

    embed_bridge = requests.post(
                    f"https://discord.com/api/v9/channels/{BRIDGE_CHAT}/messages",
                    headers=headers,
                    json={"embeds": [{"title":f"{message.chat.title}" if config["chat_name_in_title"] else "","description":f"{message.text}","author":{"name":f"{message.from_user.username}","icon_url":url}}]}
                    )
    return embed_bridge

def bridge_photo_embed(message):
    config = refresh_settings()
    photos = bot.get_user_profile_photos(message.from_user.id)
    pfp = photos.photos[0][0]
    url = bot.get_file_url(pfp.file_id)
    photo_url = bot.get_file_url(message.photo[-1].file_id)
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
    return embed_bridge

def sticker_embed(message):
    photos = bot.get_user_profile_photos(message.from_user.id)
    pfp = photos.photos[0][0]
    url = bot.get_file_url(pfp.file_id)
    config = refresh_settings()
    sticker_url = bot.get_file_url(message.sticker.file_id)
        
    embed_bridge = requests.post(
                        f"https://discord.com/api/v9/channels/{BRIDGE_CHAT}/messages",
                        headers=headers,
                        json={"embeds": [{"title":f"{message.chat.title}" if config["chat_name_in_title"] else "",
                                            "author":{"name":f"{message.from_user.username}","icon_url":url},
                                            "image":{"url":sticker_url}
                            
                                }]})
                        

    return embed_bridge
    
def bridge_video(message):
    """Sends a video to discord via API call, currently the only way to send videos as you cannot use them in embeds. Returns request info"""
    config = refresh_settings()
    video = message.video
    video_url = bot.get_file_url(video.file_id)
    embed_bridge = requests.post(
                                f"https://discord.com/api/v9/channels/{BRIDGE_CHAT}/messages",
                                headers=headers,
                                data={"content":f"{message.from_user.username}: {video_url}"}
                                )
    return embed_bridge

def bridge_message(message):
    """Bridges a text-only message from telegram to discord"""
    send_message = requests.post(
                    f"https://discord.com/api/v6/channels/{BRIDGE}/messages",
                    headers=headers, 
                    json={"content": f"{message.from_user}{message.text}"}
                )
    return send_message

def bridge_response(response:str, embed:bool=False, embed_data:dict=None):
    """Takes a String response, and sends it to discord. If embeds are enabled, uses embed

    Args:
        response (Str): _description_
        embed (Bool, optional): . Defaults to None.
        embed_data (Dict, optional): Data for the embed, description, author, etc. Defaults to None.

    Returns:
        Dict: Response data from discord API call
    """
    if embed:
        send_message = requests.post(
            f"https://discord.com/api/v6/channels/{BRIDGE}/messages",
                    headers=headers, 
                        json={"embeds": [{"description":f"{response}", "author":{"name":f"{embed_data["author"]}","icon_url":embed_data["author_icon"]}}]}
        )
    else:
        send_message = requests.post(
                    f"https://discord.com/api/v6/channels/{BRIDGE}/messages",
                    headers=headers, 
                    json={"content": f"{response}"}
                )
    return send_message