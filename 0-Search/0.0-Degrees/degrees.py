import sys

sys.path.append("../Algorithms")

from classes import *
from BFS import *
from get_data import *

import random as rd


def degrees():
    movies, people, stars = load_data("large")
    name_1 = input("Actor 1 name: ")
    name_1_id = actor_id(people, name_1)
    if name_1_id is None:
        return
    name_2 = input("Actor 2 name: ")
    name_2_id = actor_id(people, name_2)
    if name_2_id is None:
        return

    if name_1 == name_2:
        movie_id = rd.choice(movies_of_actor(stars, name_1_id))
        movie = movie_title_and_year(movies, movie_id)
        print("0 degrees of separation.")
        print(f"0: {name_1} starred in {movie[0]} in {movie[1]}.")
        return

    def moves(name_id):
        movie_ids = movies_of_actor(stars, name_id)
        moves_list = []

        for movie_id in movie_ids:
            moves_list.append(
                Move(
                    action=lambda _, movie_id=movie_id: actors_in_movie(
                        stars, movie_id
                    ),
                    move_id=movie_id,
                )
            )

        return moves_list

    degrees_problem = Search_Problem(
        starting_state=name_1_id, goal_state=name_2_id, moves=moves
    )

    solution = BFS(degrees_problem)[0]

    if solution is None:
        print("I can't find a link between the two actors.")
        return

    deg = len(solution) - 1
    if deg == 1:
        print("1 degree of separation.")
    else:
        print(f"{deg} degrees of separation.")

    i = 1
    for step in solution[1:]:
        movie = movie_title_and_year(movies, step.trans_move.move_id)
        print(
            str(i)
            + ": "
            + actor_name(people, step.parent_node.state)
            + " and "
            + actor_name(people, step.state)
            + " starred in "
            + movie[0]
            + " in "
            + str(movie[1])
            + "."
        )
        i = i + 1


if __name__ == "__main__":
    degrees()
