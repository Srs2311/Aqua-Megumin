import telebot
import json
import requests
import os
from dotenv import load_dotenv
import time
import settings_management as sm

settings = sm.refresh_settings()
headers = {'Authorization': f"Bot {settings["tokens"]["discord"]}"}

def download_telegram_image(bot,message,destination="./pictures/",name=None):
    #downloads the photo from telegram
    if message.reply_to_message:
        photo_info = bot.get_file(message.reply_to_message.photo[-1].file_id)
    elif message.photo:
        photo_info = bot.get_file(message.photo[-1].file_id)
    r = requests.get(f"https://api.telegram.org/file/bot{settings["tokens"]["telegram"]}/{photo_info.file_path}",allow_redirects=True)
    if name == None:
        open(f"./{destination}/{photo_info.file_unique_id}.png","wb").write(r.content)
    else:
        open(f"./{destination}/{name}.png","wb").write(r.content)

def send_photo_to_discord(channel,image_path,message_text):
    requests.post(
        f"https://discord.com/api/v9/channels/{channel}/messages",
        headers=headers,
        files = {
            (image_path, open(image_path, 'rb'))
        },
        data={"content": f"{message_text}" if message_text != None else ""}
        ) 

def send_discord_message(channel,text):
    requests.post(
        f"https://discord.com/api/v9/channels/{channel}/messages",
        headers=headers,
        data={"content": text}
        ) 

def add_photo(bot, message):
    if message.reply_to_message:
        messageText = message.text
        messageText = messageText.replace("/addphoto ","")       
    elif message.caption:
        messageText = message.caption
        messageText = messageText.replace("/addphoto ","")
    
    #if the file exists in the image library, it is downloaded and sent to the image library
    if os.path.exists(f"./image_library/{messageText}.png") == False:
        download_telegram_image(bot,message,destination="./image_library/",name=messageText)
        send_photo_to_discord(settings["discord_settings"]["image_library"],f"./image_library/{messageText}.png",messageText)
        bot.send_message(message.chat.id,f"Added photo: {messageText}")
    else:
        bot.send_message(message.chat.id,"Photo with that name already exists")   
                 
def send_image_from_library(bot,message):
    name = str(message.text).replace("/img ","")
    if os.path.exists(f"./image_library/{name}.png"):
        bot.send_photo(message.chat.id,photo=open(f"./image_library/{name}.png","rb"))
        send_photo_to_discord(settings["discord_bridge"]["discord_bridge_chat"],f"./image_library/{name}.png",(str(message.caption) if message.caption else ""))
    else:
        print(f"Could not find file {name}.png")

def generate_image_library():
    for file in os.listdir("./image_library"):
        file_path = os.path.join("./image_library",file)
        file_name = str(file).replace(".png","")
        send_photo_to_discord(settings["discord_settings"]["image_library"],file_path,file_name)
        time.sleep(1)