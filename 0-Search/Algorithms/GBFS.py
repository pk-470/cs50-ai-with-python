# An implementation of the Greedy Best-First Search (GBFS) algorithm for solving search problems.

from classes import *


def GBFS(
    problem: Search_Problem,
    heuristic,
    show_solution=False,
    show_explored=False,
    show_moves=False,
):
    starting_node = Node(problem.starting_state, None, None)

    # Check if the starting node is already the goal, otherwise initialise
    # the frontier containing the starting node.
    if starting_node.state == problem.goal_state:
        if show_solution or show_explored or show_moves:
            print("We are already at the goal state. There is nothing to be done.")
        return None, None
    gbfs_frontier = Informed_Frontier([starting_node])

    # Initialise the explored nodes set.
    explored = Explored_Nodes()

    # Define the function that chooses the node of minimum distance from the goal.
    def choice(nodes):
        node = nodes[0]
        for n in nodes[1:]:
            if heuristic(n) < heuristic(node):
                node = n

        return node

    while True:
        # If the frontier is empty, print that there are no solutions and stop.
        if gbfs_frontier.is_empty():
            if show_solution or show_moves:
                print("There are no solutions to the problem.")
            if show_explored:
                explr_states = [explr.state for explr in explored.nodes]
                print(
                    "\n"
                    "While trying to find a solution, the algorithm"
                    "explored the following states:"
                    "\n"
                )
                print(explr_states)
                print("\n")
            return None, explored

        # Otherwise, remove the node determinded to be closest to the goal according
        # to the chosen heuristic, and add it to the explored nodes set.
        current_node = gbfs_frontier.remove_node(choice)
        explored.add_node(current_node)

        # Expand the node (i.e. find all new nodes that can be reached from this node).
        future_nodes = current_node.expand(problem.moves(current_node.state))

        # Check each new node if it is the goal. If so, return the solution.
        # Otherwise, add it to the frontier (as long as it is not already
        # in the frontier or the explored nodes set).
        for node in future_nodes:
            if node.state == problem.goal_state:
                steps = [node]
                while node.parent_node is not None:
                    node = node.parent_node
                    steps.append(node)
                sol_steps = steps[::-1]
                explored.add_node(current_node)
                if show_solution:
                    print("A solution has been found:\n")
                    sol_states = [step.state for step in sol_steps]
                    print(sol_states)
                    print("\n")
                if show_explored:
                    print(
                        "To find this solution, the algorithm explored the following states:\n"
                    )
                    explr_states = [explr.state for explr in explored.nodes]
                    print(explr_states)
                    print("\n")
                if show_moves:
                    print("The solution is obtained through the following moves:\n")
                    moves = [
                        step.trans_move.move_id
                        for step in sol_steps
                        if step.trans_move is not None
                    ]
                    print(moves)
                    print("\n")
                return sol_steps, explored
            elif not gbfs_frontier.contains_state(
                node.state
            ) and not explored.contains_state(node.state):
                gbfs_frontier.add_node(node)
