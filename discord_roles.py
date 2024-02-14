import json
import discord
import time
from environment_control import *


def refresh_server_roles(message):
    role_list = []
    for role in message.guild.roles:
        role_list.append(role)
    return role_list

def refresh_reaction_roles():
    with open("./json/role_reactions.json","r") as r:
        role_list = json.load(r)
    return role_list

def refresh_role_message():
    with open("./json/role_message.json","r") as r:
        role_message = json.load(r)
    return role_message

async def add_role_to_user(message,role_name):
    role_list = refresh_server_roles(message)
    for role in role_list:
        if role_name == str(role):
            await message.author.add_roles(role)

async def remove_role_from_user(message,role_name):
    role_list = refresh_server_roles(message)
    for role in role_list:
        if role_name == str(role):
            await message.author.remove_roles(role)

async def rainbow_mode(message):
    rainbow = ["red","orange","yellow","green","blue","indigo","violet"]
    while True:
        for i in range(0,len(rainbow)):
            await add_role_to_user(message,rainbow[i])
            time.sleep(.1)
            await remove_role_from_user(message,rainbow[i-1])
            time.sleep(.1)

async def add_role_to_role_message(role_info,role_message,role_chat):
    role_info = role_info.split("|")
    role_emoji = role_info[0]
    role_name = role_info[1]
    role_json = {"emoji":role_emoji,"name":role_name}
    role_message = await role_chat.fetch_message(role_message["id"])
    await role_message.add_reaction(role_json["emoji"])
    role_list = refresh_reaction_roles()
    role_list.append(role_json)
    with open("./json/role_reactions.json","w") as w:
        w.write(json.dumps(role_list))
    

async def generate_role_message(role_chat):
    role_message = await role_chat.send("React to this message to get a role")
    reaction_list = refresh_reaction_roles()
    for emoji in reaction_list:
        await role_message.add_reaction(emoji["emoji"])
    role_json = {}
    role_json["id"] = role_message.id
    print(role_json)
    with open("./json/role_message.json","w") as role_message_json:
        role_message_json.write(json.dumps(role_json))

async def list_roles(message):
    role_list = refresh_server_roles(message)
    response = ""
    for role in role_list:
        response = (f"{response} {role.name} \n {role.id} \n \n")
    await message.channel.send(response)