import argparse
import sre_yield
import csv
import sys
import string
# import time

parser = argparse.ArgumentParser()
parser.add_argument(
    "crossword_file", help="Name of the file which contains the crossword")
parser.add_argument(
    "regex_file", help="Name of the file which contains the regular expressions")

args = parser.parse_args()

# Saving names in variables so args.filename is not executed many times in case needed
crossword_file = args.crossword_file
regex_file = args.regex_file


def read_crossword(crossword_file):
    """
    The read_crossword method takes as input the file name of the 
    crossword and returns the crossword and the max and min length 
    of a word in it.

    input:   -crossword_file: string name of the csv crossword file
    output:  -crossword: dictionary {word_id:list}
             -max_word_length: int with the max word length
             -min_word_length: int with the min word length
    """
    crossword = {}
    max_word_length = 0
    min_word_length = sys.maxsize
    with open(crossword_file, newline='') as crossword:
        reader = csv.reader(crossword, delimiter=',')
        crossword = {row[0]: row[1:] for row in reader}

    for value in crossword.values():
        if len(value[0]) > max_word_length:
            max_word_length = len(value[0])
        if len(value[0]) < min_word_length:
            min_word_length = len(value[0])

    return crossword, max_word_length, min_word_length


def read_regular_expressions(regex_file, max_word_length, min_word_length):
    """
    The read_regular_expressions method reads the txt file with the regular expressions
    and returns the possible words that they create in a dictionary. The max and min word
    lengths are used to limit those possibilities.

    input:   -regex_file: string name of the txt file with the regular expressions
             -max_word_length: int with the max word length in the crossword
             -min_word_length: int with the min word length in the crossword
    output:  -regex_words: dictionary {regex:list_of_possible_words}
    """
    regex_words = {}
    with open(regex_file) as regex:
        for line in regex:
            all_regex_words = list(
                sre_yield.AllStrings(line.rstrip(), max_count=5, charset=string.ascii_uppercase))
            # Getting unique words that fit the largest crossword word
            unique_fitting_words = []
            for item in all_regex_words:
                if item not in unique_fitting_words and len(item) <= max_word_length and len(item) >= min_word_length:
                    unique_fitting_words.append(item)
            regex_words[line.rstrip()] = unique_fitting_words

    return regex_words


crossword, max_word_length, min_word_length = read_crossword(
    crossword_file)
regex_words = read_regular_expressions(
    regex_file, max_word_length, min_word_length)


def word_is_fitting(word, node):
    """
    The word_is_fitting method checks if the word chosen can be fitted into the crossword
    word it is chosen for. It takes into account the length of the words plus the compatibility
    of letters crossing with the neighbors.

    input:   -word: string with the word we are trying to fit
             -node: string with the node on which we are trying to fit the word
    output:  -fits: boolean true when all checks pass, false otherwise
    """
    list_of_checks = []
    fits = False

    # Check for the length of the word to be equal with the length of the crossword node
    if len(word) == len(crossword[node][0]):

        list_of_checks.append(len(word) == len(crossword[node][0]))

        word_index = 0
        # This ckeck is mostly for the nodes that already have letters in them and cuts
        # the list by a lot.
        for letter in crossword[node][0]:
            list_of_checks.append(letter == word[word_index] or letter == '.')
            word_index += 1

        # checks if the whole list is True
        if list_of_checks.count(True) == len(list_of_checks):
            fits = True

    return fits


def find_all_fitting_words():
    """
    The find_all_fitting_words method finds all the possible words that can fit into a crossword
    word and inputs them to a global dictionary. The words are input as pairs of them and their
    regular expression and this dictionary has the following form:

    fitting_words = {
        '0': [[reg_expression1, word1], [reg_expression2, word2], [reg_expression3, word3]],
        '1': [[reg_expression1, word1], [reg_expression2, word2], [reg_expression3, word3]],
        .
        .
        .
    }
    """
    for key in crossword.keys():
        words_list = []
        for regex, value in sorted(regex_words.items()):
            for word in value:
                if word_is_fitting(word, key):
                    words_list.append([regex, word])

        fitting_words[key] = words_list


# --> filled is a list with the length of the crossword keys that represents which words are filled.
filled = [False] * len(crossword)

# --> used is a dictionary {reg_expression: True|False} that keeps track which words are being used
# so they are not used again
used = {key: False for key in regex_words.keys()}

# --> g is a graph with the neighbors of each node (word)
g = {}
for key, value in crossword.items():
    g[key] = value[1::2]

# Here we find all the fitting words from the method above
fitting_words = {}
find_all_fitting_words()


solution = {}


def word_fits(word, node):
    """
    The word_fits function checks for a word that we want to input in the crossword and it's fitting.
    The checks happen for every neighbor and the points of check are the cross points. If no neibhor
    exists then the word fits for sure and the method returns true.

    input:   -word: string with the word we are trying to fit
             -node: string with the node on which we are trying to fit the word
    output:  -fits: boolean true when all checks pass, false otherwise
    """
    fits = True
    list_of_checks = []

    i = 2
    for neighbor in g[node]:
        if neighbor in solution:

            neighbor_letter_position = int(crossword[node][i])
            neighbor_index = int(g[neighbor].index(node))
            word_letter_position = int(
                crossword[neighbor][2*neighbor_index + 2])

            list_of_checks.append(solution[neighbor][1][neighbor_letter_position]
                                  == word[word_letter_position])
        i += 2

    # checks if the list has at least one False
    if list_of_checks.count(False) >= 1:
        fits = False

    return fits


def crossword_parse():

    # checks if the whole list is True
    if filled.count(True) != len(filled):

        node = str(filled.index(False))
        fitting_list = fitting_words[node]

        for word in fitting_list:

            # check if the word fits and the regex is not being used
            if word_fits(word[1], node) and not used[word[0]]:

                solution[node] = word
                filled[int(node)] = True
                used[word[0]] = True
                crossword_parse()

        # undo if the previous word if no words are fitting so recursion goes back
        if not filled[int(node)] and node != '0':
            filled[int(node) - 1] = False
            regex = solution[str(int(node) - 1)][0]
            used[regex] = False
            del solution[str(int(node) - 1)]


# uncomment the lines bellow and comment the crossword_parse() in order to get an average process times

# ---------------------------------- <<< >>> ---------------------------------------------

# iterations = 10
# start_time = time.time()

# for i in range(iterations):
#     crossword_parse()

# end_time = time.time()
# avg_time = (end_time - start_time) / iterations

# print("\n Average process time --- %s seconds ---" %
#       (avg_time))

crossword_parse()

correct_solution = {int(key): value for key, value in solution.items()}

for key, value in sorted(correct_solution.items()):
    print(key, value[0], value[1])
