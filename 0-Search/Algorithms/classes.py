class Node:
    def __init__(self, state, parent_node, trans_move, path_cost=0):
        self.state = state
        self.parent_node = parent_node
        self.trans_move = trans_move
        self.path_cost = path_cost

    def apply_move(self, move):
        states = move.action(self.state)
        nodes = []
        for state in states:
            nodes.append(
                Node(
                    state=state,
                    parent_node=self,
                    trans_move=move,
                    path_cost=self.path_cost + move.weight,
                )
            )

        return nodes

    def expand(self, moves):
        expansion = []
        for move in moves:
            expansion.extend(self.apply_move(move))

        return expansion


class Stack_Frontier:
    def __init__(self, nodes):
        self.nodes = nodes

    def is_empty(self):
        return not bool(self.nodes)

    def contains_state(self, state):
        return any([state == node.state for node in self.nodes])

    def add_node(self, node):
        self.nodes.append(node)

    def remove_node(self):
        if not self.nodes:
            raise Exception("The frontier is empty.")
        node = self.nodes.pop(-1)
        return node


class Queue_Frontier(Stack_Frontier):
    def remove_node(self):
        if not self.nodes:
            raise Exception("The frontier is empty.")
        node = self.nodes.pop(0)
        return node


class Informed_Frontier(Stack_Frontier):
    def remove_node(self, choice):
        if not self.nodes:
            raise Exception("The frontier is empty.")
        node = choice(self.nodes)
        self.nodes.remove(node)
        return node


class Explored_Nodes:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def contains_state(self, state):
        return any([state == node.state for node in self.nodes])


class Move:
    def __init__(self, action, move_id=None, weight=1):
        self.action = action
        self.move_id = move_id
        self.weight = weight


class Search_Problem:
    def __init__(self, starting_state, goal_state, moves):
        self.starting_state = starting_state
        self.goal_state = goal_state
        self.moves = moves
