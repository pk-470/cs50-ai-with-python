# [Week 0 - Search](https://cs50.harvard.edu/ai/2020/weeks/0/)

## Module description

This module introduces a number of classic search algorithms aiming to find a path from some initial state to a goal state. The algorithms covered are:

- Depth-first search;
- Breadth-first search;
- Greedy best-first search;
- A\* search.

It also introduces the concept of adversarial search, in which the algorithm faces an opponent which tries to achieve the opposite goal. The algorithms covered in this section include:

- MiniMax;
- Alpha-beta pruning;
- Depth-limited minimax.

## Projects

The module includes two project assignments:

### [Project 0.0: Degrees](https://cs50.harvard.edu/ai/2020/projects/0/degrees/)

The goal of this project is to write a program that uses breadth-first search to determine how many "degrees of separation" apart two actors are, based on the [Six Degrees of Kevin Bacon](https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon) game.

### [Project 0.1: Tic-Tac-Toe](https://cs50.harvard.edu/ai/2020/projects/0/tictactoe/)

The aim of this project is to implement the minimax algorithm in order to create an AI that plays Tic-Tac-Toe optimally.

### Note on the directory contents

Along with my solutions to the above projects (which deviate quite a lot from the solution templates provided in the module), included in this directory are also my own implementations of the 4 classic search algorithms (BFS, DFS, GBFS, A\*) introduced in the lecture, generalised so that they can be applied to any object of the Search_Problem class as defined in the classes.py file (see the Algorithms subdirectory). Note that my code is partly based on the source code of the lecture. Moreover, I have modified the code of the maze solver which was given in the lecture as an example so that it integrates with my own implementations.

**For VSCode users**: To avoid IntelliSense not working for the search algorithm modules imported from the _Algorithms_ directory into the _maze.py_ and _degrees.py_ files using sys.path.append, create a folder named _.vscode_ in the target directories (i.e. _Maze_ and _0.0-Degrees_ respectively) and add a settings.json file in it containing the following lines:

> {
>
> "python.analysis.extraPaths": ["../Algorithms"]
>
> }
