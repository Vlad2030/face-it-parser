from datetime import datetime
import get


def clientToken(token):
    f = open("tokens_site.txt", "a")
    nickname = get.me(token)["payload"]["nickname"]
    now = datetime.now()
    f.write(f"\n{token} {nickname} {now}")
    print(f"{token} {nickname} {now} - добавлен")
    f.close()


def serverToken(token, clientToken):
    f = open("tokens_server.txt", "a")
    nickname = get.me(clientToken)["payload"]["nickname"]
    now = datetime.now()
    f.write(f"{token} {nickname} {now}\n")
    print(f"{token} {nickname} {now} - добавлен")
    f.close()