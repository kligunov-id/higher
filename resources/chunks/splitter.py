import os.path


def split_to_chunks(filename, difficulty) -> None:
    """
    splits a file into chunks, with chunks initially separated by empty lines
    :param filename: the name of file to be split
    :param difficulty: the difficulty of chunks
    :return: None
    """
    dump = open(filename).readlines()
    chunk = []
    number = 1
    for line in dump:
        if line.strip() == '':
            with open(os.path.join(difficulty, difficulty + '_' + str(number) + '.txt'), 'w') as f:
                for cline in chunk:
                    f.write(cline)
            chunk = []
            number += 1
        else:
            chunk.append(line)


if __name__ == "__main__":
    split_to_chunks(input("filename "), input("difficulty "))
