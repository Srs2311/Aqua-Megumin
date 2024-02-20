import telebot
import json
from dotenv import load_dotenv
import requests
import telegram_images as t_images
import magic_eight_ball as magic8ball
import quotes
import countdown as t_countdown
import dice_roll
import telegram_to_discord as t2d
import kanye
import weather_check
import settings_management as sm


def load_settings():
    with open("./json/config.json") as config:
        settings = json.load(config)
    return settings

settings = load_settings()
#discord api call headers
headers = {'Authorization': f"Bot {settings.get("tokens").get("discord")}"}
#creates the telegram bot
bot = telebot.TeleBot(settings.get("tokens").get("telegram"), parse_mode=None)
#------------------------------------------------------------------------------------------------------------------------#

#<---------------------------------------------Useful, but fun Commands-------------------------------------------------->

#<-------------------------QUOTE COMMANDS---------------------------------->
#adds a quote to the quote db
@bot.message_handler(commands=['add_quote','addquote'])
def add_quote(message):
    """Command to add a quote by replying to a message with /addquote or add_quote"""
    if message.reply_to_message:
        quotes.add_quote(f"{message.from_user.username}: {message.reply_to_message.text}")
        bot.reply_to(message,f"Added quote: {message.from_user.username}: {message.reply_to_message.text}")
    else:
        bot.reply_to(message,"Reply to a message to add it as a quote")
        
#sends a quote based on user request, or random if no specific quote is mentioned        
@bot.message_handler(commands=["quote"])
def send_quote(message):
    quote_text = str(message.text).replace("/quote","")
    if quote_text.startswith(" "):
        quote_text = quote_text[1:]
    quote_response = quotes.fetch_quote(quote_text)
    bot.reply_to(message,quote_response)
    bridge_commands(message,quote_response)
    
#<-------------------------RNG COMMANDS---------------------------------->
#sends a magic8ball response
@bot.message_handler(commands=["magic8ball"])
def eight_ball(message):
    response = magic8ball.magic_eight_ball()
    bot.send_message(message.chat.id,response)
    bridge_commands(message,response)

#takes input of # of dice and #of dice sides (1d6,2d8,etc), then responds with the results of those dice rolls
@bot.message_handler(commands=["roll"])
def roll(message):
    text = str(message.text).replace("/roll ","")
    response = dice_roll.roll_dice(text)
    responseStr = ""
    for i in range(0,len(response)):
        responseStr = f"{response[i]}   {responseStr}"
    bot.send_message(message.chat.id,responseStr)
    bridge_commands(message,responseStr)
    
#<---------------IMAGE COMMANDS----------------------------------------->

#adds a photo to the photo library    
@bot.message_handler(commands=["addphoto","add_photo"])
def add_photo_with_reply(message):
    t_images.add_photo(bot,message)
    
#command to pull an image from image.json and post in chat
@bot.message_handler(commands=["img"])
def send_image(message):
    bridge_commands(message,None)
    t_images.send_image_from_library(bot,message)

#<----------------GIF COMMANDS----------------------------------------->

@bot.message_handler(commands=["gif"])
def send_gif(message):
    gif_name = message.text.replace("/gif ","")
    with open("./gifs.json","r") as gifList:
        gif_list = json.load(gifList)
        for gif in gif_list:
            if gif_name == gif["name"]:
                bot.send_animation(message.chat.id,gif["fileid"])

@bot.message_handler(commands = ["addgif"])
def add_gif(message):
    gif_message = message.reply_to_message
    message_text = message.text.replace("/addgif ","")
    gif_info = {"name":message_text,"fileid":gif_message.animation.file_id}
    with open("./gifs.json","r") as imagesList:
        gif_list = json.load(imagesList)
        gif_names = []
        for gif in gif_list:
            gif_names.append(gif["name"])
        if message_text not in gif_names:
            gif_list.append(gif_info)
            bot.send_message(message.chat.id,f"Added GIF {message_text}")
        else:
            bot.send_message(message.chat.id,"GIF with that name already exists")
        
    with open("./gifs.json","w") as imagesList:
            imagesList.write(json.dumps(gif_list))
            
#<------------------COUNTDOWN COMMANDS--------------------------------------->

@bot.message_handler(commands=["countdown"])
def countdown(message):
    response = t_countdown.countdown(str(message.text))
    bot.send_message(message.chat.id,response)
    bridge_commands(message,response)

@bot.message_handler(commands=["addCountdown","addcountdown"])
def add_countdown(message):
    response = t_countdown.add_countdown(message.text)
    bot.send_message(message.chat.id,response)
    bridge_commands(message,response)
  
#<---------------------------------------------Meme Commands------------------------------------------------------------->

@bot.message_handler(commands=['kanye'])
def rand_kanye(message):
    response = kanye.get_kanye_quote()
    bot.reply_to(message,response)
    bridge_commands(message,response, embed=True, response_embed={"author":"Kanye East", "author_icon":"https://i.imgflip.com/41j06n.png"})

#<---------------------------------------------Admin Commands------------------------------------------------------------>

#simple command to generate a response, mostly used for making sure the bot is online
@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message,"pong")
    bridge_commands(message,"pong")  

@bot.message_handler(commands=["generateImageLibrary"])
def generate_image_library(message):
    t_images.generate_image_library()

#gets chatid of a telegram chat, mostly a developer feature
@bot.message_handler(commands=["chatid"])
def send_chat_id(message):
    bot.send_message(message.chat.id,f"Chat ID: {message.chat.id}")
  
#responds with users username
@bot.message_handler(commands=["whoami"])
def whoami(message):
    bot.reply_to(message,f"{message.from_user.username}")
    
@bot.message_handler(commands=["userInfo","userinfo"])
def send_user_info(message):
    photos = bot.get_user_profile_photos(message.from_user.id)
    pfp = photos.photos[0][0]
    bot.send_message(message.chat.id,f"{message.from_user}")
    bot.send_photo(message.chat.id,photo=str(pfp.file_id))
    t2d.bridge_message_embed(message)

#<---------------------------------------------QOL Commands-------------------------------------------------------------->

@bot.message_handler(commands=["weather"])
def weather(message):
    weather_results = weather_check.get_daily_forecast()
    bot.send_message(message.chat.id,weather_results["detailedForecast"])
    bridge_commands(message, weather_results.get("detailedForecast","Weather unavailable"), embed = True, response_embed={"author":"Your Local Weatherman","author_icon":weather_results.get("icon")})

#<---------------------------------------------Bridging logic------------------------------------------------------------>


@bot.message_handler(content_types=["photo"])
def photo_handler(message):
    if message.caption:
        if "/addphoto" in message.caption or "/add_photo" in message.caption:
            t_images.add_photo(bot,message)
    #image bridging
    t_images.download_telegram_image(bot,message,name=str(message.photo[-1].file_unique_id))
    if settings["discord_bridge"]["use_embeds"] == True:
        t2d.bridge_photo_embed(message)

@bot.message_handler(content_types=["sticker"])
def sticker_handler(message):
    t2d.sticker_embed(message)

#forwards any non-command messages 
@bot.message_handler(func=lambda m: True)
def discord_bridge(message):
    if message.text:
        t2d.bridge_message_embed(message)
    if message.photo:
        t2d.bridge_photo_embed(message)
    if message.animation:
        t2d.bridge_video(message)
    if message.video:
        t2d.bridge_video(message)
    if message.sticker:
        t2d.sticker_embed(message)
        
#sends command and response to discord, called in other functions
def bridge_commands(message,response, embed:bool=False,  response_embed:dict=None):
    if settings["discord_bridge"]["use_embeds"] == True:
        t2d.bridge_message_embed(message)
    else:
        t2d.bridge_message(message)
         
    if response != None:
        t2d.bridge_response(response,embed=embed,embed_data=response_embed)

bot.infinity_polling()

