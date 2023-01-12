from ..app import *
import threading
import add
import filters
import get


def start():
    blacklist_fiel = open("blacklist.txt", "r")
    blacklist = []
    for line in blacklist_fiel.read().splitlines():
        blacklist.append(line)
    blacklist = set(blacklist)

    tokens_site_fiel = open("tokens_site.txt", "r")
    tokens_site = []
    for line in tokens_site_fiel.read().splitlines():
        tokens_site.append(line)

    tokens_server_fiel = open("tokens_server.txt", "r")
    tokens_server = []
    for line in tokens_server_fiel.read().splitlines():
        tokens_server.append(line)

    proxy_fiel = open("proxy.txt", "r")
    proxy = []
    for line in proxy_fiel.read().splitlines():
        try:
            proxies = {"https": line}
            r = requests.get("https://www.google.com/", proxies=proxies)
            proxy.append(line)
        except Exception as e:
            print(e)
            print(f"Прокси {line} невалиден")
            pass
    if len(proxy) == 0:
        thread_count = int(input("Введите число потоков: "))
    else:
        thread_count = len(proxy)
    for i, token in enumerate(tokens_site):
        print(f"({i+1}) {token}")
    index_site_token = input("Введите номер токена сайта или 0 для добавления нового: ")
    if int(index_site_token) == 0:
        clientToken = input("Введите новый токен: ")
        add.clientToken(clientToken)
    else:
        split_token_site = tokens_site[int(index_site_token) - 1].split(" ")
        clientToken = split_token_site[0] + " " + split_token_site[1]

    for i, token in enumerate(tokens_server):
        print(f"({i+1}) {token}")
    index_tokens_server = input(
        "Введите номер токена сервера или 0 для добавления нового: "
    )
    if int(index_tokens_server) == 0:
        serverToken = input("Введите новый токен: ")
        add.serverToken(serverToken, clientToken)
    else:
        split_token_server = tokens_server[int(index_tokens_server) - 1].split(" ")
        serverToken = split_token_server[0] + " " + split_token_server[1]

    filters.startFiltresInputs()

    me = get.me(clientToken)

    print("получение матчей")
    region = regions[region_index]
    indexPages = 0
    totalPages = 1
    while indexPages < totalPages:
        matches_data = get.matches(clientToken, indexPages, region)
        for matche in matches_data["payload"]:
            matches.put(matche)
        totalPages = matches_data["totalPages"]
        indexPages = indexPages + 1

    print("получение игроков")
    threads = []
    for i in range(thread_count):
        threads.append(threading.Thread(target=get.users, args=(matches,)))
        threads[i].start()

    for i in range(thread_count):
        threads[i].join()
    print("начало работы")
    threads = []
    for i in range(thread_count):
        if len(proxy) == 0:
            threads.append(
                threading.Thread(
                    target=check.user,
                    args=(
                        players,
                        serverToken,
                        clientToken,
                        steam_ids,
                        filters.filtres,
                        me["payload"]["id"],
                        blacklist,
                        data,
                    ),
                )
            )
        else:
            threads.append(
                threading.Thread(
                    target=check.user,
                    args=(
                        players,
                        serverToken,
                        clientToken,
                        steam_ids,
                        filters.filtres,
                        me["payload"]["id"],
                        blacklist,
                        data,
                        proxy[i],
                    ),
                )
            )
            threads[i].start()