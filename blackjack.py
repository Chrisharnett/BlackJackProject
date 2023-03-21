#!/usr/bin/env/python3
def deck():
    suits = ["clubs", "spades", "hearts", "diamonds"]
    numbers = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    deck = []
    for suit in suits:
        for number in numbers:
            if number == "A":
                value = 1
            if number == "J" or number == "Q" or number == "K"
                value = 10
            else:
                value = int(number)



def main():
    pass


if __name__ == '__main__':
    main

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
