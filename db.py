import sys

FILENAME = "money.txt"


def load_money_from_disk():
    money = 0
    try:
        with open(FILENAME) as file:
            money = file.read()
        if money == 0:
            money = 100
        return money
    except FileNotFoundError:
        print("Money file not found. Starting with $100")
    except Exception as e:
        print("Unknown exception occured. Exiting program.")
        print(type(e), e)
        sys.exit(1)


def write_cash_money(money):
    try:
        with open(FILENAME, "w") as file:
            file.write(money)
    except Exception as e:
        print("Unknown Exception, Closing Program")
        print(type(e), e)
        sys.exit(1)





