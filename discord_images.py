import discord
import json
import requests

async def add_photo(self,message):
    if len(message.attachments) > 0:
        print(message.attachments[0])
        if message.attachments[0]:
            photo_name = str(message.content).replace("/addphoto ","")
            photo_url = str(message.attachments[0])
            img_data = requests.get(photo_url).content
            with open(f"./image_library/{photo_name}.png", "wb") as handler:
                handler.write(img_data)
        
async def send_image(self,message):
    image_request = str(message.content).replace("/img ", "")
    await message.channel.send(file=discord.File(f"./image_library/{image_request}.png"))