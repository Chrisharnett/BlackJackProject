#!/usr/bin/env/python3

import db
import random
import time
from decimal import Decimal
from decimal import ROUND_HALF_UP


def endGame(playerHand, dealerHand, bet, money, winner):
    print()
    print("Results")
    printTable(playerHand, dealerHand)
    printScore(playerHand, dealerHand)
    time.sleep(1)
    bet = bet.quantize(Decimal("1.00"), ROUND_HALF_UP)
    if winner == 'b':
        bet = (bet * Decimal(1.5)).quantize(Decimal("1.00"), ROUND_HALF_UP)
        money += bet
        print("BlackJack!")
        print(f"Amazing! You win {bet}")
    elif winner == 'd':
        money -= bet
        if handValue(dealerHand) == 21:
            print("Dealer BlackJack!")
        print("Sorry. You Lose")
    elif winner == 't':
        print("Tie! No winner")
    elif winner == 'p':
        print("Congratulations, you win!")
        money += bet
    db.write_cash_money(str(money))
    print(f"Money: {money}")
    return money


def printScore(playerHand, dealerHand):
    playerPoints = playersHandValue(playerHand)
    dealerPoints = handValue(dealerHand)
    if playersHandValue(playerHand) > 21:
        playerPoints = "BUST"
    if handValue(dealerHand) > 21:
        dealerPoints = "BUST"
    print(f"{'DEALERS POINTS: ':{'20'}}{dealerPoints:{'<10'}}")
    print(f"{'YOUR POINTS: ':{'20'}}{playerPoints:{'<10'}}")


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
    if hand.count("A") < 1 and handValue(hand) > 21:
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


def handValue(hand):
    value = 0
    for card in hand:
        value += int(card[2])
    return value


def playersHandValue(hand):
    for count, card in enumerate(hand):
        if '11' in card:
            while handValue(hand) > 21:
                i = count
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
    if handValue(dealerHand) > playersHandValue(playerHand):
        return 'd'
    while handValue(dealerHand) < 17 or handValue(dealerHand) < playersHandValue(playerHand):
        newCard = deck.pop()
        dealerHand.append(newCard)
        if 'A' in newCard:
            dealerAce(dealerHand)
        printTable(playerHand, dealerHand)
    if handValue(dealerHand) > 21:
        return 'p'
    if handValue(dealerHand) > playersHandValue(playerHand):
        return 'd'
    if handValue(dealerHand) == playersHandValue(playerHand):
        return 't'


def playersTurn(deck, playerHand, dealerHand):
    play = input("Would you like to hit or stand?   ")
    while play.lower() == "hit":
        card = deck.pop()
        playerHand.append(card)
        printTable(playerHand, dealerHand[1:])
        if playersHandValue(playerHand) == 21:
            print("21 points!")
            break
        elif playersHandValue(playerHand) > 21:
            print("You're bust!")
            return 'd'
        else:
            time.sleep(1)
        play = input("Would you like to hit or stand?   ")
        if play.lower() == "stand":
            break
        elif play.lower() != "hit":
            print("Invalid entry. Type 'hit' or 'stand'")
            play = input("Would you like to hit or stand?   ")
            continue
    if handValue(dealerHand) > playersHandValue(playerHand):
        return 'd'
    elif handValue(dealerHand) == playersHandValue(playerHand):
        return 't'
    else:
        return 'n'


def startGame(deck, playerHand, dealerHand):
    for x in range(2):
        card = deck.pop()
        playerHand.append(card)
        card = deck.pop()
        dealerHand.append(card)
        if 'A' in card:
            dealerAce(dealerHand)
        printTable(playerHand, dealerHand[1:])
    if playersHandValue(playerHand) == 21:
        if handValue(dealerHand) == 21:
            return 't'
        else:
            return "b"
    elif handValue(dealerHand) == 21:
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
    if len(dealerHand) == 0:
        print(f"DEALER'S SHOW CARD: \n??\n")
    else:
        print(f"DEALER'S SHOW CARD:\n{showHand(dealerHand)}")
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
