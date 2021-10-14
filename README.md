# pandeliskirpoglou-algo-assignments

## First assignment - Crossword solution

The first assignment is dedicated in solving a crossword of regular expressions. In order to execute the algorithm
clone the repository, head in the folder with the re_crossword.py file and execute this command in your command window.
The following runs on Python v3.

```
python re_crossword.py crossword_file regex_file
```

* crossword_file: csv file that contains the crossword
* regex_file    : txt file that contains the regular expressions

For details use -h after re_crossword.py
You can also find examples of the crossword_file and regex_file in the folder assignment-2021-1


## Second assignment - Points cover

The second assignment is dedicated on the hitting objects problem. In this problem we are trying to hit a set of
points with the least ammount of lines with various solving ways. The two ways to solve the problem are the set covering 
method and the greedy method. You can also choose if you want those lines to be parallel with the axes. The set of points 
is given with a file in txt form as following:

```
1 1
2 2
3 3
4 4
5 5
6 6
7 1
7 2
8 3
8 4
9 5
9 6
10 1
10 2
10 3
11 4
11 5
11 6
```

In order to execute the algorithm you need to clone the repository, head in the folder with the points_cover.py file,
execute this command in your favorite command promt. The following runs on Python v3.

```
python points_cover.py [-f] [-g] points_file.txt
```

* [-f]: using -f will process the problem with the set covering method (otherwise greedy method)
* [-g]: using -g will give a solution filled only with parallel to the axes lines (otherwise all type of lines)

For details use -h after points_cover.py
You can also find examples of points file in the folder assignment-2021-2

## Third assignment - Beckett Gray (Unfinished)

The third assignment focuses on finding possible beckett gray codes with different filters. By finding 
all gray codes and then creating a hypercube with them we are able to see different patterns of possible solutions
in a famous problem called the Beckett problem.