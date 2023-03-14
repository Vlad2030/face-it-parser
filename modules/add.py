from datetime import datetime

import get


def token(token: str, client_token: str) -> None:
    nickname: dict = get.me(token)["payload"]["nickname"]
    now: float = datetime.now()

    if token and not client_token:
        with open("tokens_site.txt", "a") as file:
            file.write(f"{token} {nickname} {now}\n")
        return print(f"{token} {nickname} {now} - добавлен")

    if token and client_token:
        with open("tokens_server.txt", "a") as file:
            file.write(f"{token} {nickname} {now}\n")
        return print(f"{token} {nickname} {now} - добавлен")
