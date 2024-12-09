import itertools


def get_puzzle_input():
    with open("input.txt", "r") as file:
        numbers = [int(i) for i in file.read().strip()] + [0]

        pos, index = 0, 0
        files, spaces = [], []
        for file_len, space_len in list(zip(numbers, numbers[1:]))[::2]:
            files.append((index, (pos, file_len)))
            spaces.append((pos + file_len, space_len))

            pos += file_len + space_len
            index += 1

        return files, spaces


def run(move_strategy):
    files, spaces = get_puzzle_input()
    new_files = itertools.chain.from_iterable([move_strategy(file, spaces) for file in reversed(files)])
    return checksum(new_files)


def move_file_frag(file, spaces):
    if not spaces or spaces[0][0] > file[1][0]:
        return [file]

    file_index, (file_pos, file_len) = file
    space_pos, space_len = spaces.pop(0)

    if space_len > file_len:
        spaces.insert(0, (space_pos + file_len, space_len - file_len))
        return [(file_index, (space_pos, file_len))]

    elif space_len == file_len:
        return [(file_index, (space_pos, file_len))]

    elif space_len < file_len:
        return [(file_index, (space_pos, space_len))] + move_file_frag((file_index, (file_pos, file_len - space_len)), spaces)


def move_file_comp(file, spaces):
    file_index, (file_pos, file_len) = file

    for space_index, (space_pos, space_len) in enumerate(spaces):
        if space_pos > file_pos:
            continue

        if file_len <= space_len:
            spaces.pop(space_index)
            if file_len < space_len:
                spaces.insert(space_index, (space_pos + file_len, space_len - file_len))
            return [(file_index, (space_pos, file_len))]
    else:
        return [(file_index, (file_pos, file_len))]


def checksum(files):
    return sum(index * i for index, (file_pos, file_len) in files for i in range(file_pos, file_pos + file_len))


if __name__ == "__main__":
    print("Puzzle 1:", run(move_file_frag))  # Puzzle 1: 6344673854800
    print("Puzzle 2:", run(move_file_comp))  # Puzzle 2: 6360363199987
