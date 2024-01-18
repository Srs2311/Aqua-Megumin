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
        with open("./json/ignored_channels.json","r") as ignored_channels:
            channels = json.load(ignored_channels) 
        if message.channel not in channels:
            channel_info = {}
            channel = message.channel
            channel_info["name"] = str(channel.name)
            channel_info["id"] = str(channel.id)
            channels.append(channel_info)
            with open ("./json/ignored_channels.json","w") as ignored_channels_writeable:
                ignored_channels_writeable.write(json.dumps(channels))

