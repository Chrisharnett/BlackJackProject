#!/usr/bin/env/python3

import db
import random
import time
from decimal import Decimal
from decimal import ROUND_HALF_UP


def endGame(playerHand, dealerHand, bet, money, winner):
    playerPoints = handValue(playerHand)
    dealerPoints = handValue(dealerHand)
    if handValue(playerHand) > 21:
        playerPoints = "BUST"
    if handValue(dealerHand) > 21:
        dealerPoints = "BUST"
    print(f"{'YOUR POINTS: ':{'20'}}{playerPoints:{'<10'}}")
    print(f"{'DEALERS POINTS: ':{'20'}}{dealerPoints:{'<10'}}")
    time.sleep(1)
    bet = bet.quantize(Decimal("1.00"), ROUND_HALF_UP)
    if handValue(dealerHand) < handValue(playerHand) <= 21:
        winner = "p"

    if winner == "b":
        money += (bet * Decimal(1.5)).quantize(Decimal("1.00"), ROUND_HALF_UP)
        print(f"Amazing! You win {bet}")
    elif winner == "p":
        print("Congratulations, you win!")
        money += bet
    elif winner == 'd':
        money -= bet
        print()
        print("Dealer wins")
    else:
        print("Tie! No winner")
    db.write_cash_money(str(money))
    print(f"Money: {money}")
    print()
    return money


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
    if hand.count("A") >= 1:
        for count, card in enumerate(hand):
            indices = []
            if card[0].upper() == "A":
                indices.append(count - 1)
            for i in indices[1:]:
                hand[i][2] = 1
    return hand


# def playerAce(hand):
#     for count, card in enumerate(hand):
#         if card[0].upper() == "A":
#             index = count - 1
#             if handValue(hand) <= 10:
#                 hand[index][2] = "11"
#     return hand
#

def handValue(hand):
    value = 0
    for card in hand:
        value += int(card[2])
    return value


def playersHandValue(hand):
    while handValue(hand) > 21:
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


def dealerTurn(deck, hand, playerHand):
    print(f"DEALER'S CARDS:\n{showHand(hand)}")
    if handValue(hand) > handValue(playerHand):
        return "d"
    time.sleep(1)
    while handValue(hand) < 17:
        newCard = deck.pop()
        if 'A' in newCard:
            dealerAce(hand)
        hand.append(newCard)
        print(f"DEALER'S CARDS:\n{showHand(hand)}")
        if (handValue(hand)) > (handValue(playerHand)) and handValue(hand) < 21:
            return "d"
        elif handValue(hand) == 21:
            print("Dealer gets 21!")
            return "d"
        elif handValue(hand) > 21:
            print("Dealer is bust.")
            return "p"
        else:
            time.sleep(1)


def playersTurn(deck, hand):
    play = input("Would you like to hit or stand?   ")
    while play == "hit":
        card = deck.pop()
        hand.append(card)
        print(f"YOUR CARDS:\n{showHand(hand)}")
        if playersHandValue(hand) == 21:
            print("21 points!")
            return "p"
        elif playersHandValue(hand) > 21:
            print("You're bust!")
            return "d"
        else:
            time.sleep(1)
        play = input("Would you like to hit or stand?   ")
        if play.lower() == "stand":
            return "no"


def startGame(deck, playerHand, dealerHand):
    for x in range(2):
        card = deck.pop()
        playerHand.append(card)
        if len(playerHand) == 2 and playersHandValue(playerHand) == 21:
            print("BLACKJACK!!")
            return "b"
        card = deck.pop()
        dealerHand.append(card)
        if 'A' in card:
            dealerAce(dealerHand)
        if handValue(dealerHand) == 21:
            print(f"DEALER'S CARDS:\n{showHand(dealerHand)}")
            print("Dealer hits Blackjack!")
            return "db"
    print()
    print(f"DEALER'S SHOW CARD:\n{showHand(dealerHand[1:])}")
    print(f"YOUR CARDS:\n{showHand(playerHand)}")
    return "no"


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


def main():
    print("BLACKJACK!")
    print("Blackjack payout is 3:2")
    money = Decimal(db.load_money_from_disk())

    # bet = 0
    player_again = 'y'
    while player_again == 'y':
        bet, money = player_bet(money)
        if money < 5:
            break
        deck = newDeck()
        playerHand = []
        dealerHand = []

        winner = "no"
        while winner == "no":
            winner = startGame(deck, playerHand, dealerHand)
            if winner != "no":
                break
            winner = playersTurn(deck, playerHand)
            if winner != "no":
                break
            winner = dealerTurn(deck, dealerHand, playerHand)
            print()
            time.sleep(2)

            money = endGame(playerHand, dealerHand, bet, money, winner)

        play_again = input("Play again(y/n):  ")
        if play_again.lower() != 'y':
            break
    print("Come Back soon!")
    print("Goodbye")


if __name__ == '__main__':
    main()
