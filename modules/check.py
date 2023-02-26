import get
import send


def user(
        players: dict, serverToken: str,
        clientToken: str, steam_ids: list, filtres: dict,
        meId: str, blacklist: bool, data: dict, proxy: str) -> None:

    price: float = 0.00

    while players:
        player: dict = players.get()

        try:
            if proxy:
                userInfo: dict = get.userInfo(
                    token=serverToken,
                    facitId=player["id"],
                    proxy=proxy
                )
            else:
                userInfo: dict = get.userInfo(
                    token=serverToken, 
                    facitId=player["id"], 
                    proxy=proxy,
                )

            if userInfo["steam_id_64"] not in blacklist:
                sendFrendRequestVal: bool = False
                if (not filtres["price"]["work"]
                        and not filtres["level"]["work"]):
                    sendFrendRequestVal: bool = True

                if filtres["level"]["work"]:
                    if (int(filtres["level"]["from"])
                            <= int(userInfo["games"]["csgo"]["skill_level"])
                            <= int(filtres["level"]["to"])):
                        sendFrendRequestVal: bool = True

                if filtres["price"]["work"]:
                    if filtres["level"]["work"]:
                        if sendFrendRequestVal:
                            try:
                                if proxy:
                                    price: float = get.inventoryPrice(
                                        steemId=userInfo["steam_id_64"],
                                        data=data,
                                        proxy=proxy,
                                    )
                                else:
                                    price: float = get.inventoryPrice(
                                        steemId=userInfo["steam_id_64"],
                                        data=data,
                                        proxy=None,
                                    )

                                if (int(filtres["price"]["from"])
                                        <= int(price)
                                        <= int(filtres["price"]["to"])):
                                    sendFrendRequestVal: bool = True
                                else:
                                    sendFrendRequestVal: bool = False

                            except Exception:
                                sendFrendRequestVal: bool = False

                    else:
                        try:
                            if proxy:
                                price: float = get.inventoryPrice(
                                    steemId=userInfo["steam_id_64"],
                                    data=data,
                                    proxy=proxy,
                                )

                            else:
                                price: float = get.inventoryPrice(
                                    steemId=userInfo["steam_id_64"],
                                    data=data,
                                    proxy=None,
                                )

                            if (int(filtres["price"]["from"])
                                    <= int(price)
                                    <= int(filtres["price"]["to"])):
                                sendFrendRequestVal: bool = True

                            else:
                                sendFrendRequestVal: bool = False

                        except Exception:
                            sendFrendRequestVal: bool = False

                steam_id = userInfo["steam_id_64"]
                level = userInfo["games"]["csgo"]["skill_level"]

                if sendFrendRequestVal:
                    if proxy:
                        send.friendRequest(
                            token=clientToken,
                            facitIdSending=meId,
                            facitIdReceiving=userInfo["player_id"],
                            proxy=proxy,
                        )
                    else:
                        send.friendRequest(
                            token=clientToken,
                            facitIdSending=meId,
                            facitIdReceiving=userInfo["player_id"],
                            proxy=None,
                        )

                    print(f"{steam_id} {level} {price} request sent")
                    return steam_ids.put(userInfo["steam_id_64"])

                else:
                    return print(f"{steam_id} {level} {price}")
        except:
            return players.put(player)