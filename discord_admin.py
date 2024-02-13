import discord
import json


def admin_check(self,message):
    print("admin check called")
    if "bot_admin" in [role.name.lower() for role in message.author.roles]:
        return True
    else:
        return False

async def trim(self,message):
    if admin_check(self,message):
        trim_num  = str(message.content).replace("/trim ","")
        async for message_to_delete in message.channel.history(limit=int(trim_num)):
            await message_to_delete.delete()
        
async def ignore_channel(self,message):
    if admin_check(self,message):
        with open("./json/config.json","r") as config:
            config = json.load(config) 
        if message.channel not in config["telegram_bridge"]["ignored_channels"]:
            channel_info = {}
            channel_info["name"] = str(message.channel.name)
            channel_info["id"] = str(message.channel.id)
            config["telegram_bridge"]["ignored_channels"].append(channel_info)
            with open ("./json/config.json","w") as config_writeable:
                config_writeable.write(json.dumps(config))

