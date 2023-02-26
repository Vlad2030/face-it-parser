import requests
from queue import Queue
import threading


import modules.add
import modules.check
import modules.filters
import modules.get
import modules.saver
import modules.send


if __name__ == "__main__":
    data: dict = modules.get.itemsPrice()
    regions: dict = {
        1: "EU",
        2: "US",
        3: "SEA",
        4: "Oceania",
        5: "SA",
    }
    region_index: int = input(
            "\n\n1 - EU\n2 - US\n3 - SEA\n4 - Oceania\n5 - SA\n6 - US, SEA, Oceania, SA\nВведите номер региона: "
        )

    amount: int = input("Введите сколько раз парсить: ")
    matches: Queue = Queue()
    players: Queue = Queue()
    steam_ids: Queue = Queue()

    with open("blacklist.txt", "r") as blacklist_fiel:
        blacklist = []
        for line in blacklist_fiel.read().splitlines():
            blacklist.append(line)
        blacklist = set(blacklist)

    with open("tokens_site.txt", "r") as tokens_site_fiel:
        tokens_site = []
        for line in tokens_site_fiel.read().splitlines():
            tokens_site.append(line)

    with open("tokens_server.txt", "r") as tokens_server_fiel:
        tokens_server = []
        for line in tokens_server_fiel.read().splitlines():
            tokens_server.append(line)

    with open("proxy.txt", "r") as proxy_fiel:
        proxy = []
        for line in proxy_fiel.read().splitlines():
            try:
                proxies = {"https": line}
                requests.get("https://www.google.com/", proxies=proxies)
                proxy.append(line)
            except Exception as e:
                print(
                    f"{e}"
                    f"Прокси {line} невалиден"
                )

    if proxy:
        thread_count: int = int(input("Введите число потоков: "))
    else:
        thread_count = len(proxy)

    for i, token in enumerate(tokens_site):
        print(f"({i+1}) {token}")

    index_site_token: int = input("Введите номер токена сайта или 0 для добавления нового: ")
    if index_site_token is 0:
        clientToken: int = input("Введите новый токен: ")
        modules.add.token(token=clientToken, client_token=None)
    else:
        split_token_site: str = tokens_site[int(index_site_token) - 1].split(" ")
        clientToken: str = split_token_site[0] + " " + split_token_site[1]

    for i, token in enumerate(tokens_server):
        print(f"({i+1}) {token}")
    index_tokens_server: int = input(
        "Введите номер токена сервера или 0 для добавления нового: "
    )

    if index_tokens_server is 0:
        serverToken: str = input("Введите новый токен: ")
        modules.add.token(token=serverToken, client_token=clientToken)
    else:
        split_token_server: str = tokens_server[int(index_tokens_server) - 1].split(" ")
        serverToken: str = split_token_server[0] + " " + split_token_server[1]

    modules.filters.startFiltresInputs()

    me: dict = modules.get.me(clientToken)

    print("получение матчей")
    region = regions[region_index]
    indexPages = 0
    totalPages = 1
    while indexPages < totalPages:
        matches_data: dict = modules.get.matches(
            token=clientToken,
            offset=indexPages,
            region=region,
        )

        for matches in matches_data["payload"]:
            matches.put(matches)

        totalPages: dict = matches_data["totalPages"]
        indexPages: float = indexPages + 1

    print("получение игроков")
    threads = []

    for i in thread_count:
        threads.append(threading.Thread(target=modules.get.users, args=(matches,)))
        threads[i].start()

    for i in thread_count:
        threads[i].join()

    print("начало работы")
    threads = []
    for i in thread_count:
        if proxy is 0:
            threads.append(
                threading.Thread(
                    target=modules.check.user,
                    args=(
                        players,
                        serverToken,
                        clientToken,
                        steam_ids,
                        modules.filters.filtres,
                        me["payload"]["id"],
                        blacklist,
                        data,
                    ),
                ),
            ),

        else:
            threads.append(
                threading.Thread(
                    target=modules.check.user,
                    args=(
                        players,
                        serverToken,
                        clientToken,
                        steam_ids,
                        modules.filters.filtres,
                        me["payload"]["id"],
                        blacklist,
                        data,
                        proxy[i],
                    ),
                ),
            ),
            threads[i].start()

    save_thread = threading.Thread(target=modules.saver, args=(steam_ids, players))
    save_thread.start()

    for i in thread_count:
        threads[i].join()

    save_thread.join()