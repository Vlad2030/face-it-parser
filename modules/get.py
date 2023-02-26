from environs import Env
import requests
import filters


env = Env()
env.read_env()
api_key: str = env.list('API_KEY')


def itemsPrice(proxy=None) -> dict:
    with requests.get(
        url=f"https://api.steamapis.com/market/items/"
            f"730?api_key={api_key}"
        ) as r:
        items: dict = {}
        for item in r.json()["data"]:
            items[item["market_hash_name"]] = item["prices"]["avg"]
    return items


def me(token: str) -> dict:
    with requests.get(
        "https://api.faceit.com/users/v1/sessions/me",
        headers={
            "authorization": token,
        },
    ) as r:
        return r.json()


def matches(token: str, offset: float, region: str) -> dict:
    with requests.get(
        url="https://api.faceit.com/match/v1/matches/list?"
            "state=SUBSTITUTION&state=CAPTAIN_PICK&state=VOTING&"
            "state=CONFIGURING&state=READY&state=ONGOING&"
            "state=MANUAL_RESULT&state=PAUSED&state=ABORTED",
        headers={
            "authorization": token
        },
        params={
            "game": "csgo",
            "region": region,
            "limit": "100",
            "entityType": "matchmaking",
            "offset": str(offset) + "00",
        },
    ) as r:
        return r.json()


def inventoryPrice(steemId: str, data: dict, proxy: str) -> float:
    proxies: dict = {"https": proxy}
    initial_price: int = 0

    if proxy:
        r: requests.Response = requests.get(
            url=f"https://api.steamapis.com/steam/inventory/{steemId}"
                f"/730/2?api_key={api_key}",
            proxies=proxies,
        )
        rj: dict = r.json()
    else:
        r: requests.Response = requests.get(
            url=f"https://api.steamapis.com/steam/inventory/"
                f"{steemId}/730/2?api_key={api_key}",
        )
        rj: dict = r.json()

    try:
        for description in rj["descriptions"]:
            market_hash_name: str = description["market_hash_name"]
        return initial_price + data[market_hash_name]

    except Exception:
        return print(r.text)


def userInfo(token: str, facitId: str, proxy: str) -> dict:
    proxies = {"https": proxy}

    if proxy:
        return requests.get(
            url=f"https://open.faceit.com/data/v4/players/{facitId}",
            proxies=proxies,
            headers={"authorization": token},
        ).json()
    else:
        return requests.get(
            url=f"https://open.faceit.com/data/v4/players/{facitId}",
            headers={"authorization": token},
        ).json()


def users(matches: dict) -> None:
    while matches:
        match = matches
        for team in match["teams"]:
            for player in match["teams"][team]["roster"]:
                player.put(player)


def valueFiltres(value: int) -> None:
    if value is 1:
        if filters.filtres["level"]["work"]:
            val: int = input("Введите нижний уровень faceit: ")
            if filters.filtres["level"]["from"] is val:
                val: int = input("Введите верхний уровень faceit: ")
                if filters.filtres["level"]["to"] is val:
                    return filters.startFiltresInputs()

    elif value is 2:
        if filters.filtres["price"]["work"]:
            val: int = input("Введите нижнюю стоимость: ")
            if filters.filtres["price"]["from"] is val:
                val: int = input("Введите верхнюю стоимость: ")
                if filters.filtres["price"]["to"] is val:
                    return filters.startFiltresInputs()

    else:
        return print("error value")