#!/usr/bin/env/python3

import db
import random
import time
from decimal import Decimal
from decimal import ROUND_HALF_UP


def endGame(playerHand, dealerHand, bet, money, winner):
    printScore(playerHand, dealerHand)
    time.sleep(1)
    bet = bet.quantize(Decimal("1.00"), ROUND_HALF_UP)
    if winner == 'b':
        money += (bet * Decimal(1.5)).quantize(Decimal("1.00"), ROUND_HALF_UP)
        print("BlackJack!")
        print(f"Amazing! You win {bet}")
    elif winner == 'p' or dealersHandValue(dealerHand) < playersHandValue(playerHand):
        print("Congratulations, you win!")
        money += bet
    elif winner == 'd' or dealersHandValue(dealerHand) > playersHandValue(playerHand):
        money -= bet
        print()
        print("Dealer wins")
    elif winner == 't' or dealersHandValue(dealerHand) == playersHandValue(playerHand):
        print("Tie! No winner")

    db.write_cash_money(str(money))
    print(f"Money: {money}")
    print()
    return money


def printScore(playerHand, dealerHand):
    playerPoints = dealersHandValue(playerHand)
    dealerPoints = dealersHandValue(dealerHand)
    if playersHandValue(playerHand) > 21:
        playerPoints = "BUST"
    if dealersHandValue(dealerHand) > 21:
        dealerPoints = "BUST"
    print(f"{'YOUR POINTS: ':{'20'}}{playerPoints:{'<10'}}")
    print(f"{'DEALERS POINTS: ':{'20'}}{dealerPoints:{'<10'}}")


def player_bet(money):
    print()
    print(f"Money: {money}")
    if money < 5:
        more_money = input("You're out of money. Would you like to buy more chips (y/n)?:  ")
        if more_money.lower() == "y":
            money = 100
            print(f"Money: {money}")
        else:
            return
    while True:
        try:
            bet_amount = Decimal(input("Bet Amount: "))
            if bet_amount > money:
                print("You don't have enough money, try again.")
            elif 5 > bet_amount > 1000:
                raise ValueError
            else:
                return bet_amount, money
        except ValueError:
            print("Invalid bet. Bets must be between 5 and 1000.")


def dealerAce(hand):
    index = -1
    if hand.count("A") < 1 and dealersHandValue(hand) > 21:
        for count, card in enumerate(hand):
            if card[0].upper() == "A":
                hand[count-1][2] = "1"
    if hand.count("A") >= 1:
        for count, card in enumerate(hand):
            indices = []
            if card[0].upper() == "A":
                indices.append(count - 1)
            for i in indices[1:]:
                hand[i][2] = 1
    return hand


def dealersHandValue(hand):
    value = 0
    for card in hand:
        value += int(card[2])
    return value


def playersHandValue(hand):
    while dealersHandValue(hand) > 21:
        if '11' in hand:
            i = hand.index("11")
            hand[i][2] = "1"
    value = 0
    for card in hand:
        value += int(card[2])
    return value


def showHand(hand):
    handString = ""
    for card in hand:
        handString += f"{card[0]}{card[1]}\n"
    return handString


def dealerTurn(deck, playerHand, dealerHand):
    printTable(playerHand, dealerHand)
    if dealersHandValue(dealerHand) > playersHandValue(playerHand):
        return 'd'
    while dealersHandValue(dealerHand) < 17 or dealersHandValue(dealerHand) < playersHandValue(playerHand):
        newCard = deck.pop()
        dealerHand.append(newCard)
        if 'A' in newCard:
            dealerAce(dealerHand)
        printTable(playerHand, dealerHand)
    if dealersHandValue(dealerHand) > 21:
        return 'p'
    if dealersHandValue(dealerHand) > playersHandValue(playerHand):
        return 'd'
    if dealersHandValue(dealerHand) == playersHandValue(playerHand):
        return 't'


def playersTurn(deck, playerHand, dealerHand):
    play = input("Would you like to hit or stand?   ")
    while play == "hit":
        card = deck.pop()
        playerHand.append(card)
        printTable(playerHand, dealerHand)
        if playersHandValue(playerHand) == 21:
            print("21 points!")
            break
        elif playersHandValue(playerHand) > 21:
            print("You're bust!")
            return "d"
        else:
            time.sleep(1)
        play = input("Would you like to hit or stand?   ")
    if dealersHandValue(dealerHand) > playersHandValue(playerHand):
        return 'd'
    elif dealersHandValue(dealerHand) == playersHandValue(playerHand):
        return 't'
    else:
        return 'n'


def startGame(deck, playerHand, dealerHand):
    for x in range(2):
        card = deck.pop()
        playerHand.append(card)
        printTable(playerHand, dealerHand)
        card = deck.pop()
        dealerHand.append(card)
        if 'A' in card:
            dealerAce(dealerHand)
        printTable(playerHand, dealerHand)
    if playersHandValue(playerHand) == 21:
        if dealersHandValue(dealerHand) == 21:
            return 't'
        else:
            return "b"
    elif dealersHandValue(dealerHand) == 21:
        return "d"
    else:
        return "n"


def newDeck():
    print("Shuffling the deck.")
    time.sleep(1)
    suits = ["\u2663", "\u2660", "\u2661", "\u2662"]
    numbers = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    deck = []
    for suit in suits:
        for number in numbers:
            if number.upper() == "A":
                value = "11"
            elif number == "J" or number == "Q" or number == "K":
                value = "10"
            else:
                value = number
            deck.append([number, suit, value])
        random.shuffle(deck)
    return deck


def printTable(playerHand, dealerHand):
    print()
    print(f"DEALER'S SHOW CARD:\n{showHand(dealerHand[1:])}")
    print(f"YOUR CARDS:\n{showHand(playerHand)}")
    time.sleep(2)


def main():
    print("BLACKJACK!")
    print("Blackjack payout is 3:2")
    money = Decimal(db.load_money_from_disk())

    # bet = 0
    play_again = 'y'
    while play_again == 'y':
        bet, money = player_bet(money)
        if money < 5:
            break
        deck = newDeck()
        playerHand = []
        dealerHand = []

        winner = "n"
        while winner == "n":
            winner = startGame(deck, playerHand, dealerHand)
            if winner != "n":
                break
            winner = playersTurn(deck, playerHand, dealerHand)
            if winner != "n":
                break
            winner = dealerTurn(deck, playerHand, dealerHand)
        money = endGame(playerHand, dealerHand, bet, money, winner)

        print()
        time.sleep(2)
        play_again = input("Play again(y/n):  ")

    print("Come Back soon!")
    print("Goodbye")


if __name__ == '__main__':
    main()
