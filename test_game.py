import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

class Player:
    def __init__(self, name, play_strategy, call_bluff_strategy, is_human= False):
        self.name = name
        self.hand = []
        self.play_strategy = play_strategy
        self.call_bluff_strategy = call_bluff_strategy
        self.is_human = is_human

    def play_card(self):
        if self.is_human:
            print(f"Your hand: {self.hand}")
            action = input("Type the rank of the card you want to play: ").strip()
            for card in self.hand:
                if card.rank == action:
                    self.hand.remove(card)
                    return Card(action, card.suit)  # Return a new card with the claimed rank
            print("Invalid input. You don't have that rank. You lose your turn.")
            return None
        else:
            return self.play_strategy(self)

    def call_bluff(self, game):
        if self.is_human:
            return input("Do you want to call a bluff? (yes/no): ").strip().lower() == "yes"
        else:
            return self.call_bluff_strategy(self, game)
        
    def truth_or_lie(self):
        card_to_play_rank = input("What rank do you want to claim the card has? ").strip()
        print("Human claimed:", card_to_play_rank)
        return card_to_play_rank


    def take_pile(self, pile):
        self.hand.extend(pile.copy())

    def __repr__(self):
        return self.name


class Game:
    def __init__(self, players):
        self.players = players
        self.pile = []
        self.current_rank = None
        self.current_player_index = random.randint(0, len(self.players)-1)

    def deal(self):
        deck = [Card(rank, suit) for rank in ['A', 'K', 'Q'] for suit in ['Red Heart', 'Black Heart', 'Diamond']]
        random.shuffle(deck)
        while deck:
            for player in self.players:
                if deck:
                    player.hand.append(deck.pop())
        
        for player in self.players:
            print(f"\n{player}'s hand: {player.hand}")

    def play_turn(self):
        ok = False
        # Get the current player
        
        current_player = self.players[self.current_player_index] # it clashes with this  one 

        # Player's current turn print
        print(f"\nIt's {current_player}'s turn.")
        
        # The current player plays a card
        card = current_player.play_card()

        
        if card:
            # If a card is played, add it to the pile and update the current rank
            self.pile.append(card)
            if len(self.pile) == 1:
                self.current_rank = current_player.truth_or_lie()
            print(f"Current rank is: {self.current_rank}")
            print(f"{current_player} played {card}")
            
            # Get the next player
            next_player = self.players[(self.current_player_index+1)%len(self.players)]
            print(f"\nIt's {next_player}'s turn.")
            # The next player calls a bluff
            if next_player.call_bluff(self):
                print(f"{next_player} calls bluff on {current_player}")
                
                # Check if the last card played matches the current rank
                # If it does, the bluff was false
                if self.pile[-1].rank == self.current_rank:
                    # The next player was wrong to call a bluff, so they take the pile
                    next_player.take_pile(self.pile)
                    print(f"{next_player} was wrong. {next_player} takes the pile.")
                    ok = True
                    
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
        if ok == False:
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


# STRATEGY FUNCTIONS

# implement this strategy
def play_strategy_trusting(player):
    if game.current_rank is None:
        card = random.choice(player.hand)
        player.hand.remove(card)
        return card
    # Generate a random number between 0 and 1
    random_number = random.random()
    if random_number <= 0.1:
        # If the player doesn't have a card of the current rank, lie
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

# implement this strategy
def play_strategy_distrusting(player):
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

# implement this strategy
def call_bluff_strategy_trusting(player, game):
     # Call bluff or lie if player does not have a card of the current rank
    if game.current_rank is not None and not any(card.rank == game.current_rank for card in player.hand):
        # Generate a random number between 0 and 1
        random_number = random.random()

        if random_number <= 0.3:
            # Call bluff
            print("Agent says Cheat")
            return True
        else:
            # Lie
            return False
    return False  # Otherwise, do not call bluff

# implement this strategy
def call_bluff_strategy_distrusting(player, game):
    # Call bluff or lie if player does not have a card of the current rank
    if game.current_rank is not None and not any(card.rank == game.current_rank for card in player.hand):
        # Generate a random number between 0 and 1
        random_number = random.random()

        if random_number >= 0.3:
            # Call bluff
            print("Agent says Cheat")
            return True
            
        else:
            # Lie
            return False
    else: 
        if game.current_rank is not None and any(card.rank == game.current_rank for card in player.hand):
            # Generate a random number between 0 and 1
            random_number = random.random()
            if random_number <= 0.3:
                # Call bluff
                print("Agent says Cheat")
                return True
            else:
                # Lie or Truth
                return False
            

if __name__ == "__main__":
    player1 = Player('Player 1', play_strategy_trusting, call_bluff_strategy_trusting, is_human= True)
    player2 = Player('Player 2', play_strategy_trusting, call_bluff_strategy_trusting, is_human= True)
    player3 = Player('Player 3', play_strategy_distrusting, call_bluff_strategy_distrusting, is_human= True)

    game = Game([player1, player2, player3])

    game.play_game()



