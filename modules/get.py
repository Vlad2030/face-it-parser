import requests
import json
import os

from dotenv import load_dotenv
from filters import *
from ..app import *

load_dotenv()
api_key = os.getenv('API_KEY')

def itemsPrice(proxy=None):
    r = requests.get(f"https://api.steamapis.com/market/items/" \
        f"730?api_key={api_key}")
    items = {}
    for item in r.json()["data"]:
        items[item["market_hash_name"]] = item["prices"]["avg"]
    return items


def me(token):
    r = requests.get(
        "https://api.faceit.com/users/v1/sessions/me",
        headers={"authorization": token}
    )
    return r.json()


def matches(token, offset, region):
    r = requests.get(
        "https://api.faceit.com/match/v1/matches/list?"
        "state=SUBSTITUTION&state=CAPTAIN_PICK&state=VOTING&"
        "state=CONFIGURING&state=READY&state=ONGOING&"
        "state=MANUAL_RESULT&state=PAUSED&state=ABORTED",
        headers={"authorization": token},
        params={
            "game": "csgo",
            "region": region,
            "limit": "100",
            "entityType": "matchmaking",
            "offset": str(offset) + "00",
        },
    )
    return r.json()


def inventoryPrice(steemId, data, proxy=None):
    if proxy == None:
        r = requests.get(
            f"https://api.steamapis.com/steam/inventory/"
            f"{steemId}/730/2?api_key={api_key}"
        )
        rj = r.json()
    else:
        proxies = {"https": proxy}
        r = requests.get(
            f"https://api.steamapis.com/steam/inventory/{steemId}"
            f"/730/2?api_key={api_key}",
            proxies=proxies,
        )
        rj = r.json()
    try:
        initial_price = 0
        for description in rj["descriptions"]:
            market_hash_name = description["market_hash_name"]
            try:
                initial_price = initial_price + data[market_hash_name]
            except:
                pass
        return initial_price
    except Exception as ex:
        print(r.text)
        return ""


def userInfo(token, facitId, proxy=None):
    if proxy == None:
        r = requests.get(
            f"https://open.faceit.com/data/v4/players/{facitId}",
            headers={"authorization": token},
        )
    else:
        proxies = {"https": proxy}
        r = requests.get(
            f"https://open.faceit.com/data/v4/players/{facitId}",
            proxies=proxies,
            headers={"authorization": token},
        )
    return r.json()


def users(matches):
    while not matches.empty():
        match = matches.get()
        for team in match["teams"].keys():
            for player in match["teams"][team]["roster"]:
                players.put(player)


def valueFiltres(value):
    if int(value) == 1:
        filtres["level"]["work"] = True
        val = input("Введите нижний уровень faceit : ")
        filtres["level"]["from"] = val
        val = input("Введите верхний уровень faceit : ")
        filtres["level"]["to"] = val
        startFiltresInputs()
    if int(value) == 2:
        filtres["price"]["work"] = True
        val = input("Введите нижнюю стоимость: ")
        filtres["price"]["from"] = val
        val = input("Введите верхнюю стоимость: ")
        filtres["price"]["to"] = val
        startFiltresInputs()