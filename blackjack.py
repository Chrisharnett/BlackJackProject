#!/usr/bin/env/python3

import db
import random

CLUBS = "\u2663"
SPADES = "\u2660"
HEARTS = '\u2661'
DIAMONDS = '\u2662'


def blackJack():
    pass


def bet():
    pass


def ace():
    pass


def stand():
    pass


def hit():
    pass


def dealCards():
    pass


def newDeck():
    suits = [CLUBS, SPADES, HEARTS, DIAMONDS]
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
    wallet = db.load_money_from_disk()
    deck = newDeck()
    print(deck)


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
