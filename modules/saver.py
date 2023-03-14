def saver(steam_ids: list, players: list) -> None:
    with open("blacklist.txt", "a") as file:
        while not steam_ids.empty() or not players.empty():
            steemId = steam_ids.get()
            file.write(f"{steemId}\n")
    return print("stop")
