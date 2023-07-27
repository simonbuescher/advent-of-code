import itertools


class Directory:
    def __init__(self, name, parent):
        self._name = name
        self._parent = parent
        self._files = {}

    def name(self):
        return self._name

    def size(self):
        return sum(file.size() for name, file in self._files.items())

    def change_directory(self, file_name):
        if file_name == "..":
            return self._parent
        return self._files[file_name]

    def add_file(self, file):
        self._files.update({file.name(): file})

    def get_dirs(self):
        my_dirs = [file for name, file in self._files.items() if isinstance(file, Directory)]
        child_dirs = [directory.get_dirs() for directory in my_dirs]

        return itertools.chain(my_dirs, *child_dirs)

    def __repr__(self):
        return f"Dir(name={self._name}, files={list(self._files.values())})"


class File:
    def __init__(self, name, size, parent):
        self._name = name
        self._size = size
        self._parent = parent

    def name(self):
        return self._name

    def size(self):
        return self._size

    def change_directory(self, file_name):
        raise ValueError("change_directory(file_name) cannot be called on file")

    def add_file(self, file):
        raise ValueError("add_file(file) cannot be called on file")

    def get_dirs(self):
        raise ValueError("get_dirs() cannot be called on file")

    def __repr__(self):
        return f"File(name={self._name}, size={self._size})"


def read_puzzle_input():
    with open("input.txt", "r") as file:
        return file.read().strip()


def parse_puzzle_input(puzzle_input):
    commands = puzzle_input.split("$ ")[1:]

    root = Directory("/", None)
    current_dir = root

    for command in commands:
        if command.startswith("cd"):
            path = command.strip()[3:]
            if path == "/":
                current_dir = root
            else:
                current_dir = current_dir.change_directory(path)

        elif command.startswith("ls"):
            files = command.strip().split("\n")[1:]
            for file in files:
                if file.startswith("dir"):
                    name = file[4:]
                    current_dir.add_file(Directory(name, current_dir))
                else:
                    size, name = file.split(" ")
                    current_dir.add_file(File(name, int(size), current_dir))

    return root


def first_puzzle():
    puzzle_input = read_puzzle_input()
    root = parse_puzzle_input(puzzle_input)

    dirs = root.get_dirs()

    sizes = [directory.size() for directory in dirs]
    result = sum(size for size in sizes if size <= 100000)
    print(f"Puzzle 1 Answer: {result}")


def second_puzzle():
    puzzle_input = read_puzzle_input()
    root = parse_puzzle_input(puzzle_input)

    total_disk_space = 70000000
    total_required_disk_space = 30000000

    free_space = total_disk_space - root.size()
    required_space = total_required_disk_space - free_space

    dirs = root.get_dirs()
    result = list(sorted(directory.size() for directory in dirs if directory.size() >= required_space))[0]
    print(f"Puzzle 2 Answer: {result}")


if __name__ == "__main__":
    first_puzzle()
    second_puzzle()
