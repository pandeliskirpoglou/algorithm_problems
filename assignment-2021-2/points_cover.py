import argparse
import sys
import itertools
import pprint


def read_points(filename):
    """
    The read_points method reads opens the file with the points and returns them in a 
    list filled with lists of couples with coordinates.

    input:   -filename: string name of the file with the points
    output:  -points: list with couples of coordinates [[X1,Y1],...,[Xn,Yn]]
    """
    points = []
    with open(filename) as points_file:
        for line in points_file:
            content = line.split(" ")
            point = [int(content[0]), int(content[1].rstrip())]
            points.append(point)
    return points


parser = argparse.ArgumentParser()
parser.add_argument(
    "points_file", help="Name of the file which contains the crossword")
parser.add_argument("-f", "--setCovering", action="store_true",
                    help="Use -f if you want to utilise the set covering method")
parser.add_argument("-g", "--parallel", action="store_true",
                    help="Use -g if you want the lines to be parallel with the x & y axis")

args = parser.parse_args()

# Saving names in variables so args.filename is not executed many times in case needed
points_file = args.points_file
set_covering = args.setCovering
parallel = args.parallel

points = read_points(points_file)

# Global list with all the possible lines
S = []


def line_exists(point1, point2):
    """
    The line_exists method checks if two points are already being used in a line,
    in the set S. If those two points exist in a line, this means that a line with 
    those points already appears in S. This happens because two points can adress one
    and only one line. 

    input:   -point1: list with the coordinates of point1
             -point2: list with the coordinates of point2
    output:  -exists: boolean True --> line exists | False --> line does not exists

    """
    exists = False
    for line in S:
        count = 0
        for point in line:
            if point == point1 or point == point2:
                count += 1
        if count == 2:
            exists = True
            break
    return exists


def find_S():
    """
    The find_S method calculates all the possible lines that can pass through all
    the given points. It is used for the set covering method and it inputs all these
    lines in a global list called S.

    In order to check for all possible lines find_s:
    1. takes two different points
    2. adds them in a line (finding the line with a (slope), b(intercept), or x = b)
    3. checks if other points match the line
    4. adds the possible lines on the S list
    """
    for point1 in points:
        second_starting_point = points.index(point1) + 1
        for point2_index in range(second_starting_point, len(points)):
            point2 = points[point2_index]

            if not line_exists(point1, point2):
                line = [point1, point2]
                third_starting_point = point2_index + 1

                if point1 != point2:
                    """
                    The following lines check wether a can be calculate and it does not
                    involve division with zero. If x1 and x2 match that means that the
                    line follows the x = x1 = x2 pattern
                    """
                    if point1[0] != point2[0]:

                        a = (point2[1] - point1[1])/(point2[0] - point1[0])
                        b = point1[1] - a * point1[0]

                        for point3_index in range(third_starting_point, len(points)):

                            point3 = points[point3_index]
                            fits = point3[1] == a*point3[0] + b
                            if point3 != point1 and point3 != point2 and fits:

                                line.append(point3)

                        S.append(line)

                    else:

                        x = point1[0]

                        for point3_index in range(third_starting_point, len(points)):

                            point3 = points[point3_index]
                            fits = point3[0] == x
                            if point3 != point1 and point3 != point2 and fits:
                                line.append(points[point3_index])

                        S.append(line)


def find_parallel_S():
    """
    The find_parallel_S function retrieves all the lines that cover the points. If a point (X, Y)
    not have a match to define a line, then the point (X+1, Y) is used as its match. The method simply
    checks for each point if it has a match with same x or y coordinates and adds them to the listx or listy
    accordingly.
    """
    for point1 in points:

        x = point1[0]
        y = point1[1]

        listx = [point1]
        listy = [point1]

        for point2 in points:
            if point1 != point2:

                if point2[0] == x:
                    listx.append(point2)
                elif point2[1] == y:
                    listy.append(point2)

        if len(listx) != 1:
            S.append(listx)
        if len(listy) != 1:
            S.append(listy)
        if len(listx) == 1 and len(listy) == 1:
            S.append([point1, [point1[0] + 1, point1[1]]])


def set_covering_method(is_parallel):
    """
    The set_covering function calculates the solution for the set covering method
    for all types of lines. It uses an algorithm with the following steps:

    Until no solution is found
    1. Find all possible subsets of S for every possible number of lines
    2. For every possible subset check if:
        a. solution covers number of points (makes less loops)
        b. solution covers all points
    3. If solution is found end the process

    input:   -is_parallel: boolean True --> S contains parallel points | False --> otherwise 
    output:  -solution: list with the solution of the problem
    """
    found = False
    i = 1
    while not found:

        solution = []
        all_solutions = itertools.combinations(S, i)

        for possible_solution in all_solutions:
            used = [False] * len(points)
            sum_of_points = 0
            """
            If the sum of points is les than 18 this means the solution is not found
            for sure, so move on (break).
            """
            for lines in possible_solution:
                sum_of_points += len(lines)

            if sum_of_points >= len(points):
                for line in possible_solution:
                    for point in line:
                        if point in points:
                            used[points.index(point)] = True

                if used.count(True) == len(used):
                    solution = possible_solution
                    found = True

            else:
                if not is_parallel:
                    break

        i += 1

    return solution


def greedy_method():
    """
    The greedy_method function implements the greedy algorithm. In more depth,
    the algorithm finds every time the line that covers the most uncovered points
    and adds it to the solution. This loop ends when all the points are covered.

    output:  -solution: list with the solution of the greedy algorithm
    """
    used = [False] * len(points)
    solution = [S[0]]
    for point in S[0]:
        used[points.index(point)] = True

    while used.count(True) != len(used):
        max_covered = 0
        i = 0
        max_index = -1
        for line in S:
            covered = 0
            for point in line:
                if point in points:
                    if not used[points.index(point)]:
                        covered += 1

            if covered > max_covered:
                max_covered = covered
                max_index = i

            i += 1

        solution.append(S[max_index])
        for point in S[max_index]:
            if point in points:
                used[points.index(point)] = True

    return solution


def final_sort(unsorted_list):
    """
    The final_sort method sorts the solution appropriately just for the case
    of -g. In order to sort first by reverse length and then by the first element
    we input the unsorted solution (unsorted list) and for every group of lines
    with the same list, we sort them and then append them to the sorted list.

    input:   -unsorted_lsit: list with the unsorted solution
    output:  -sorted_list: list with the sorted solution
    """
    line_length = len(unsorted_list)
    lines_by_length = []
    sorted_list = []

    while line_length > 0:

        for line in unsorted_list:
            if len(line) == line_length:
                lines_by_length.append(
                    sorted(line, key=lambda solution: solution[1]))

        line_length -= 1

        if lines_by_length:
            lines_by_length = sorted(lines_by_length)

            for line in lines_by_length:
                sorted_list.append(line)

            lines_by_length.clear()
    return sorted_list


solution = []

if set_covering:
    if parallel:
        #
        # Set covering with parallel lines solution
        #

        find_parallel_S()

        S = sorted(S, key=len)
        S.reverse()

        i = 0
        for line in S:
            S[i] = sorted(S[i])
            i += 1

        unique_S = []

        for line in S:
            if not line in unique_S:
                unique_S.append(line)

        S = unique_S
        solution = set_covering_method(parallel)

        solution = final_sort(solution)

    else:
        #
        # Set covering withOUT parallel lines solution
        #

        find_S()

        # sort S from largest covering lines to smaller for faster results
        S = sorted(S, key=len)
        S.reverse()
        solution = set_covering_method(parallel)

        solution = sorted(solution, key=len)
        solution.reverse()
else:
    if parallel:
        #
        # greedy with parallel lines solution
        #

        find_parallel_S()

        S = sorted(S, key=len)
        S.reverse()

        i = 0
        for line in S:
            S[i] = sorted(S[i])
            i += 1

        unique_S = []

        for line in S:
            if not line in unique_S:
                unique_S.append(line)

        S = unique_S

        solution = greedy_method()

        solution = final_sort(solution)
    else:
        #
        # greedy withOUT parallel lines solution
        #

        find_S()

        # sort S from largest covering lines to smaller for faster results
        S = sorted(S, key=len)
        S.reverse()

        solution = greedy_method()

        solution = sorted(solution, key=len)
        solution.reverse()


print()
for line in solution:
    for point in line:
        print('(' + str(point[0]) + ',', str(point[1]) + ')', end=' ')
    print()
