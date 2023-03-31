#!/usr/bin/env/python3

import db
import random
import time
from decimal import Decimal

CLUBS = "\u2663"
SPADES = "\u2660"
HEARTS = "\u2661"
DIAMONDS = "\u2662"


def player_bet(money):
    print()
    print(f"Money: {money}")
    bet_amount = Decimal(input("Bet Amount: "))
    return bet_amount


def dealerAce(hand):
    index = -1
    for count, number in enumerate(hand):
        if number[0].upper() == "A":
            index = count - 1
            if len(hand) < 2 or (17 < handValue(hand) + 11 <= 21):
                hand[index][2] = "11"
    return hand


def playerAce(hand):
    index = -1
    for count, card in enumerate(hand):
        if card[0].upper() == "A":
            index = count - 1
            if handValue(hand) > 10:
                print("This ace is worth 1!")
                return hand
            if handValue(hand) == 10:
                print("This ace is worth 11")
            else:
                while True:
                    ace_value = input("Nice, an Ace! Would you like it to be worth 1 or 11 points? ")
                    if ace_value == "11":
                        hand[index][2] = ace_value
                        return hand
                    elif ace_value != "1":
                        print("The Ace can be worth only 1 or 11.")


def handValue(hand):
    value = 0
    for card in hand:
        value += int(card[2])
    return value


def showHand(hand):
    handString = ""
    for card in hand:
        handString += f"{card[0]}{card[1]}\n"
    return handString


def dealerTurn(deck, hand, playerHand):
    print(f"DEALER'S CARDS:\n{showHand(hand)}")
    if handValue(hand) > handValue(playerHand):
        return "d"

    time.sleep(1)
    print()
    while handValue(hand) <= handValue(playerHand):
        newCard = deck.pop()
        if 'A' in newCard:
            dealerAce(hand)
        hand.append(newCard)
        print(f"DEALER'S CARDS:\n{showHand(hand)}")
        if (handValue(hand)) > (handValue(hand)) and handValue(hand) < 21:
            return "d"
        if handValue(hand) > 21:
            print("Dealer is bust.")
            return "p"
        elif handValue(hand) == 21:
            print("Dealer gets BlackJack, dealer wins")
            return "d"
        else:
            time.sleep(1)


def playersTurn(deck, hand):
    play = input("Would you like to hit or stand?   ")
    print()
    while play == "hit":
        card = deck.pop()
        hand.append(card)
        if 'A' in card:
            playerAce(hand)
        print()
        print(f"YOUR CARDS:\n{showHand(hand)}")
        if handValue(hand) == 21:
            print("BlackJack!")
            return "p"
        elif handValue(hand) > 21 and 'A' in hand:
            index = -1
            for count, card in enumerate(hand):
                if 'A' in card:
                    index = count - 1
                    hand[index][2] = 1
            print("Ace is now worth 1.")
            print(f"YOUR CARDS:\n{showHand(hand)}")
        elif handValue(hand) > 21:
            print("Sorry, you're bust!")
            return "d"
        else:
            time.sleep(1)
        play = input("Would you like to hit or stand?   ")
        if play.lower() == "stand":
            return


def startGame(deck, playerHand, dealerHand):
    for x in range(2):
        card = deck.pop()
        playerHand.append(card)
        if 'A' in card:
            print(f"YOUR CARDS:\n{showHand(playerHand)}")
            playerAce(playerHand)
        card = deck.pop()
        dealerHand.append(card)
        if 'A' in card:
            dealerAce(dealerHand)
    print(f"DEALER'S SHOW CARD:\n{showHand(dealerHand[1:])}")
    print(f"YOUR CARDS:\n{showHand(playerHand)}")
    if handValue(playerHand) == 21:
        print("BLACKJACK!")
        return "b"
    elif handValue(dealerHand) == 21:
        print(f"DEALER'S CARDS:\n{showHand(dealerHand)}")
        print("Dealer hits Blackjack!")
        return "d"
    time.sleep(1)

    return "no"


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
    print("BLACKJACK!")
    print("Blackjack payout is 3:2")
    money = Decimal(db.load_money_from_disk())
    deck = newDeck()
    bet = "0"
    play = True
    while True:
        bet = player_bet(money)
        playerHand = []
        dealerHand = []
        winner = "no"
        while winner == "no":
            winner = startGame(deck, playerHand, dealerHand)
            if winner == "p" or winner == "d":
                break
            winner = playersTurn(deck, playerHand)
            if winner == "p" or winner == "d":
                break
            winner = dealerTurn(deck, dealerHand, playerHand)
            if winner == "p" or winner == "d":
                break
        print()
        print(f"YOUR POINTS: {handValue(playerHand)}")
        print(f"DEALER'S POINTS: {handValue(dealerHand)}")
        if handValue(playerHand) > handValue(dealerHand) or winner == 'p':
            print("Congratulations, you win!")
        if winner == "b":
            money += (bet * Decimal(3/2))
        elif winner == "p":
            money += bet
        elif winner == 'd':
            money -= bet
            print("Sorry, You lose")
        else:
            print("Tie! No winner")
        print(f"Money: {money}")
        print()
        play_again = input("Play again(y/n):  ")
        if play_again.lower() != 'y':
            break
    print("Come Back soon!")
    print("Goodbye")


if __name__ == '__main__':
    main()
