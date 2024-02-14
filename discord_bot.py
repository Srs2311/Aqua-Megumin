import discord
import telebot
import json
import os
from dotenv import load_dotenv
import discord_admin as admin
import discord_images as d_images
import discord_weather as d_weather
import discord_roles
import discord_to_telegram as d2t
import quotes
import countdown
import dice_roll
import kanye
import rule34
import magic_eight_ball
import waifu
from environment_control import *


#grabs and returns config settings for bot
def refresh_settings():
    with open("./json/config.json","r") as settings:
        settings = json.load(settings)
    
    ignored_channel_ids = []
    for channel in settings["telegram_bridge"]["ignored_channels"]:
        ignored_channel_ids.append(channel.get("id",None))
    return settings,ignored_channel_ids


bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        bridge = client.get_channel(BRIDGE_CHAT)
        embed = discord.Embed(title="Explosion! Bot is online")
        embed.set_image(url = waifu.get_waifu("sfw","megumin"))
        await bridge.send(embed=embed)
        
    
    async def on_message(self, message):
        settings,ignored_channels = refresh_settings()
        
        # don't respond to ourselves
        if message.author == self.user:
            return
        
        #checks if channel is in an ignored channel
        if str(message.channel.id) in ignored_channels:
            return

        #checks for a photo attachment
        try:
            photo_url = str(message.attachments[0])
        except:
            photo_url = ""
        
#<------------------------USEFUL, BUT FUN COMMANDS------------------------------------->
        
        #/addphoto command, adds a photo to the library
        if str(message.content).lower().startswith("/addphoto") or str(message.content).lower().startswith("/add_photo"):
            await d_images.add_photo(self, message, image_gallery=client.get_channel(int(settings.get("discord_settings").get("image_gallery"))))
            
        #img command send a requested image
        elif str(message.content).startswith("/img"):
            await d_images.send_image(self,message)
        
        #sends the time until a requested countdown
        elif str(message.content).startswith("/countdown"):
            response = countdown.countdown(message.content)
            bridge = client.get_channel(BRIDGE_CHAT)
            await bridge.send(response)
            bot.send_message(TELEGRAM_CHAT,f"{message.author}: {message.content}")
            bot.send_message(TELEGRAM_CHAT,response)
        
        #adds a countdown  
        elif str(message.content).lower().startswith("/add_countdown"):
            response = countdown.add_countdown(message.content)
            bridge = client.get_channel(BRIDGE_CHAT)
            await bridge.send((response))
            bot.send_message(TELEGRAM_CHAT,f"{message.author}: {message.content}")
            bot.send_message(TELEGRAM_CHAT,f"{response}")

        #responds with a magic8ball answer
        elif str(message.content).startswith("/magic8ball"):
            await message.channel.send(magic_eight_ball.magic_eight_ball())
            
        #takes input of # of dice and #of dice sides (1d6,2d8,etc), then responds with the results of those dice rolls
        elif str(message.content).lower().startswith("/roll"):
            text = str(message.content).replace("/roll ","")
            response = dice_roll.roll_dice(text)
            responseStr = ""
            for i in range(0,len(response)):
                responseStr = f"{response[i]}   {responseStr}"
            bridge = client.get_channel(BRIDGE_CHAT)
            await bridge.send(responseStr)
            bot.send_message(TELEGRAM_CHAT,f"{message.author}: {message.content}")
            bot.send_message(TELEGRAM_CHAT,responseStr)
            
        elif str(message.content).startswith("/quote"):
            quote_text = str(message.content).replace("/quote","")
            if quote_text.startswith(" "):
                quote_text = quote_text[1:]
            response = quotes.fetch_quote(quote_text)
            await message.channel.send(response)
            bot.send_message(TELEGRAM_CHAT,f"{message.author}: {message.content}")
            bot.send_message(TELEGRAM_CHAT,response)
        
#<------------------------MEME COMMANDS------------------------------------------------>
        
        elif str(message.content).lower().startswith("/kanye"):
            embed = discord.Embed(title=kanye.get_kanye_quote())
            embed.set_author(name="Kanye East",icon_url="https://i.imgflip.com/41j06n.png")
            await message.channel.send(embed=embed)
            
        #makes your role color a changing rainbow
        elif str(message.content).startswith("/rainbow"):
            await discord_roles.rainbow_mode(message)
        
        #summons waifu images
        elif str(message.content).lower().startswith("/waifu"):
            command = message.content.split (" ",3)
            print(command)
            urls = []
            if command [0] == "/waifus":
                urls = waifu.get_many_waifu(command[1] if len(command) >=3 else "sfw",command[2] if len(command) >=3 else command[1])
            
            elif command[1] == "categories":
                url = waifu.get_waifu_categories(command[2] if len(command)>= 3 else "sfw")
            
            else:    
                url = waifu.get_waifu(command[1] if len(command) >=3 else "sfw",command[2] if len(command) >=3 else command[1])
            
            if len(urls) > 0:
                for url in urls:
                    print(url)
                    await message.channel.send(url)
            else:
                print(url)
                await message.channel.send(url)

#<------------------------ADMIN COMMANDS----------------------------------------------->
        
        #lists all server roles in discord chat
        elif str(message.content).startswith("/list_roles"):
            await discord_roles.list_roles(message)
    
        #deletes last n messages
        elif str(message.content).startswith("/trim"):
            await admin.trim(self,message)    
        
        #adds a channel to the ignored_channels list, and no longer bridges, or responds to commands on that channel
        elif str(message.content).startswith("/ignore_channel"):
            await admin.ignore_channel(self,message)
            await message.channel.send("Ignoring Channel")
        
        elif str(message.content).startswith("/add_role"):
            role_name = str(message.content).replace ("/add_role ","")
            await discord_roles.add_role_to_user(message,role_name)
            
        elif str(message.content).startswith("/generate_role_message"):
            role_chat = client.get_channel(ROLE_CHAT)
            await discord_roles.generate_role_message(role_chat)
        
        elif str(message.content).startswith("/rolemsg_add"):
            role_info = str(message.content).replace("/rolemsg_add ","")
            with open("./json/role_message.json","r") as r:
                role_chat = client.get_channel(ROLE_CHAT)
                role_message = json.load(r)
            await discord_roles.add_role_to_role_message(role_info,role_message,role_chat)
            
#<------------------------NSFW COMMANDS----------------------------------------------->
        
        elif str(message.content).lower().startswith("/rule34"):
            command = message.content.split(" ",3)
            results = rule34.search_rule_34(command[1] if len(command) >=3 else 1,command[2] if len(command) >=3 else command[1])
            if results != None:
                for result in results:
                    await message.channel.send(result.get("file_url","image not found"))
            else:
                await message.channel.send("No results found :(")
        
#<------------------------QOL COMMANDS----------------------------------------------->
        elif str(message.content).lower().startswith("/weather"):
            if message.content.replace("/weather","").strip() == "":
                await d_weather.get_current_weather(message)
            elif message.content.replace("/weather","").strip() == "week":
                await d_weather.get_weekly_weather(message)

#<------------------------Bridging--------------------------------------------------->        
        #bridges the message:
        if message.channel.nsfw and not settings.get("telegram_bridge").get("bridge_nsfw_channels",False):
            print("NSFW channel - not bridging")
            return
        else:
            d2t.bridge_message(photo_url,message)
        
    
    #sends telegram message when user joins/leaves voice channel
    async def on_voice_state_update(self, member, before, after):
        if str(after.channel) == "General":
            bot.send_message(chat_id,f"{member} has joined General")
        elif str(before.channel) == "General":
            bot.send_message(chat_id,f"{member} has left General")

    async def on_raw_reaction_add(self,payload):
        role_message = discord_roles.refresh_role_message()
        if int(payload.message_id) == int(role_message["id"]):
            role_list = discord_roles.refresh_reaction_roles()
            for role in role_list:
                if role["emoji"] == payload.emoji.name:
                    rlist = discord_roles.refresh_server_roles(payload.member)
                    for r in rlist:
                        if r.name == role["name"]:
                            await payload.member.add_roles(r)

intents = discord.Intents.all()
intents.message_content = True
client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)