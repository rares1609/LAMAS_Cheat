import random
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

# Global variables used for printing the final graphs and the probabilties for the Hybrid agent type
global wins_distrusting, wins_hybrid, wins_trusting, prob_D, prob_T, wins_D, wins_T, wins_H

# Counter for the number of winnings per strategy 
wins_trusting = 0
wins_distrusting = 0
wins_hybrid = 0

# Initial probability of choosing strategy trusting and strategy distrusting
prob_T = 0.5
prob_D = 0.5

# Used for storing the averages of wins per strategy 
wins_D = []
wins_T = []
wins_H = []

# Represents the cards used for playing the game
class Card:
    def __init__(self, rank):
        # Initialize a new Card instance with the specified rank.
        self.rank = rank

    def __repr__(self):
        # Returns a string representation of the card.
        return f"{self.rank}"

# Represents a player in the card game.
class Player:
    # Initialize with the name of the player, the strategy for playing cards, the strategy for calling bluff.
    # Moreover, is_human indicates if the player is human. Defaults to False.
    def __init__(self, name, play_strategy, call_bluff_strategy, is_human= False):
        self.name = name
        self.hand = []
        self.play_strategy = play_strategy
        self.call_bluff_strategy = call_bluff_strategy
        self.is_human = is_human
        self.pile_belief = []
        self.cards_played = []

    # Plays a card from the player's hand. 
    def play_card(self):
        if self.is_human:
            rank_counts = Counter(card.rank for card in self.hand)
            hand_str = ', '.join(f"{count}{rank}" for rank, count in rank_counts.items())
            while True:  # Keep asking for input until a valid rank is provided
                print(f"Your hand: {hand_str}")
                action = input("Type the rank of the card you want to play: ").strip()
                for card in self.hand:
                    if card.rank == action:
                        self.hand.remove(card)
                        self.cards_played.append(card)
                        return Card(action)  # Return a new card with the claimed rank
                print("Invalid input. You don't have that rank. Try again.")
        else:
            # If the player is an agent, it calls the play card function for its respective strategy 
            return self.play_strategy(self)

    # Determines if the player wants to call a bluff.
    def call_bluff(self, game):
        if self.is_human:
            while True:  # Keep asking for input until a valid response is provided
                response = input("Do you want to call a bluff? (yes/no): ").strip().lower()
                if response in ["yes", "no"]:
                    return response == "yes"
                else:
                    print("Invalid input. Please type 'yes' or 'no'.")
        else:
            # If the player is an agent, it calls the call bluff function for its respective strategy 
            return self.call_bluff_strategy(self, game)

    # Handles the human part mostly of choosing whether to lie or not about a card
    def truth_or_lie(self):
        if self.is_human:
            while True:  # Keep asking for input until a valid rank is provided
                card_to_play_rank = input("What rank do you want to claim the card has? ").strip()
                if card_to_play_rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
                    print("Human claimed:", card_to_play_rank)
                    return card_to_play_rank
                else:
                    print("Invalid input. Please type a valid rank (A or Q).")
        else: 
            return self.play_strategy(self)
    
    # Discards three cards of the same rank from the player's hand (if found).
    def discard_three_of_a_kind(self, discard_pile):
        rank_counts = Counter(card.rank for card in self.hand)
        for rank, count in rank_counts.items():
            if count == 3:
                self.hand = [card for card in self.hand if card.rank != rank]
                discard_pile.extend(Card(rank) for _ in range(3))
                print(f"{self.name} discarded three {rank}s.")
                return rank 
                
        return 0

    # When a player was caught lying or falsely accused another, this function adds the current pile of cards to its hand
    def take_pile(self, pile):
        self.hand.extend(pile.copy())

    # Returns the name of the player
    def __repr__(self):
        return self.name

# Represents a game of Cheat
class Game:
    def __init__(self, players):
        self.players = players
        self.pile = []
        self.discard_pile = []
        self.current_rank = None
        self.current_player_index = random.randint(0, len(self.players)-1)

    # This method shuffles the deck, deals the cards to the players, and checks if any player has three cards of the
    # same rank. If such a condition is met, the dealing process is repeated until no player has three cards of the
    # same rank.
    def deal(self):
            global wins_distrusting, wins_hybrid, wins_trusting, prob_D, prob_T

            random.shuffle(self.players)         

            while True: 
                deck = [Card(rank) for rank in ['A', 'Q'] for _ in range(3)]  # remove suit here
                random.shuffle(deck)
                
                # Clear each player's hand before dealing
                for player in self.players:
                    player.hand.clear()

                # Deal the cards to the players
                while deck:
                    for player in self.players:  
                        if deck:
                            player.hand.append(deck.pop())
                        
                # Check if any player has three of the same rank
                if any(Counter(card.rank for card in player.hand).most_common(1)[0][1] >= 3 for player in self.players):
                    print("Reshuffling... a player had three cards of the same rank.")
                    continue
                
                # If no player has three cards of the same rank, we can break the loop and continue
                break

            for player in self.players:
                rank_counts = Counter(card.rank for card in player.hand)
                hand_str = ', '.join(f"{count}{rank}" for rank, count in rank_counts.items())
                print(f"\n{player}'s hand: {hand_str}")

            # If hybrid agent, then choose between the trsusting and distrusting strategies based on a weighted average probability
            for player in self.players:
                if player.name == "Hybrid":
                    if random.random() <= prob_T:
                        player.play_strategy = play_strategy_trusting
                        player.call_bluff_stategy = call_bluff_strategy_trusting
                    else:
                        player.play_strategy = play_strategy_distrusting
                        player.call_bluff_stategy = call_bluff_strategy_distrusting

    # Handles how a turn is played by the agents
    def play_turn(self):
        ok = False
        # -1 = that rank is for sure not in the game
        # Discard three of a kind at the start of the turn
        for player in self.players:
            player.discard_three_of_a_kind(self.discard_pile)
           
        # Get the current player
        current_player = self.players[self.current_player_index]

        # Player's current turn print
        print(f"\nIt's {current_player}'s turn.")
        
        # The current player plays a card
        card = current_player.play_card()

        if card:
            # If a card is played, add it to the pile and update the current rank
            self.pile.append(card)
            if len(self.pile) == 1:
                if current_player.name == 'Player 1':
                    self.current_rank = current_player.truth_or_lie()
                else:
                    if len(current_player.hand) > 0:
                        self.current_rank = random.choice('Q' + 'A')
                    else: 
                        self.current_rank = card.rank
                # Reset the pile belief as a new game starts 
                for player in self.players:
                    player.pile_belief = []
            print(f"Current rank is: {self.current_rank}")
            print(f"{current_player} played {card}")

            current_player.pile_belief.append(card)
            
            # Get the next players
            next_player = self.players[(self.current_player_index+1)%len(self.players)]

            # Find next next player
            copy = (self.current_player_index + 1) % len(self.players)
            next_next_player = self.players[(copy+1)%len(self.players)]

            # Update the pile belief system according to each strategy
            if next_player.play_strategy == play_strategy_trusting:
                if self.current_rank == 'A':
                    next_player.pile_belief.append('A')
                else:
                    next_player.pile_belief.append('Q')

            if next_player.play_strategy == play_strategy_distrusting:
                if self.current_rank == 'A':
                    next_player.pile_belief.append('Q')
                else:
                    next_player.pile_belief.append('A')

            
            if next_next_player.play_strategy == play_strategy_trusting:
                if self.current_rank == 'A':
                    next_next_player.pile_belief.append('A')
                else:
                    next_next_player.pile_belief.append('Q')

            if next_next_player.play_strategy == play_strategy_distrusting:
                if self.current_rank == 'A':
                    next_next_player.pile_belief.append('Q')
                else:
                    next_next_player.pile_belief.append('A')

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

                    # Find the player after the next player (the next next player)
                    copy = (self.current_player_index + 1) % len(self.players)
                    next_next_player = self.players[(copy+1)%len(self.players)]
                
                # After a bluff has been called, the pile is emptied
                self.pile = []
                
                # Reset the current rank because a new round starts
                self.current_rank = None 

        # Move on to the next player
        if ok == False:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
    
    # Handles the winning condition of the game
    def game_over(self):
        for player in self.players:
            if len(player.hand) == 0:
                return player
        return None

    # Handles how the game is played and saves the wins for each type of agent
    def play_game(self):
        global wins_distrusting, wins_hybrid, wins_trusting, prob_D, prob_T, wins_D, wins_H, wins_T
        self.deal()
        winner = self.game_over()
        while not winner:
            self.play_turn()
            winner = self.game_over()
        print(f"{winner} is the winner!")

        # Save the games won for each type of agent
        if winner.name == "Distrusting":
            wins_distrusting += 1

        if winner.name == "Trusting":
            wins_trusting += 1

        if winner.name == "Hybrid":
            wins_hybrid += 1

        
        if (wins_distrusting+wins_hybrid+wins_trusting) > 0:
            wins_D.append((wins_distrusting/(wins_distrusting+wins_hybrid+wins_trusting)) * 100)
            wins_T.append((wins_trusting/(wins_distrusting+wins_hybrid+wins_trusting)) * 100)
            wins_H.append((wins_hybrid/(wins_distrusting+wins_hybrid+wins_trusting)) * 100)

        # Calculate success rates
        success_rate_T = wins_trusting / (wins_distrusting + wins_trusting) if (wins_distrusting + wins_trusting) > 0 else 0
        success_rate_D = wins_distrusting / (wins_distrusting + wins_trusting) if (wins_distrusting + wins_trusting) > 0 else 0

        # Adjust probabilities based on success rates
        prob_T = success_rate_T
        prob_D = success_rate_D

# STRATEGY FUNCTIONS

# Play strategy for trusting agents
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
    
    #if the agent has the card, it plays it 
    for card in player.hand:
        if card.rank == game.current_rank:
            player.hand.remove(card)
            return card

    # If the player doesn't have a card of the current rank, lie
    card = random.choice(player.hand)
    player.hand.remove(card)
    print("The Trusting player played a" + card.rank + "but claimed it to be" + game.current_rank)
    return card

# Play strategy for distrusting agents
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
    print("The Distrusting player played a" + card.rank + "but claimed it to be" + game.current_rank)
    return card

# Call bluff strategy for trusting agents
def call_bluff_strategy_trusting(player, game):
     # Call bluff or lie if player does not have a card of the current rank
    if game.current_rank is not None and not any(card.rank == game.current_rank for card in player.hand):
        if player.pile_belief.count(game.current_rank) > 3:
            print("Trusting Agent says Cheat")
            return True
        else:
            return False
        
    return False  # Otherwise, do not call bluff

# Call bluff strategy for distrusting agents
def call_bluff_strategy_distrusting(player, game):
    # Call bluff or lie if player does not have a card of the current rank
    if game.current_rank is not None and not any(card.rank == game.current_rank for card in player.hand):
        if player.pile_belief.count(game.current_rank) > 3:
            print("Distrusting Agent says Cheat")
            return True
        
        if game.current_rank == 'A':
            # the player does not call cheat when it encounters a contradiction in its pile belief sistem (current state is removed)
            if player.pile_belief.count('Q') + len(player.hand) > 3:
                player.pile_belief[-1] = 'A'
                return False
            else: 
                print("Distrusting Agent says Cheat")
                return True
            
        if game.current_rank == 'Q':
            # the player does not call cheat when it encounters a contradiction in its pile belief sistem (current state is removed)
            if player.pile_belief.count('A') + len(player.hand) > 3:
                player.pile_belief[-1] = 'Q'
                return False
            else: 
                print("Distrusting Agent says Cheat")
                return True
        
    else: 
        if game.current_rank is not None and any(card.rank == game.current_rank for card in player.hand):
            cnt = 0
            for card in player.hand:
                if card.rank == game.current_rank:
                    cnt = cnt + 1
            
            if player.pile_belief.count(game.current_rank) + cnt> 3:
                print("Distrusting Agent says Cheat")
                return True
            
            if game.current_rank == 'A':
                # the player does not call cheat when it encounters a contradiction in its pile belief sistem (current state is removed)
                if player.pile_belief.count('Q') + len(player.hand) - cnt > 3:
                    return False
                else: 
                    print("Distrusting Agent says Cheat")
                    return True
            
            if game.current_rank == 'Q':
                # the player does not call cheat when it encounters a contradiction in its pile belief sistem (current state is removed)
                if player.pile_belief.count('A') + len(player.hand) - cnt > 3:
                    return False
                else: 
                    print("Distrusting Agent says Cheat")
                    return True

# Main
if __name__ == "__main__":

    n_T = []
    n_D = []
    n_H = []

    print("Menu:")
    print("1. Play a game of Cheat againts two AIs: Trusting and Distrusting")
    print("2. Play a game of Cheat againts two AIs: Trusting and Hybrid")
    print("3. Play a game of Cheat againts two AIs: Hybrid and Distrusting")
    print("4. Let the three agents play againts each other")

    # Choose between the options from the menu
    while True:
        choice = input("Enter your choice (1-4): ")
        if choice in ['1', '2', '3', '4']:
            option =  int(choice)
            break
        else:
            print("Invalid choice. Please try again.")
    

    # Option for one human player, one trusting agent and one distrusting agent
    if option == 1:
        player1 = Player('Player 1', play_strategy_trusting, call_bluff_strategy_trusting, is_human= True)
        player2 = Player('Trusting', play_strategy_trusting, call_bluff_strategy_trusting, is_human= False)
        player3 = Player('Distrusting', play_strategy_distrusting, call_bluff_strategy_distrusting, is_human= False)

        game = Game([player1, player2, player3])

        game.play_game()

    # Option for one human player, one trusting agent and one hybrid agent
    if option == 2:
        player1 = Player('Player 1', play_strategy_trusting, call_bluff_strategy_trusting, is_human= True)
        player2 = Player('Trusting', play_strategy_trusting, call_bluff_strategy_trusting, is_human= False)
        player3 = Player('Hybrid', play_strategy_distrusting, call_bluff_strategy_distrusting, is_human= False)

        game = Game([player1, player2, player3])

        game.play_game()

    # Option for one human player, one distrusting agent and one hybrid agent
    if option == 3:
        player1 = Player('Player 1', play_strategy_trusting, call_bluff_strategy_trusting, is_human= True)
        player2 = Player('Distrusting', play_strategy_trusting, call_bluff_strategy_trusting, is_human= False)
        player3 = Player('Hybrid', play_strategy_distrusting, call_bluff_strategy_distrusting, is_human= False)

        game = Game([player1, player2, player3])

        game.play_game()

    # Option for only agents playing for 5 runs of n number of games per run
    if option == 4: 
        n = input("Type the number of games to be played:").strip()
        n = int(n)
        copy = n

        while (copy > 0):
            player1 = Player('Hybrid', play_strategy_trusting, call_bluff_strategy_trusting, is_human= False)
            player2 = Player('Trusting', play_strategy_trusting, call_bluff_strategy_trusting, is_human= False)
            player3 = Player('Distrusting', play_strategy_distrusting, call_bluff_strategy_distrusting, is_human= False)

            game = Game([player1, player2, player3])
            game.play_game()

            copy = copy - 1

        rounds = list(range(1, n + 1))
        print(wins_trusting)
        print(wins_distrusting)
        print(wins_hybrid)

        # Plotting the lines
        plt.plot(rounds, wins_D, label='Distrusting')
        plt.plot(rounds, wins_T, label='Trusting')
        plt.plot(rounds, wins_H, label='Hybrid')

        # Adding labels and title
        plt.xlabel('Number of games')
        plt.ylabel('Per-strategy percentage of games won')
        plt.title('Averages of percentage wins in the game of cheat per strategy')

        # Adding legend
        plt.legend()

        # Displaying the plot
        plt.show()

        n_T.append(wins_trusting)
        n_D.append(wins_distrusting)
        n_H.append(wins_hybrid)

        prob_T = 0.5
        prob_D = 0.5

        wins_hybrid = 0
        wins_distrusting = 0
        wins_trusting = 0

        copy = n
        while (copy > 0):
            player1 = Player('Hybrid', play_strategy_trusting, call_bluff_strategy_trusting, is_human= False)
            player2 = Player('Trusting', play_strategy_trusting, call_bluff_strategy_trusting, is_human= False)
            player3 = Player('Distrusting', play_strategy_distrusting, call_bluff_strategy_distrusting, is_human= False)

            game = Game([player1, player2, player3])
            game.play_game()

            copy = copy - 1

        n_T.append(wins_trusting)
        n_D.append(wins_distrusting)
        n_H.append(wins_hybrid)

        prob_T = 0.5
        prob_D = 0.5

        wins_hybrid = 0
        wins_distrusting = 0
        wins_trusting = 0

        copy = n
        while (copy > 0):
            player1 = Player('Hybrid', play_strategy_trusting, call_bluff_strategy_trusting, is_human= False)
            player2 = Player('Trusting', play_strategy_trusting, call_bluff_strategy_trusting, is_human= False)
            player3 = Player('Distrusting', play_strategy_distrusting, call_bluff_strategy_distrusting, is_human= False)

            game = Game([player1, player2, player3])
            game.play_game()

            copy = copy - 1

        n_T.append(wins_trusting)
        n_D.append(wins_distrusting)
        n_H.append(wins_hybrid)

        prob_T = 0.5
        prob_D = 0.5

        wins_hybrid = 0
        wins_distrusting = 0
        wins_trusting = 0

        copy = n
        while (copy > 0):
            player1 = Player('Hybrid', play_strategy_trusting, call_bluff_strategy_trusting, is_human= False)
            player2 = Player('Trusting', play_strategy_trusting, call_bluff_strategy_trusting, is_human= False)
            player3 = Player('Distrusting', play_strategy_distrusting, call_bluff_strategy_distrusting, is_human= False)

            game = Game([player1, player2, player3])
            game.play_game()

            copy = copy - 1

        n_T.append(wins_trusting)
        n_D.append(wins_distrusting)
        n_H.append(wins_hybrid)

        prob_T = 0.5
        prob_D = 0.5

        wins_hybrid = 0
        wins_distrusting = 0
        wins_trusting = 0

        copy = n
        while (copy > 0):
            player1 = Player('Hybrid', play_strategy_trusting, call_bluff_strategy_trusting, is_human= False)
            player2 = Player('Trusting', play_strategy_trusting, call_bluff_strategy_trusting, is_human= False)
            player3 = Player('Distrusting', play_strategy_distrusting, call_bluff_strategy_distrusting, is_human= False)

            game = Game([player1, player2, player3])
            game.play_game()

            copy = copy - 1

        n_T.append(wins_trusting)
        n_D.append(wins_distrusting)
        n_H.append(wins_hybrid)

        data = [n_H, n_T, n_D]

        # Calculate the number of runs
        num_runs = len(data[0])

        strategies = ['Hybrid', 'Trusting', 'Distrusting']

        # Set the width of each bar
        bar_width = 0.3

        # Set the x-axis positions for each group of bars
        x = np.arange(num_runs)

        # Create a figure and axes
        fig, ax = plt.subplots()

        # Plot the bars for each strategy
        for i, strategy_wins in enumerate(data):
            ax.bar(x + i * bar_width, strategy_wins, width=bar_width, label=strategies[i])

        # Add labels and title
        ax.set_xlabel('Runs')
        ax.set_ylabel(f'Number of won games out of {n}')
        ax.set_title('The number of winnings for the three strategies')
        ax.set_xticks(x + bar_width)
        ax.set_xticklabels([f'Run {i+1}' for i in range(num_runs)])
        ax.legend()

        # Move the legend outside the bar plot
        ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1))

        # Adjust the layout to accommodate the legend
        plt.subplots_adjust(right=0.7)

        # Show the plot
        plt.show()

        # Print the final results based on each strategy
        print(data)
