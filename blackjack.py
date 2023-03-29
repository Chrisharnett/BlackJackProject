#!/usr/bin/env/python3

import db
import random
import time

CLUBS = "\u2663"
SPADES = "\u2660"
HEARTS = "\u2661"
DIAMONDS = "\u2662"


def blackJack():
    pass


def bet():
    pass


def dealerAce(hand):
    index = -1
    for count, number in enumerate(hand):
        if number.upper() == 'A':
            index = count - 1
            if showValue(hand) <= 10:
                hand[index][2] = "11"
            else:
                hand[index][2] = "1"
    return hand


def playerAce(hand):
    index = -1
    for count, card in enumerate(hand):
        if card[0].upper() == 'A':
            index = count - 1
            if showValue(hand) > 10:
                print("This ace is worth 1!")
                return hand
            else:
                while True:
                    ace_value = input("Nice, an Ace! Would you like it to be worth 1 or 11 points? ")
                    if ace_value == '1' or ace_value == '11':
                        hand[index][2] = ace_value
                        return hand
                    else:
                        print("The Ace can be worth only 1 or 11.")


def showValue(hand):
    value = 0
    for card in hand:
        value += int(card[2])
    return value


def showHand(hand):
    handString = ""
    for card in hand:
        handString += f"{card[0]}{card[1]}" + ","
    return handString


def dealCard(deck):
    return deck.pop()


def newDeck():
    suits = [CLUBS, SPADES, HEARTS, DIAMONDS]
    numbers = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    deck = []
    value = ""
    for suit in suits:
        for number in numbers:
            if number.upper() == "A":
                value = "1"
            elif number == "J" or number == "Q" or number == "K":
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
    playerHand = []
    dealerHand = []
    print("Let's deal the cards.")

    #  Start the game
    for x in range(2):
        card = deck.pop()
        playerHand.append(card)
        if 'A' in card:
            playerAce(playerHand)
        print()
        print(f"Player's Hand: {showHand(playerHand)}")
        print(f"Hand Value: {showValue(playerHand)}")
        time.sleep(1)
        print()
        dealCard(deck, dealerHand)
        if 'A' in dealerHand:
            dealerHand = dealerAce(dealerHand)
        if len(dealerHand) == 1:
            print("Dealer receives 1 card face down")
        elif len(dealerHand) > 1:
            print(f"Dealer's Hand: {showHand(dealerHand[1:])}")
        time.sleep(1)

    play = input("Would you like to hit or stand?   ")
    while play == "hit":
        dealCard(deck, playerHand)
        if 'A' in playerHand:
            playerHand = playerAce(playerHand)
        print(f"Player's Hand: {showHand(playerHand)}")
        print(f"Hand Value: {showValue(playerHand)}")
        if showValue(playerHand) > 21:
            print("Sorry, you're bust! Better luck next time.")
            break
        time.sleep(1)
        play = input("Would you like to hit or stand?   ")


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
