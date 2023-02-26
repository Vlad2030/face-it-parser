import get


filtres = {
    "level": {
        "work": False,
    },
    "price": {
        "work": False
    },
}

def startFiltresInputs() -> None:
    val_from = filtres["level"]["from"]
    val_to = filtres["level"]["to"]

    if filtres["level"]["work"]:
        print(f"1 - фильтрация по уровню (от {val_from} до {val_to})")
    else:
        print("1 - фильтрация по уровню")

    if filtres["price"]["work"]:
        print(f"2 - фильтрация по стоимости (от {val_from} до {val_to})")
    else:
        print("2 - фильтрация по стоимости")

    print("0 - продолжить")
    value: int = input("Введите номер фильтра: ")
    return get.valueFiltres(value)