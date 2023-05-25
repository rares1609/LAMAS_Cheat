class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        pass  # Code to create the deck of cards using the Card class.

    def shuffle(self):
        pass  # Code to shuffle the deck.

    def deal(self):
        pass  # Code to deal a card from the deck.

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw(self, deck):
        pass  # Code to draw a card from the deck into the player's hand.

    def play(self, rank):
        pass  # Code to play a card of a specific rank. It could lie.

    def call_cheat(self, player):
        pass  # Code to call "cheat" on another player.

class Game:
    def __init__(self, players):
        self.players = players
        self.deck = Deck()
        self.pile = []
        self.current_rank = None

    def start(self):
        pass  # Code to start the game, shuffle the deck and deal the cards.

    def play_round(self):
        pass  # Code to make each player take their turn.

    def check_cheat(self, player):
        pass  # Code to check if a player was cheating when called out.

    def end_game(self):
        pass  # Code to check if the game has ended (one player has no cards left), and announce the winner.


def main():
    players = [Player("Player1"), Player("Player2"), Player("Player3"), Player("Player4")]
    game = Game(players)
    game.start()

    while not game.end_game():
        game.play_round()

if __name__ == "__main__":
    main()
