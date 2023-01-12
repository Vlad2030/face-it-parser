import get
import send


def user(
    players,
    serverToken,
    clientToken,
    steam_ids,
    filtres,
    meId,
    blacklist,
    data,
    proxy=None,
):
    while not players.empty():
        player = players.get()
        try:
            if proxy == None:
                userInfo = userInfo(serverToken, player["id"])
            else:
                userInfo = userInfo(serverToken, player["id"], proxy)
            if userInfo["steam_id_64"] not in blacklist:
                sendFrendRequestVal = False
                if not filtres["price"]["work"] and not filtres["level"]["work"]:
                    sendFrendRequestVal = True
                if filtres["level"]["work"]:
                    if (
                        int(filtres["level"]["from"])
                        <= int(userInfo["games"]["csgo"]["skill_level"])
                        <= int(filtres["level"]["to"])
                    ):
                        sendFrendRequestVal = True
                price = ""
                if filtres["price"]["work"]:
                    if filtres["level"]["work"]:
                        if sendFrendRequestVal:
                            try:
                                if proxy == None:
                                    price = get.inventoryPrice(
                                        userInfo["steam_id_64"], data
                                    )
                                else:
                                    price = get.inventoryPrice(
                                        userInfo["steam_id_64"], data, proxy
                                    )
                                if (
                                    int(filtres["price"]["from"])
                                    <= int(price)
                                    <= int(filtres["price"]["to"])
                                ):
                                    sendFrendRequestVal = True
                                else:
                                    sendFrendRequestVal = False
                            except Exception as ex:
                                sendFrendRequestVal = False
                    else:
                        try:
                            if proxy == None:
                                price = get.inventoryPrice(userInfo["steam_id_64"], data)
                            else:
                                price = get.inventoryPrice(
                                    userInfo["steam_id_64"], data, proxy
                                )
                            if (
                                int(filtres["price"]["from"])
                                <= int(price)
                                <= int(filtres["price"]["to"])
                            ):
                                sendFrendRequestVal = True
                            else:
                                sendFrendRequestVal = False
                        except Exception as ex:
                            sendFrendRequestVal = False
                steam_id = userInfo["steam_id_64"]
                level = userInfo["games"]["csgo"]["skill_level"]
                if sendFrendRequestVal:
                    if proxy == None:
                        send.friendRequest(clientToken, meId, userInfo["player_id"])
                    else:
                        send.friendRequest(
                            clientToken, meId, userInfo["player_id"], proxy
                        )
                    print(f"{steam_id} {level} {price} request sent")
                    steam_ids.put(userInfo["steam_id_64"])
                else:
                    print(f"{steam_id} {level} {price}")
        except:
            players.put(player)