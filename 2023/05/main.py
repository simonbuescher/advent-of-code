class SeedRange:
    def __init__(self, start, end):
        self._start = start
        self._end = end

    def map(self, range_map):
        src, dest, size = range_map

        if self._end <= src or (src + size) <= self._start:
            # seed range outside of mapping range
            return False, [], []
        elif self._start == src and self._end == (src + size):
            # seed range exactly matches mapping range
            return True, [SeedRange(dest, dest + size)], []
        elif self._start < src < (src + size) < self._end:
            # mapping range inside seed range
            return True, [SeedRange(dest, dest + size)], [SeedRange(self._start, src), SeedRange(src + size, self._end)]
        elif src <= self._start < (src + size) < self._end:
            # start of seed range inside mapping range, end is outside
            return True, [SeedRange(self._start + dest - src, dest + size)], [SeedRange(src + size, self._end)]
        elif self._start < src <= self._end <= (src + size):
            # start of seed range outside of mapping range, end is inside
            return True, [SeedRange(dest, self._end + dest - src)], [SeedRange(self._start, src)]
        elif src <= self._start <= self._end <= (src + size):
            # seed range inside mapping range
            return True, [SeedRange(self._start + dest - src, self._end + dest - src)], []

    def get_start(self):
        return self._start


def get_puzzle_input():
    with open("input.txt", "r") as file:
        content = file.read()

    def get_seeds(seed_str):
        return [int(seed) for seed in seed_str[7:].split()]

    def get_map(map_str):
        return [(int(line.split()[1]), int(line.split()[0]), int(line.split()[2])) for line in map_str.split("\n")[1:]]

    maps = content.split("\n\n")
    return get_seeds(maps[0]), [get_map(map_str) for map_str in maps[1:]]


def run(seed_ranges, maps):
    open_set = seed_ranges
    for map in maps:
        results = []
        while open_set:
            seed_range = open_set.pop(0)
            for range_map in map:
                did_map, mapped, unmapped = seed_range.map(range_map)
                if did_map:
                    results.extend(mapped)
                    open_set.extend(unmapped)
                    break
            else:
                results.append(seed_range)
        open_set = results

    return min(seed_range.get_start() for seed_range in open_set)


def first_puzzle():
    seeds, maps = get_puzzle_input()
    seed_ranges = [SeedRange(seed, seed + 1) for seed in seeds]
    result = run(seed_ranges, maps)
    print(f"Puzzle 1: {result}")


def second_puzzle():
    seeds, maps = get_puzzle_input()
    seed_pairs = list(zip(seeds[0::2], seeds[1::2]))
    seed_ranges = [SeedRange(seed, seed + size) for seed, size in seed_pairs]
    result = run(seed_ranges, maps)
    print(f"Puzzle 2: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 227653707
    second_puzzle()  # Puzzle 2: 78775051
