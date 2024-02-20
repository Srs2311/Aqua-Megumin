import telebot
import settings_management as sm

settings = sm.refresh_settings()


bot = telebot.TeleBot(settings["tokens"]["telegram"], parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

def bridge_message(photo_url,message):
    #if a photo url was grabbed, bridges the photo
    if len(photo_url) > 0:
        if ".mp4" in photo_url:
            bot.send_video(settings["telegram_bridge"]["telegram_chat"],photo_url,caption=f"{message.author}: {message.content}")
        else:
            bot.send_photo(settings["telegram_bridge"]["telegram_chat"],photo_url,caption=f"{message.author}: {message.content}")
        #If not, just bridges the message text
    else:
        bot.send_message(settings["telegram_bridge"]["telegram_chat"],f"{message.author}: {message.content}")