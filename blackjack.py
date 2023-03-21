#!/usr/bin/env/python3

import db
import random


def newDeck():
    suits = ["clubs", "spades", "hearts", "diamonds"]
    numbers = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    deck = []
    for suit in suits:
        for number in numbers:
            if number.upper() == "A":
                value = "1"
            if number == "J" or number == "Q" or number == "K":
                value = "10"
            else:
                value = number
            deck.append([number, suit, value])
        random.shuffle(deck)
    return deck


def main():
    print("BlackJack Project")
    money = db.load_money_from_disk()
    deck = newDeck()


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
