import discord
import telebot
import json
import os
from dotenv import load_dotenv
import discord_admin as admin
import discord_images as d_images
import quotes
import magic_eight_ball
from environment_control import *


#grab and store ignored channel list
def refresh_ignored_channels():
    with open("./json/ignored_channels.json","r") as channels:
        ignored_channels = json.load(channels)
        ignored_channel_ids = []
        for channel in ignored_channels:
            ignored_channel_ids.append(str(channel["id"]))
        return ignored_channel_ids


bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        bridge = client.get_channel(BRIDGE_CHAT)
        await bridge.send("Explosion! Bot is online")
    
    async def on_message(self, message):
        image_library = client.get_channel(IMAGE_LIBRARY)
        # don't respond to ourselves
        if message.author == self.user:
            return
        
        if str(message.channel.id) in refresh_ignored_channels():
            return
        #checks for a photo attachment
        try:
            photo_url = str(message.attachments[0])
        except:
            photo_url = ""
            pass
        
        #adds photo to image library
        if str(message.content).startswith("/addphoto"):
            await d_images.add_photo(self,message)

        #deletes last n messages
        elif str(message.content).startswith("/trim"):
            await admin.trim(self,message)    

        elif str(message.content).startswith("/admin_check"):
            admin.admin_check(self,message)
        
        elif str(message.content).startswith("/ignore_channel"):
            await admin.ignore_channel(self,message)
        
        elif str(message.content).startswith("/magic8ball"):
            await message.channel.send(magic_eight_ball.magic_eight_ball())
        
        #img command to reflect telegram bot
        elif str(message.content).startswith("/img"):
            await d_images.send_image(self,message)
        
        elif str(message.content).startswith("/quote"):
            quote_text = str(message.content).replace("/quote","")
            if quote_text.startswith(" "):
                quote_text = quote_text[1:]
            await message.channel.send(quotes.fetch_quote(quote_text))
        
        #bridging (disbled on ignored_channels)
        elif not any(channel == str(message.channel.id) for channel in refresh_ignored_channels()):
            if len(photo_url) > 0:
                if ".mp4" in photo_url:
                    bot.send_video(chat_id,photo_url,caption=f"{message.author}: {message.content}")
                else:
                    bot.send_photo(chat_id,photo_url,caption=f"{message.author}: {message.content}")
            else:
                bot.send_message(chat_id,f"{message.author}: {message.content}")
        elif any(channel == str(message.channel.id) for channel in refresh_ignored_channels()):
            print("message posted in ignored channel")
    
    #sends telegram message when user joins/leaves voice channel
    async def on_voice_state_update(self, member, before, after):
        if str(after.channel) == "General":
            bot.send_message(chat_id,f"{member} has joined General")
        elif str(before.channel) == "General":
            bot.send_message(chat_id,f"{member} has left General")


intents = discord.Intents.all()
intents.message_content = True
client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)