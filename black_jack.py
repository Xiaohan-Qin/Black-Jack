import random
import sys

# Set up constants:
HEARTS = chr(9829)  # Character 9829 is '♥'.
DIAMONDS = chr(9830)  # Character 9830 is '♦'.
SPADES = chr(9824)  # Character 9824 is '♠'.
CLUBS = chr(9827)  # Character 9827 is '♣'.
BACKSIDE = 'backside'


def main():
    print('''

    Rules:
      Try to get as close to 21 without going over.
      Kings, Queens, and Jacks are valued at 10.
      Aces can count as either 1 or 11.
      Cards from 2 through 10 are worth their face value.
      You can either:
      (H)Hit to take another card, or
      (S)Stand to stop taking cards.
      On your first play, you can (D)Double down to increase your bet,
      but must hit exactly one more time before standing.
      In case of a tie, the bet is returned to the player.
      The dealer stops hitting at 17.
      
    Press Crt-C to quit game.
    Have fun!
    ''')

    money = 5000
    while True:  # Main game loop.
        if money <= 0:
            print("You're broke!")
            print('Thanks for playing :)')
            sys.exit()

        # Let player enter their bet for this round:
        print('Money:', money)
        bet = get_bet(money)

        # Give dealer and player two cards from the deck each:
        deck = get_deck()
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

        # Player actions:
        print('Bet:', bet)
        while True:  # Keep looping until player stands or busts.
            display_hands(playerHand, dealerHand, False)
            print()

            if get_hand_value(playerHand) > 21:
                break

            move = get_move(playerHand, money - bet)

            if move == 'D':
                # Doubling down. Player can increase their bet:
                additionalBet = get_bet(min(bet, (money - bet)))
                bet += additionalBet
                print('Bet increased to {}.'.format(bet))
                print('Bet:', bet)

            if move in ('H', 'D'):
                # Hit/doubling down takes another card.
                newCard = deck.pop()
                rank, suit = newCard
                print('You drew a {} of {}.'.format(rank, suit))
                playerHand.append(newCard)

                if get_hand_value(playerHand) > 21:
                    continue

            if move in ('S', 'D'):
                break

        # Dealer's actions:
        if get_hand_value(playerHand) <= 21:
            while get_hand_value(dealerHand) < 17:
                # Dealer hits:
                print('Dealer hits...')
                dealerHand.append(deck.pop())
                display_hands(playerHand, dealerHand, False)

                if get_hand_value(dealerHand) > 21:
                    # Dealer has busted.
                    break
                input('Press Enter to continue...')
                print('\n\n')

        # Show final hands:
        display_hands(playerHand, dealerHand, True)

        playerValue = get_hand_value(playerHand)
        dealerValue = get_hand_value(dealerHand)
        # Handle whether player won, lost, or tied:
        if dealerValue > 21:
            print('Dealer busts! You win ${}!'.format(bet))
            money += bet
        elif (playerValue > 21) or (playerValue < dealerValue):
            print('You lost!')
            money -= bet
        elif playerValue > dealerValue:
            print('You won ${}!'.format(bet))
            money += bet
        elif playerValue == dealerValue:
            print('It\'s a tie, the bet is returned to you.')

        input('Press Enter to continue...')
        print('\n\n')


def get_bet(max_bet):
    """Ask player how much they want to bet for this round."""
    while True:  # Keep asking until they enter a valid amount.
        print('How much do you bet? (1-{}, or QUIT)'.format(max_bet))
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print('Thanks for playing!')
            sys.exit()

        if not bet.isdecimal():
            continue  # If player didn't enter a number, ask again.

        bet = int(bet)
        if 1 <= bet <= max_bet:
            return bet  # Player entered a valid bet.


def get_deck():
    """Return a list of (rank, suit) tuples for all 52 cards."""
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))  # Add the numbered cards.
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))  # Add the face and ace cards.
    random.shuffle(deck)
    return deck


def display_hands(player_hand, dealer_hand, show_dealer_hand):
    """Show the player's and dealer's cards. Hide the dealer's first
    card if showDealerHand is False."""
    print()
    if show_dealer_hand:
        print('DEALER:', get_hand_value(dealer_hand))
        display_cards(dealer_hand)
    else:
        print('DEALER: ???')
        # Hide dealer's first card:
        display_cards([BACKSIDE] + dealer_hand[1:])

    # Show player's cards:
    print('PLAYER:', get_hand_value(player_hand))
    display_cards(player_hand)


def get_hand_value(cards):
    """Returns the value of the cards. Face cards are worth 10, aces are
    worth 11 or 1 (this function picks the most suitable ace value)."""
    value = 0
    numberOfAces = 0

    # Add the value for non-ace cards:
    for card in cards:
        rank = card[0]
        if rank == 'A':
            numberOfAces += 1
        elif rank in ('K', 'Q', 'J'):
            value += 10
        else:
            value += int(rank)

    # Add the value for aces:
    value += numberOfAces  # Add 1 per ace.
    for i in range(numberOfAces):
        # If another 10 can be added without busting, add:
        if value + 10 <= 21:
            value += 10

    return value


def display_cards(cards):
    """Display all the cards in the cards list."""
    rows = ['', '', '', '', '']  # Text to display on each row.

    for i, card in enumerate(cards):
        rows[0] += ' ___  '  # Print top line of the card.
        if card == BACKSIDE:
            # Print a card's back:
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
            # Print the card's front:
            rank, suit = card  # The card is a tuple data structure.
            rows[1] += '|{} | '.format(rank.ljust(2))
            rows[2] += '| {} | '.format(suit)
            rows[3] += '|_{}| '.format(rank.rjust(2, '_'))

    for row in rows:
        print(row)


def get_move(player_hand, money):
    """Asks the player for their move, and returns 'H' for hit, 'S' for
    stand, and 'D' for double down."""
    while True:  # Keep looping until player enters a valid move.
        moves = ['(H)Hit', '(S)Stand']

        # Player can double down on their first move:
        if len(player_hand) == 2 and money > 0:
            moves.append('(D)Double down')

        # Get player's move:
        movePrompt = ', '.join(moves) + '> '
        move = input(movePrompt).upper()
        if move in ('H', 'S'):
            return move
        if move == 'D' and '(D)Double down' in moves:
            return move

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("You've quited the game.")
        sys.exit()


