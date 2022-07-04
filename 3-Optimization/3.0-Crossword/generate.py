from math import inf
import random
import sys
import itertools
import copy

from crossword import *


class CrosswordCreator:
    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont

        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        font = ImageFont.truetype("fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (
                                rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10,
                            ),
                            letters[i][j],
                            fill="black",
                            font=font,
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for x in self.crossword.variables:
            domain_x = self.domains[x].copy()
            for word in domain_x:
                if len(word) != x.length:
                    self.domains[x].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        if self.crossword.overlaps[x, y] is None:
            return False

        revision = False
        domain_x = self.domains[x].copy()
        i, j = self.crossword.overlaps[x, y]
        for word_x in domain_x:
            if all([word_x[i] != word_y[j] for word_y in self.domains[y]]):
                self.domains[x].remove(word_x)
                revision = True

        return revision

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = [
                (x, y)
                for x in self.crossword.variables
                for y in self.crossword.variables
                if x != y
            ]

        while arcs:
            x, y = arcs.pop(0)
            if self.revise(x, y):
                if not self.domains[x]:
                    return False
                arcs.extend([(z, x) for z in self.crossword.neighbors(x) if z != y])

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return all([x in assignment for x in self.crossword.variables])

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Check if words fit in the variables to which they are assigned
        # (note: not necessary, since we enforce node consistency in the
        # beginning)
        # for x in assignment:
        #     if x.length != len(assignment[x]):
        #         return False
        for x, y in itertools.combinations(assignment, 2):
            # Check for duplicate assignments
            if assignment[x] == assignment[y]:
                return False
            # Check for conflicting characters
            if self.crossword.overlaps[x, y]:
                i, j = self.crossword.overlaps[x, y]
                if assignment[x][i] != assignment[y][j]:
                    return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        def ruled_out(var_word):
            count = 0
            for nbhr in self.crossword.neighbors(var):
                if nbhr not in assignment:
                    for nbhr_word in self.domains[nbhr]:
                        # Rule out duplicates
                        if var_word == nbhr_word:
                            count += 1
                            continue
                        # Rule out words that conflict at overlaps
                        i, j = self.crossword.overlaps[var, nbhr]
                        if var_word[i] != nbhr_word[j]:
                            count += 1
            return count

        return sorted(self.domains[var], key=ruled_out)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Find all unassigned variables of minimal domain size
        min_domain = inf
        for x in self.crossword.variables:
            if x not in assignment:
                test_domain = len(self.domains[x])
                if test_domain < min_domain:
                    sorted_domain = [x]
                    min_domain = test_domain
                elif test_domain == min_domain:
                    sorted_domain.append(x)

        # Find all variables of maximal degree among the above
        max_degree = -inf
        for x in sorted_domain:
            test_degree = len(self.crossword.neighbors(x))
            if test_degree > max_degree:
                sorted_degree = [x]
                max_degree = test_degree
            elif test_degree == max_degree:
                sorted_degree.append(x)

        # Return a variable randomly selected among the above
        return random.choice(sorted_degree)

    def inferences(self, var, word):
        """
        Updates the variable domains assuming a new var: word assignment, i.e.
        removes word from the domains of other variables and uses AC-3 to enforce
        arc consistency in all arcs (x, y) for which the domain of y has changed.
        Returns all new inferences that can be made after these changes, or None if
        some domain is left empty.
        """
        # Set {word} as the domain of var
        self.domains[var] = set([word])

        # Remove word from the domain of other variables
        changed_vars = []
        for x in self.crossword.variables:
            if x != var and word in self.domains[x]:
                self.domains[x].remove(word)
                if not self.domains[x]:
                    return False
                changed_vars.append(x)

        # Apply AC-3 on the arcs containing variables whose domain changed
        arcs = [(nbhr, var) for nbhr in self.crossword.neighbors(var)]
        for x in changed_vars:
            arcs.extend([(nbhr, x) for nbhr in self.crossword.neighbors(x)])
        if not self.ac3(arcs):
            return None

        # Find all new inferences
        inferences = {}
        for x in self.domains:
            if x != var and len(self.domains[x]) == 1:
                inferences[x] = list(self.domains[x])[0]
        return inferences

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # Check if assignment is consistent
        if not self.consistent(assignment):
            return None

        # Check if assignment is complete
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for word in self.order_domain_values(var, assignment):
            # Add var: word to assignment
            assignment[var] = word
            # Make a copy of current domains to restore in case of failure
            current_domains = copy.deepcopy(self.domains)
            # Update the variable domains and find all new inferences
            inferences = self.inferences(var, word)
            if inferences is not None:
                # Add inferences to assignment
                assignment.update(inferences)
                # Apply backtrack to the new assignment
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                # If backtrack fails, remove inferences from assignment
                assignment = {
                    x: assignment[x] for x in assignment if x not in inferences
                }
            # If inferences or backtrack fail, restore the domains and
            # remove var: word from assignment
            self.domains = current_domains
            assignment.pop(var)

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
