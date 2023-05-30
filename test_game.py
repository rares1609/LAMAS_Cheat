import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

class Player:
    def __init__(self, name, play_strategy, call_bluff_strategy):
        self.name = name
        self.hand = []
        self.play_strategy = play_strategy
        self.call_bluff_strategy = call_bluff_strategy

    def play_card(self):
        return self.play_strategy(self)

    def call_bluff(self, game):
        return self.call_bluff_strategy(self, game)

    def take_pile(self, pile):
        self.hand.extend(pile)

    def __repr__(self):
        return self.name

def play_strategy_0th_order(player):
    if game.current_rank is None:
        card = random.choice(player.hand)
        player.hand.remove(card)
        return card

    for card in player.hand:
        if card.rank == game.current_rank:
            player.hand.remove(card)
            return card

    # If the player doesn't have a card of the current rank, lie
    card = random.choice(player.hand)
    player.hand.remove(card)
    return card

def call_bluff_strategy_0th_order(player, game):
    if game.current_rank is not None and not any(card.rank == game.current_rank for card in player.hand):
        return True  # Call bluff if player does not have a card of the current rank
    return False  # Otherwise, do not call bluff

class Game:
    def __init__(self, players):
        self.players = players
        self.pile = []
        self.current_rank = None
        self.current_player_index = random.randint(0, len(self.players)-1)

    def deal(self):
        deck = [Card(rank, suit) for rank in ['A', 'K', 'Q', 'J'] for suit in ['Red Heart', 'Black Heart', 'Diamond']]
        random.shuffle(deck)
        while deck:
            for player in self.players:
                if deck:
                    player.hand.append(deck.pop())

    def play_turn(self):
        # Get the current player
        current_player = self.players[self.current_player_index]
        
        # The current player plays a card
        card = current_player.play_card()
        
        if card:
            # If a card is played, add it to the pile and update the current rank
            self.pile.append(card)
            self.current_rank = card.rank
            print(f"{current_player} played {card}")
            
            # Get the next player
            next_player = self.players[(self.current_player_index+1)%len(self.players)]
            
            # The next player calls a bluff
            if next_player.call_bluff(self):
                print(f"{next_player} calls bluff on {current_player}")
                
                # Check if the last card played matches the current rank
                # If it does, the bluff was false
                if self.pile[-1].rank == self.current_rank:
                    # The next player was wrong to call a bluff, so they take the pile
                    next_player.take_pile(self.pile)
                    print(f"{next_player} was wrong. {next_player} takes the pile.")
                else:  
                    # The bluff was true, the current player was caught lying
                    # They take the pile
                    current_player.take_pile(self.pile)
                    print(f"{current_player} was caught lying. {current_player} takes the pile.")
                
                # After a bluff has been called, the pile is emptied
                self.pile = []
                
                # Reset the current rank because a new round starts
                self.current_rank = None 

        # Move on to the next player
        self.current_player_index = (self.current_player_index + 1) % len(self.players)



    def game_over(self):
        for player in self.players:
            if len(player.hand) == 0:
                return player
        return None

    def play_game(self):
        self.deal()
        winner = self.game_over()
        while not winner:
            self.play_turn()
            winner = self.game_over()
        print(f"{winner} is the winner!")
        

player1 = Player('Player1', play_strategy_0th_order, call_bluff_strategy_0th_order)
player2 = Player('Player2', play_strategy_0th_order, call_bluff_strategy_0th_order)
player3 = Player('Player3', play_strategy_0th_order, call_bluff_strategy_0th_order)

game = Game([player1, player2, player3])
game.play_game()
