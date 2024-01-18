import telebot
import json
from dotenv import load_dotenv
import requests
import telegram_images as t_images
import magic_eight_ball as magic8ball
import quotes
import telegram_countdown as t_countdown
from environment_control import *

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)

#discord api call headers
headers = {'Authorization': f"Bot {DISCORD_TOKEN}"}

#------------------------------------------------------------------------------------------------------------------------#
@bot.message_handler(commands=['add_quote','addquote'])
def add_quote(message):
    """Command to add a quote by replying to a message with /addquote or add_quote"""
    if message.reply_to_message:
        quotes.add_quote(f"{message.from_user.username}: {message.reply_to_message.text}")
        bot.reply_to(message,f"Added quote: {message.from_user.username}: {message.reply_to_message.text}")
    else:
        bot.reply_to(message,"Reply to a message to add it as a quote")

@bot.message_handler(commands=["quote"])
def send_quote(message):
    quote_text = str(message.text).replace("/quote","")
    if quote_text.startswith(" "):
        quote_text = quote_text[1:]
    quote_response = quotes.fetch_quote(quote_text)
    bot.reply_to(message,quote_response)
    bridge_commands(message,quote_response)
        
#simple command to generate a response, mostly used for making sure the bot is online
@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message,"pong")
    bridge_commands(message,"pong")    

#responds with users username
@bot.message_handler(commands=["whoami"])
def whoami(message):
    bot.reply_to(message,f"{message.from_user.username}")

@bot.message_handler(commands=["magic8ball"])
def eight_ball(message):
    response = magic8ball.magic_eight_ball()
    bot.send_message(message.chat.id,response)
    


#command to pull an image from image.json and post in chat
@bot.message_handler(commands=["img"])
def send_image(message):
    t_images.send_image_from_library(bot,message)
    

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

@bot.message_handler(content_types=["animation"])
def add_gif(message):
    #checks if gif has a caption, which is where commands would be stored
    if message.caption:
        if "/addgif" in message.caption:
            messageText = message.caption
            messageText = messageText.replace("/addgif ","")
            gif_info = {"name":messageText,"fileid":message.animation[0].file_id}
            with open("./gifs.json","r") as gifList:
                gif_list = json.load(gifList)
                gif_names = []
                for picture in gif_list:
                    gif_names.append(picture["name"])
                if messageText not in gif_names:
                    gif_list.append(gif_info)
                    bot.send_message(message.chat.id,f"Added gif {messageText}")
                else:
                    bot.send_message(message.chat.id,"GIF with that name already exists")
        
            with open("./gifs.json","w") as imagesList:
                imagesList.write(json.dumps(gif_list))

    gif_info = bot.get_file(message.animation.file_id)
    r = requests.get(f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{gif_info.file_path}",allow_redirects=True)
    open(f"./gifs/{gif_info.file_unique_id}.mp4","wb").write(r.content)

    files = {
        (f"./gifs/{gif_info.file_unique_id}.mp4", open(f"./gifs/{gif_info.file_unique_id}.mp4", 'rb'))
    }

    image_bridge = requests.post(
    f"https://discord.com/api/v9/channels/1193661269333524520/messages",
    headers=headers,
    files=files, 
    json={"content": f"{message.from_user.username}: {message.text}"}
    )


@bot.message_handler(commands=["addphoto"])
def add_photo_with_reply(message):
    t_images.add_photo(bot,message)

@bot.message_handler(content_types=["photo"])
def add_photo(message):
    if message.caption:
        if "/addphoto" in message.caption:
            t_images.add_photo(bot,message)
    #image bridging
    t_images.download_telegram_image(bot,message,name=str(message.photo[-1].file_unique_id))
    t_images.send_photo_to_discord(BRIDGE,f"./pictures/{message.photo[-1].file_unique_id}.png",str(message.photo[-1].file_unique_id),f"{message.from_user.username}: {message.caption if message.caption else ""}")

#gets chatid of a telegram chat, mostly a developer feature
@bot.message_handler(commands=["chatid"])
def send_chat_id(message):
    bot.send_message(message.chat.id,f"Chat ID: {message.chat.id}")
    
@bot.message_handler(commands=["userInfo"])
def send_user_info(message):
    bot.send_message(message.chat.id,f"{message.from_user}")

@bot.message_handler(commands=["countdown"])
def countdown(message):
    t_countdown.countdown(bot,message)

@bot.message_handler(commands=["addCountdown","addcountdown"])
def add_countdown(message):
    t_countdown.add_countdown(bot,message)

@bot.message_handler(commands=["generateImageLibrary"])
def generate_image_library():
    t_images.generate_image_library()

#forwards non-command and non-image messages    
@bot.message_handler(func=lambda m: True)
def discord_bridge(message):
    requests.post(
    f"https://discord.com/api/v6/channels/{BRIDGE}/messages",
    headers=headers, 
    json={"content": f"{message.from_user.username}: {message.text}"}
)

#sends command and response to discord, called in other functions
def bridge_commands(message,response):
    requests.post(
    f"https://discord.com/api/v6/channels/{BRIDGE}/messages",
    headers=headers, 
    json={"content": f"{message.from_user.username}: {message.text}"}
        )
    
    requests.post(
    f"https://discord.com/api/v6/channels/{BRIDGE}/messages",
    headers=headers, 
    json={"content": f"{response}"}
    )

bot.infinity_polling()

