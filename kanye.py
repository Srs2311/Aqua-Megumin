import requests

def get_kanye_quote() -> str:
    kanye = requests.get("https://api.kanye.rest").json()["quote"]
    return kanye