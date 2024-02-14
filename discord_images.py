import discord
import json
import requests
import telebot
from environment_control import *

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

async def add_photo(self,message,image_gallery):
    if len(message.attachments) > 0:
        if message.attachments[0]:
            photo_name = str(message.content).replace("/addphoto ","")
            photo_url = str(message.attachments[0])
            img_data = requests.get(photo_url).content
            with open(f"./image_library/{photo_name}.png", "wb") as saved_image:
                saved_image.write(img_data)
            await message.channel.send(f"Adding Photo {photo_name}")
            image_gallery.send(file=discord.File(f"./image_library/{photo_name}.png"))
            
        
async def send_image(self,message):
    image_request = str(message.content).replace("/img ", "")
    await message.channel.send(file=discord.File(f"./image_library/{image_request}.png"))
    bot.send_message(TELEGRAM_CHAT,str(message.content))
    bot.send_photo(TELEGRAM_CHAT,photo=open(f"./image_library/{image_request}.png","rb"))