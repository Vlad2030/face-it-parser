import get

filtres = {
    "level": {
        "work": False,
    },
    "price": {
        "work": False
    },
}

def startFiltresInputs():
    if not filtres["level"]["work"]:
        print("1 - фильтрация по уровню")
    else:
        val_from = filtres["level"]["from"]
        val_to = filtres["level"]["to"]
        print(f"1 - фильтрация по уровню (от {val_from} до {val_to})")
    if not filtres["price"]["work"]:
        print("2 - фильтрация по стоимости")
    else:
        val_from = filtres["price"]["from"]
        val_to = filtres["price"]["to"]
        print(f"2 - фильтрация по стоимости (от {val_from} до {val_to})")
    print("0 - продолжить")
    value = input("Введите номер фильтра: ")
    get.valueFiltres(value)