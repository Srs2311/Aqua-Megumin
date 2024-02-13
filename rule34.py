import requests

def search_rule_34(limit:int,tags:str):
    try:
        results = requests.get(f"https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&limit={limit}&tags={tags}&json=1").json()
    except:
        results = None
    return results

