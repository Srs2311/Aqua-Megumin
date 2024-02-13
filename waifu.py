import requests
sfw_categories = ["waifu",
    "neko",
    "shinobu",
    "megumin",
    "bully",
    "cuddle",
    "cry",
    "hug",
    "awoo",
    "kiss",
    "lick",
    "pat",
    "smug",
    "bonk",
    "yeet",
    "blush",
    "smile",
    "wave",
    "highfive",
    "handhold",
    "nom",
    "bite",
    "glomp",
    "slap",
    "kill",
    "kick",
    "happy",
    "wink",
    "poke",
    "dance",
    "cringe"]
nsfw_categories = ["waifu","neko","trap","blowjob"]

def get_waifu(type,category):
    waifu = requests.get(f"https://api.waifu.pics/{type}/{category}").json()["url"]
    return waifu

def get_many_waifu(type,category):
    waifus = requests.post(f"https://api.waifu.pics/many/{type}/{category}",json={}).json()["files"]
    return waifus

def get_waifu_categories(type="sfw"):
    if type == "sfw":
        list_in_string = ""
        for category in sfw_categories:
            list_in_string = f"{list_in_string}{category}, "
        return list_in_string
    elif type == "nsfw":
        list_in_string = ""
        for category in nsfw_categories:
            list_in_string = f"{list_in_string}{category}, "
        return list_in_string
        