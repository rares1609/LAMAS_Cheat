import networkx as nx
import matplotlib.pyplot as plt

# Example of a Kripke model where we have 3 players, 3 ranks, each player having a card of each rank, in total 3 cards.
class KripkeModel:
    def __init__(self):
        self.states = {
            "S1": {"P1": "A", "P2": "K", "P3": "Q"},
            "S2": {"P1": "A", "P2": "Q", "P3": "K"},
            "S3": {"P1": "K", "P2": "A", "P3": "Q"},
            "S4": {"P1": "K", "P2": "Q", "P3": "A"},
            "S5": {"P1": "Q", "P2": "A", "P3": "K"},
            "S6": {"P1": "Q", "P2": "K", "P3": "A"}
        }

        self.relations = {
            "R1": [("S1", "S2"), ("S3", "S4"), ("S5", "S6")],  # P1
            "R2": [("S1", "S6"), ("S2", "S4"), ("S3", "S5")],  # P2
            "R3": [("S1", "S3"), ("S2", "S5"), ("S4", "S6")]   # P3
        }

    # Check if a state is accessible from anoter state
    def is_accessible(self, from_state, to_state, player):
        # P1 uses R1, P2 uses R2, and P3 uses R3
        relation = "R" + player[1]
        return (from_state, to_state) in self.relations[relation]

    # Get a specific state
    def get_state(self, state):
        return self.states[state]
    
    # Print model
    def print_model(self):
        print("States:")
        for state, cards in self.states.items():
            print(state, cards)
        print("Relations:")
        for relation, state_pairs in self.relations.items():
            print(relation, state_pairs)
    
    # Draw model
    def draw_graph(self):
        G = nx.DiGraph()
        for state in self.states:
            G.add_node(state)
        for relation in self.relations.values():
            G.add_edges_from(relation)

        # Changed the positions of the nodes to look more readable
        pos = {
            'S1': [0, 0], 
            'S2': [0, 2], 
            'S3': [-1, 1], 
            'S4': [1, 1], 
            'S5': [-2, 2], 
            'S6': [2, 2]
        }

        # Create labels for each node
        labels = {node: f"{node}: {values}" for node, values in self.states.items()}

        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='green')
        nx.draw_networkx_labels(G, pos, font_size=12)
        
        # Draw labels with adjusted position and size
        label_pos = {node: [coordinates[0], coordinates[1] - 0.15] for node, coordinates in pos.items()}
        nx.draw_networkx_labels(G, label_pos, labels=labels, font_size=4)
        
        nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=10)
        plt.savefig('kripke_model.png', dpi=300)  # Save as a png file with a DPI of 300.
        plt.show()


# Testing the model
kripke_model = KripkeModel()
kripke_model.draw_graph()
kripke_model.print_model()
