import os.path

"""
Resposible for converting human-readable chunks into game-readable type

Functions:

    redo_chunk(filename) -> None

Constants:

    letter_by_state
    ctype_by_letter
"""

letter_by_state = {
    -10: 'A',
    -4: 'B',
    -3: 'C',
    -2: 'D',
    -1: 'E',
    1: 'F',
    2: 'G',
    3: 'I',
    4: 'H',
    5: 'J',
    6: 'K',
    7: 'L',
    8: 'M',
    9: 'F',
    10: 'G',
    11: 'H',
    12: 'I',
    13: 'J',
    14: 'K',
    15: 'L',
    16: 'M',
    17: 'N',
    18: 'O',
    19: 'P',
    20: 'Q',
    21: 'R',
    22: 'S',
    23: 'T',
    24: 'U',
    25: 'N',
    26: 'O',
    27: 'P',
    28: 'Q',
    29: 'V',
    30: 'W',
    31: 'X',
    32: 'Y',
    33: 'Z'
}
ctype_by_letter = {
    'A': ('H', (640, 0, 160, 160)),
    'B': ('N', (480, 0, 160, 160)),
    'C': ('N', (320, 0, 160, 160)),
    'D': ('N', (0, 0, 160, 160)),
    'E': ('N', (160, 0, 160, 160)),
    'F': ('W', (480, 160, 160, 160)),
    'G': ('W', (480, 640, 160, 160)),
    'H': ('W', (0, 160, 160, 160)),
    'I': ('W', (0, 640, 160, 160)),
    'J': ('W', (480, 320, 160, 160)),
    'K': ('W', (480, 480, 160, 160)),
    'L': ('W', (0, 320, 160, 160)),
    'M': ('W', (0, 480, 160, 160)),
    'N': ('W', (320, 160, 160, 160)),
    'O': ('W', (320, 640, 160, 160)),
    'P': ('W', (160, 160, 160, 160)),
    'Q': ('W', (160, 640, 160, 160)),
    'R': ('W', (640, 640, 160, 160)),
    'S': ('W', (640, 480, 160, 160)),
    'T': ('W', (640, 320, 160, 160)),
    'U': ('W', (640, 160, 160, 160)),
    'V': ('W', (320, 320, 160, 160)),
    'W': ('W', (320, 480, 160, 160)),
    'X': ('W', (160, 320, 160, 160)),
    'Y': ('W', (160, 480, 160, 160)),
    'Z': ('W', (320, 800, 160, 160))
}


def redo_chunk(difficulty: str, filename: str) -> None:
    """ Transforms a file that denotes empty tiles by '.', holes by 'H' and walls by 'W' \
        into a file that's readable by the load_chunk function
    :param difficulty: difficulty of the chunk
    :param filename: name of file, including '.txt', or 'all' to redo all files in the resources/chunks/difficulty directory
    """
    dump = open(os.path.join('resources', 'chunks', difficulty, filename), 'r').readlines()
    with open(os.path.join('resources', 'chunks', difficulty, filename), 'w') as f:
        for y, line in enumerate(dump[:-1]):
            for x, sym in enumerate(line.strip()):
                if sym == '.':
                    state = -1
                    if dump[y][x - 1] != '.': state -= 1
                    if dump[y][x + 1] != '.': state -= 2
                elif sym == 'H':
                    state = -10
                elif sym == '#':
                    state = 1  # a variable for encoding the state of various neighbours of the cell

                    # encoding neighbours
                    if y != 0 and dump[y - 1][x] == '#': state += 1
                    if x != len(line) - 1 and dump[y][x + 1] == '#': state += 2
                    if y != len(dump) - 1 and dump[y + 1][x] == '#': state += 4
                    if y != len(dump) - 1 and dump[y + 1][x - 1] == '#': state += 8
                    if x != 0 and dump[y][x - 1] == '#': state += 16

                    # fixing missing neighbours for tiles on the corners of the chunk
                    if y == 0 and (x == 0 or x == len(line) - 2):
                        state += 1
                    if y == len(dump) - 1 and (x == 0 or x == len(line) - 2):
                        state += 4

                letter = letter_by_state[state]
                f.write(letter)
            f.write('\n')


if __name__ == '__main__':
    difficulty = input("difficulty ")
    chunk_name = input("chunk name or 'all' ")
    if chunk_name == "all":
        for chunk_name in os.listdir(os.path.join('resources', 'chunks', difficulty)):
            redo_chunk(difficulty, chunk_name)
    else:
        redo_chunk(difficulty, chunk_name)
