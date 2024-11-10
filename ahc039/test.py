# ruff: noqa: E731, E741
from collections import Counter
import os
import sys
import matplotlib.path as mpltPath


read = sys.stdin.readline
input = lambda: read().strip()
ir = lambda: int(read())
rir = lambda: range(int(read()))
mir = lambda: map(int, read().split())
lmir = lambda: list(map(int, read().split()))

DIR = "in"
OUTPUT = "out/result.txt"


def insides(fishes, coords):
    path = mpltPath.Path(coords)
    inside = path.contains_points(fishes)
    return sum(inside)


def score(mackerels, sardines, coords):
    return max(
        0,
        insides(mackerels, coords) - insides(sardines, coords) + 1,
    )


def test(filename):
    lines = [list(map(int, line.split())) for line in open(filename)]
    n = lines[0][0]
    mackerels = lines[1 : n + 1]
    sardines = lines[n + 1 :]
    os.system(f"python main.py < {filename} > {OUTPUT}")
    n, *coords = [tuple(map(int, line.split())) for line in open(OUTPUT)]
    assert n[0] == len(coords)
    assert 4 <= n[0] <= 1000
    assert all(0 <= x <= 100_000 and 0 <= y <= 100_000 for x, y in coords)
    assert all(
        (x1 == x2) != (y1 == y2)
        for (x1, y1), (x2, y2) in zip(coords, coords[1:] + [coords[0]])
    ), coords
    length = sum(
        abs(x1 - x2) + abs(y1 - y2)
        for (x1, y1), (x2, y2) in zip(coords, coords[1:] + [coords[0]])
    )
    assert length <= 400_000, length
    assert len(coords) == len(set(coords)), {
        k: v for k, v in Counter(coords).items() if v >= 2
    }
    return length, score(mackerels, sardines, coords)


def main():
    total = longest = 0
    for filename in sorted(os.listdir(DIR)):
        length, res = test(os.path.join(DIR, filename))
        longest = max(longest, length)
        total += res
        print(f"{filename}: {res:,}")
    print(f"{longest=}")
    print(f"{total:,}")


if __name__ == "__main__":
    main()
