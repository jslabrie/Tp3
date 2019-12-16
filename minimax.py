'''Contient l'algorithme minimax pour jouer au Quoridor'''

from graphe import construire_graphe
from copy import deepcopy
import networkx as nx
import quoridor

POIDS_1 = 10
POIDS_2 = 0
POIDS_3 = 0
NODES_ANALYSED = 0


class Node(object):   
    def __init__(self, depth, maximizingPlayer, state, value=0):
        self.depth = depth
        # print(depth, end='-')
        self.maximizingPlayer = maximizingPlayer
        self.state = state
        self.value = value
        self.graphe = construire_graphe(
            [player['pos'] for player in self.state['joueurs']],
            self.state['murs']['horizontaux'],
            self.state['murs']['verticaux']
        )


    def create_children(self):
        if self.depth > 0:
            walls = self.available_wall_positions()
            for pos in walls["horizontaux"]:
                new_state = self.new_game_state(pos, 'MH')
                if new_state is not None:
                    value = self.calcValue(new_state)
                    #if value != 0:
                    yield Node(
                        self.depth - 1,
                        not (self.maximizingPlayer),
                        new_state,
                        value
                    )

            for pos in walls["verticaux"]:
                new_state = self.new_game_state(pos, 'MV')
                if new_state is not None:
                    value = self.calcValue(new_state)
                    #if value != 0:
                    yield Node(
                        self.depth - 1,
                        not (self.maximizingPlayer),
                        new_state,
                        value
                    )
            li = self.movements()
            for pos in li:
                new_state_pos = self.new_game_state(pos, 'D')
                if new_state_pos is not None:
                    value = self.calcValue(new_state_pos)
                    yield Node(
                        self.depth - 1,
                        not (self.maximizingPlayer),
                        new_state_pos,
                        value
                    )

    def new_game_state(self, position, operation):
        '''
        Retourne un nouvel état de jeu après le changement passé en argument, None si le nouvel
        état est invalide.
        '''
        new_state = deepcopy(self.state)
        if operation == 'MH':
            new_state['murs']['horizontaux'].append(position)
        elif operation == 'MV':
            new_state['murs']['verticaux'].append(position)
        else:
            if self.maximizingPlayer:
                new_state['joueurs'][0]['pos'] = position
            else:
                new_state['joueurs'][1]['pos'] = position

        if operation != 'D':
            graphe = construire_graphe(
                [player['pos'] for player in new_state['joueurs']],
                new_state['murs']['horizontaux'],
                new_state['murs']['verticaux']
            )
            if not self.blocks_player(graphe):
                return new_state
        else:
            return new_state

    def calcValue(self, state):
        """Calcule la valeur du noeud selon le delta des positions

        Arguments:
            state {object} -- Nouvel état de l'enfant du noeud
            move_type {str} -- Type de coup ('MH', 'MV', ou 'D')

        Keyword Arguments:
            position {tup} -- Position du placement si le coup est un déplacement (default: {None})      

        Returns:
            float -- La valeur du noeud
        """
        graphe = construire_graphe(
            [player['pos'] for player in state['joueurs']],
            state['murs']['horizontaux'],
            state['murs']['verticaux']
        )

        pos_1 = state["joueurs"][0]["pos"]
        pos_2 = state["joueurs"][1]["pos"]

        shortest_B = nx.shortest_path(graphe, pos_2, 'B2')
        shortest_A = nx.shortest_path(graphe, pos_1, 'B1')

        # Partie gagnée
        if pos_1[1] == 9:
            win = 1000
        elif pos_2[1] == 1:
            win = -1000
        else:
            win = 0

        # Critère 1: Delta des distances
        delta = len(shortest_B) - len(shortest_A)
        
        # Critère 2: Distance du max de la prochaine rangée
        current_row = shortest_A[0][1]
        dist_a = 1
        for i in range(len(shortest_A) - 1):
            if shortest_A[i][1] > current_row:
                dist_a = i
                break
        evaluation_a = 1 / dist_a
        

        # Critère 3: Distance du min de la prochaine rangée
        current_row = shortest_B[0][1]
        dist_b = 1
        for i in range(len(shortest_B) - 1):
            if shortest_B[i][1] < current_row:
                dist_b = i
                break
        evaluation_b = -1 / dist_b

        return  win + (delta * POIDS_1) + (POIDS_2 * evaluation_a) + (POIDS_3 * evaluation_b)

    def available_wall_positions(self):
        '''
        Retourne un dictionnaire contenant un liste de positions de murs disponibles
        pour chaque orientation
        '''
        horizontal_positions = [(x, y) for x in range(1, 9)  # 9
                                for y in range(2, 10)]  # 10
        vertical_positions = [(x, y) for x in range(2, 10)  # 10
                              for y in range(1, 9)]  # 9
        
        if self.maximizingPlayer:
            player = 0
            target = 'B1'
        else:
            player = 1
            target = 'B2'

        if self.state['joueurs'][player]['murs'] == 0:
            horizontal_positions = []
            vertical_positions = []
        else:
            
            positions_path = nx.shortest_path(
                self.graphe, self.state['joueurs'][player]['pos'], target)[:-1]

            print(positions_path)
            # Horizontaux invalides

            for position in self.state["murs"]["horizontaux"]:
                pos_list = [
                    position,
                    (position[0] - 1, position[1]),
                    (position[0] + 1, position[1])
                ]
                position_ver = (position[0] + 1, position[1] - 1)
                for pos in pos_list:
                    try:
                        horizontal_positions.remove(pos)
                    except ValueError:
                        pass
                try:
                    vertical_positions.remove(position_ver)
                except ValueError:
                    pass
            
            for position in horizontal_positions:

                useless = True
                for pos in positions_path:
                    if abs(position[0] - pos[0]) <= 1 or abs(position[1] - pos[1]) <= 1:
                        useless = False

                if useless:
                    try:
                        horizontal_positions.remove(position)
                    except ValueError:
                        pass

            # Verticaux invalides
            for position in self.state["murs"]["verticaux"]:
                pos_list = [
                    position,
                    (position[0], position[1] - 1),
                    (position[0], position[1] + 1)
                ]
                position_hor = (position[0] - 1, position[1] + 1)
                for pos in pos_list:
                    try:
                        vertical_positions.remove(pos)
                    except ValueError:
                        pass
                try:
                    horizontal_positions.remove(position_hor)
                except ValueError:
                    pass

            for position in vertical_positions:
                useless = True
                for pos in positions_path:
                    if abs(position[0] - pos[0]) <= 1 or abs(position[1] - pos[1]) <= 1:
                        useless = False

                if useless:
                    try:
                        vertical_positions.remove(position)
                    except ValueError:
                        pass

            

        return {"horizontaux": horizontal_positions, "verticaux": vertical_positions}

    def movements(self):
        '''Revoie une liste des déplacements que le joueur peut effectuer'''

        if self.maximizingPlayer:
            item = nx.shortest_path(self.graphe,
                self.state["joueurs"][0]["pos"],
                'B1'
            )[1]
        else:
            item = nx.shortest_path(self.graphe,
                self.state["joueurs"][1]["pos"],
                'B2'
            )[1]
        return [item]

    def blocks_player(self, graphe):
        '''Retourne True si le placement de mur pour l'état bloque un joueur'''

        is_invalid = False
        if not nx.has_path(graphe, self.state["joueurs"][0]["pos"], 'B1'):
            is_invalid = True
        if not nx.has_path(graphe, self.state["joueurs"][1]["pos"], 'B2'):
            is_invalid = True

        return is_invalid


def minimax(node, depth, alpha, beta, maximizingPlayer):
    global NODES_ANALYSED
    if depth == 0 or abs(node.value) >= 1000:
        NODES_ANALYSED += 1
        return node.value, node.state

    if maximizingPlayer:
        maxEval = float("-inf")
        for child in node.create_children():
            val, _ = minimax(child, depth - 1, alpha, beta, False)
            state = child.state
            if maxEval < val:
                maxEval = val
                maxState = state
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return maxEval, maxState

    else:
        minEval = float("+inf")
        for child in node.create_children():
            val, _ = minimax(child, depth - 1, alpha, beta, True)
            state = child.state
            if minEval > val:
                minEval = val
                minState = state
            beta = min(beta, val)
            if beta <= alpha:
                break
        return minEval, minState


def calc_best_move(currentState, player):
    global NODES_ANALYSED
    depth = 1
    if player == 1:
        maximizingPlayer = True
    else:
        maximizingPlayer = False

    for i in range(2):
        currentState['joueurs'][i]['pos'] = tuple(currentState['joueurs'][i]['pos'])

    for i in range(len(currentState['murs']['horizontaux'])):
        currentState['murs']['horizontaux'][i] = tuple(currentState['murs']['horizontaux'][i])
    for i in range(len(currentState['murs']['verticaux'])):
        currentState['murs']['verticaux'][i] = tuple(currentState['murs']['verticaux'][i])

    NODES_ANALYSED = 0
    node = Node(depth, maximizingPlayer, currentState)
    val, new_state = minimax(node, depth, float("-inf"),
                             float("+inf"), maximizingPlayer)
    print(f'Nodes analysed: {NODES_ANALYSED}')

    # Décoder le changement
    # Si déplacement
    for i in range(2):
        if currentState["joueurs"][i]["pos"] != new_state["joueurs"][i]["pos"]:
            move = (new_state["joueurs"][i]["pos"],  'D', new_state)

    # Si MH
    if len(currentState["murs"]["horizontaux"]) != 0:
        if currentState["murs"]["horizontaux"][-1] != new_state["murs"]["horizontaux"][-1]:
            move = (new_state["murs"]["horizontaux"][-1], 'MH', new_state)
    else:
        if len(new_state["murs"]["horizontaux"]) != 0:
            move = (new_state["murs"]["horizontaux"][0], 'MH', new_state)

    # Si MV
    if len(currentState["murs"]["verticaux"]) != 0:
        if currentState["murs"]["verticaux"][-1] != new_state["murs"]["verticaux"][-1]:
            move = (new_state["murs"]["verticaux"][-1], 'MV', new_state)
    else:
        if len(new_state["murs"]["verticaux"]) != 0:
            move = (new_state["murs"]["verticaux"][0], 'MV', new_state)

    return move
