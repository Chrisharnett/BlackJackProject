#!/usr/bin/env/python3

import db
import random
import time


def endGame(playerHand, dealerHand, bet, money, winner):
    print()
    print("Results")
    printTable(playerHand, dealerHand)
    printScore(playerHand, dealerHand)
    time.sleep(1)
    result = ""
    if winner == 'b':
        bet = (bet * 1.5)
        money += bet
        result += "BlackJack! "
        result += f"Amazing! You win {bet:.2f} "
    elif winner == 'd':
        money -= bet
        if handValue(dealerHand) == 21:
            result += "Dealer BlackJack! "
        result += "Sorry. You Lose "
    elif winner == 't':
        result += "Tie! No winner "
    elif winner == 'p':
        result += "Congratulations, you win! "
        money += bet
    db.writeCashMoney(str(money))
    print(result)
    print(f"Money: {money:.2f}")
    return money


def printScore(playerHand, dealerHand):
    playerPoints = handValue(playerHand)
    dealerPoints = handValue(dealerHand)
    if handValue(playerHand) > 21:
        playerPoints = "BUST"
    if handValue(dealerHand) > 21:
        dealerPoints = "BUST"
    print(f"{'DEALERS POINTS: ':{'20'}}{dealerPoints:{'<10'}}")
    print(f"{'YOUR POINTS: ':{'20'}}{playerPoints:{'<10'}}")
    print()


def playerBet(money):
    print()
    print(f"Money: {money:.2f}")
    if money < 5:
        moreMoney = input("You're out of money. Would you like to buy more chips (y/n)?:  ")
        if moreMoney.lower() == "y":
            money = 100
            print(f"Money: {money:.2f}")
        else:
            return 0, money
    while True:
        try:
            betAmount = float(input("Bet Amount: "))
            if betAmount > money:
                print("You don't have enough money, try again.")
            elif 5 < betAmount < 1000:
                return betAmount, money
            else:
                raise ValueError
        except ValueError:
            print("Invalid bet. Bets must be a number between 5 and 1000.")


def dealerAce(hand):
    index = -1
    # Make the first ace 11 unless it busts the hand.
    if hand.count("A") < 1 and handValue(hand) > 21:
        for count, card in enumerate(hand):
            if card[0].upper() == "A":
                hand[count-1][2] = "1"
    # Make all subsequent aces worth 11
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


def playerAce(card):
    while True:
        print(f"{card[0]}{card[1]}")
        try:
            aceValue = input("An Ace! Would you like to make this ace 11 or 1?")
            if aceValue == '1':
                card[2] = aceValue
                break
            elif aceValue == '11':
                break
            else:
                print("Invalid input, try again")
        except ValueError:
            print("Invalid selection. Aces can only be 1 or 11.")
    return card


def showHand(hand):
    handString = ""
    for card in hand:
        handString += f"{card[0]}{card[1]}\n"
    return handString


def dealerTurn(deck, playerHand, dealerHand):
    printTable(playerHand, dealerHand)
    if handValue(dealerHand) > handValue(playerHand):
        return 'd'
    while handValue(dealerHand) < 17 or handValue(dealerHand) < handValue(playerHand):
        newCard = deck.pop()
        dealerHand.append(newCard)
        if 'A' in newCard:
            dealerAce(dealerHand)
        printTable(playerHand, dealerHand)
    if handValue(dealerHand) > 21:
        return 'p'
    elif handValue(dealerHand) > handValue(playerHand):
        return 'd'
    elif handValue(dealerHand) == handValue(playerHand):
        return 't'


def playersTurn(deck, playerHand, dealerHand):
    while True:
        play = input("Would you like to hit or stand?   ")
        if play.lower() == "stand":
            break
        elif play.lower() == "hit":
            card = deck.pop()
            if 'A' in card:
                if handValue(playerHand) > 10:
                    card[2] = 1
                else:
                    card = playerAce(card)
            playerHand.append(card)
            printTable(playerHand, dealerHand[1:])
            if handValue(playerHand) == 21:
                print("21 points!")
                break
            elif handValue(playerHand) > 21:
                print("You're bust!")
                return 'd'
            else:
                time.sleep(1)
        else:
            print("Invalid entry. Type 'hit' or 'stand'")
    if handValue(dealerHand) > handValue(playerHand):
        return 'd'
    elif handValue(dealerHand) == handValue(playerHand):
        return 't'
    else:
        return 'n'


def startGame(deck, playerHand, dealerHand):
    for x in range(2):
        card = deck.pop()
        if 'A' in card:
            if handValue(playerHand) > 10:
                card[2] = 1
            else:
                card = playerAce(card)
        playerHand.append(card)
        card = deck.pop()
        dealerHand.append(card)
        if 'A' in card:
            dealerAce(dealerHand)
        printTable(playerHand, dealerHand[1:])
    if handValue(playerHand) == 21:
        if handValue(dealerHand) == 21:
            return 't'
        else:
            return "b"
    elif handValue(dealerHand) == 21:
        return "d"
    else:
        return "n"


def newDeck():
    # Create and shuffle a new deck
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
    if len(dealerHand) <= 1:
        print(f"DEALER'S SHOW CARD: \n?? {showHand(dealerHand)}\n")
    else:
        print(f"DEALER'S CARDs:\n{showHand(dealerHand)}")
    print(f"YOUR CARDS:\n{showHand(playerHand)}")
    time.sleep(2)


def main():
    print("BLACKJACK!")
    print("Blackjack payout is 3:2")
    money = float(db.loadMoneyFromDisk())
    playAgain = 'y'
    while playAgain == 'y':
        bet, money = playerBet(money)
        if money < 5:
            break
        deck = newDeck()
        playerHand = []
        dealerHand = []
        # variable winner tracks whether conditions for winning the game are met along the way. n = no winner
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
        time.sleep(1)
        playAgain = input("Play again(y/n):  ")
    print()
    print("Come Back soon!")
    print("Goodbye")


if __name__ == '__main__':
    main()
