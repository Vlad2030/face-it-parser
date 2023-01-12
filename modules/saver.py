def saver(steam_ids, players):
    while not players.empty() or not steam_ids.empty():
        f = open("blacklist.txt", "a")
        steemId = steam_ids.get()
        f.write(f"\n{steemId}")
        f.close()
    print("stop")