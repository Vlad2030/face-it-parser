import requests
import math
import json
from queue import Queue
import threading
from datetime import datetime
from modules import add
from modules import check
from modules import filters
from modules import get
from modules import main
from modules import saver
from modules import send



if __name__ == "__main__":
    data = get.itemsPrice()
    regions = {
        1: "EU",
        2: "US",
        3: "SEA",
        4: "Oceania",
        5: "SA",
    }
    region_index = int(
        input(
            "\n\n1 - EU\n2 - US\n3 - SEA\n4 - Oceania\n5 - SA\n6 - US, SEA, Oceania, SA\nВведите номер региона: "
        )
    )
    amount = int(input("Введите сколько раз парсить: "))
    matches = Queue()
    players = Queue()
    steam_ids = Queue()
    main.start()
    save_thread = threading.Thread(target=saver, args=(steam_ids, players))
    save_thread.start()
    for i in range(main.thread_count):
        main.threads[i].join()
    save_thread.join()
