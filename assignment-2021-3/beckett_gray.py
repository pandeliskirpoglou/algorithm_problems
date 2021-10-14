import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
    "number_of_bits", help="Integer with the length of bits on the gray code")

args = parser.parse_args()

number_of_bits = int(args.number_of_bits)


def find_gray_code(n):
    """
    The find gray code method recieves the number of bits of the gray code we search for
    and outputs the list of all the different numbers. In order to achieve this we use a 
    stack to reverse the order of each gray code and add the object with reflecting order.
    Finally, we add 0 to the start of the numbers of the first half and then append the 
    second half with a 1 on the front.

    input:   -n: integer with the number of bits of the gray code
    output:  -gray_code: list with the gray code of n bits ['000', '001', ..., '100']
    """
    gray_code = [0, 1]
    i = 1
    stack = []

    while(i < n):
        i += 1
        # use stsack to achieve reflection
        for j in range(pow(2, i - 1)):
            stack.append(gray_code[j])

        for z in range(pow(2, i - 1)):
            gray_code[z] = '0' + (str)(gray_code[z])

        # Take out the second half from the stack to put them into list
        for m in range(pow(2, i - 1)):
            gray_code.append('1' + (str)(stack.pop()))

    return gray_code


gray_list = find_gray_code(number_of_bits)

g = {x: [] for x in gray_list}


def make_graph():
    """
    The make graph function creates the hypercube for the dfs algorithm
    to go through. For each code, it searaches through all the rest
    of the codes to find those who have at most one change. If this is
    true it appends the code into the code's neighbors.
    """
    for code1 in gray_list:
        for code2 in gray_list:
            changes = 0
            i = 0
            if code1 != code2:
                while i < len(code1):
                    if code1[i] != code2[i]:
                        changes += 1
                    i += 1
            if changes <= 1:
                g[code1].append(code2)


make_graph()


def flip(x, i):
    """
    The flip function returns the opposite bit of a number x.

    input:   -x: The number of which the bit we want to flip "1001101"
    output:  -i: The position of the bit we want to change    
    """

    if x[i] == '0':
        return '1'
    elif x[i] == '1':
        return '0'


all_codes = []
gc = []
visited = {x: False for x in gray_list}


def gc_dfs(d, x, max_coord, n, gc):
    """
    The dfs algorithm is the one which finds all the possible gray codes.

    input:   -d: Recursion depth
             -x: The code of the current node
             -max_coord: The maximum coordinate of the bit which has stayed
             most unchanged
             -n: The number of bits of the codes
             -gc: The stack of codes
    output:  -all_codes: All possible gray codes 

    """

    if d == 2 ** n:
        all_codes.append(gc)
        return

    for i in range(0, min(n - 1, max_coord + 1)):
        # cannot change one letter of a string so we turn it
        # into list and back
        text = list(x)
        text[i] = flip(x, i)
        x = '' .join(text)

        if not visited[x]:
            visited[x] = True
            gc.append(x)
            gc_dfs(d + 1, x, max(i + 1, max_coord), n, gc)
            visited[x] = False
            gc.pop()

        text = list(x)
        text[i] = flip(x, i)
        x = '' .join(text)


gc_dfs(1, gray_list[0], 0, number_of_bits, gc)
