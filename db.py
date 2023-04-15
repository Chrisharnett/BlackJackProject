import sys

FILENAME = "money.txt"


def loadMoneyFromDisk():
    money = 0
    try:
        with open(FILENAME) as file:
            money = file.read()
        return money
    except FileNotFoundError:
        print("Money file not found. A new file while be created")
    except Exception as e:
        print("Unknown exception occurred. Exiting program.")
        print(type(e), e)
        sys.exit(1)


def writeCashMoney(money):
    try:
        with open(FILENAME, "w") as file:
            file.write(money)
    except Exception as e:
        print("Unknown Exception, Closing Program")
        print(type(e), e)
        sys.exit(1)





