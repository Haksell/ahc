# ruff: noqa: E731, E741
from enum import Enum, auto
import random
import sys

read = sys.stdin.readline
input = lambda: read().strip()
ir = lambda: int(read())
rir = lambda: range(int(read()))
mir = lambda: map(int, read().split())
lmir = lambda: list(map(int, read().split()))

MAX = 100_000
ZONES = 25


class Dir(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()

    def dxdy(self):
        if self == Dir.NORTH:
            return (0, -1)
        if self == Dir.EAST:
            return (1, 0)
        if self == Dir.SOUTH:
            return (0, 1)
        if self == Dir.WEST:
            return (-1, 0)


def debug(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


def solve_zones(n, mackerels, sardines):
    zones = [[0] * 10 for _ in range(10)]
    for x, y in mackerels:
        zones[y * ZONES // (MAX + 1)][x * ZONES // (MAX + 1)] += 1
    for x, y in sardines:
        zones[y * ZONES // (MAX + 1)][x * ZONES // (MAX + 1)] -= 1
    (_, x, y) = max((zones[y][x], x, y) for y in range(ZONES) for x in range(ZONES))
    return [
        (x * MAX // ZONES, y * MAX // ZONES),
        (x * MAX // ZONES, (y + 1) * MAX // ZONES),
        ((x + 1) * MAX // ZONES, (y + 1) * MAX // ZONES),
        ((x + 1) * MAX // ZONES, y * MAX // ZONES),
    ]


def zone_to_coord(x, y):
    return (x * MAX // ZONES, y * MAX // ZONES)


def get_true_res(res):
    true_res = []
    cache = set()
    for i, (gx, gy, dir) in enumerate(res):
        next_dir = res[(i + 1) % len(res)][2]
        x, y = zone_to_coord(gx - 1, gy - 1)
        if (gx, gy) not in cache:
            true_res.append([x, y])
        else:
            dx, dy = dir.dxdy()
            ndx, ndy = next_dir.dxdy()
            true_res.append([x - dx, y - dy])
            true_res.append([x - dx + ndx, y - dy + ndy])
            true_res.append([x + ndx, y + ndy])
        cache.add((gx, gy))
    return true_res


def res_from_taken(taken):
    start = x, y = next(
        (x, y) for y in range(ZONES + 2) for x in range(ZONES + 2) if taken[y][x]
    )
    res = [(x, y, Dir.NORTH)]
    dir = Dir.EAST
    x += 1
    while (x, y) != start:
        res.append((x, y, dir))
        if dir == Dir.NORTH:
            if not taken[y - 1][x]:
                dir = Dir.EAST
            elif taken[y - 1][x - 1]:
                dir = Dir.WEST
        elif dir == Dir.EAST:
            if not taken[y][x]:
                dir = Dir.SOUTH
            elif taken[y - 1][x]:
                dir = Dir.NORTH
        elif dir == Dir.SOUTH:
            if not taken[y][x - 1]:
                dir = Dir.WEST
            elif taken[y][x]:
                dir = Dir.EAST
        elif dir == Dir.WEST:
            if not taken[y - 1][x - 1]:
                dir = Dir.NORTH
            elif taken[y][x - 1]:
                dir = Dir.SOUTH
        dx, dy = dir.dxdy()
        x += dx
        y += dy
    return get_true_res(res)


def solve(n, mackerels, sardines):
    zones = [[0] * ZONES for _ in range(ZONES)]
    for x, y in mackerels:
        zones[min(ZONES - 1, y * ZONES // (MAX + 1))][
            min(ZONES - 1, x * ZONES // (MAX + 1))
        ] += 1
    for x, y in sardines:
        zones[min(ZONES - 1, y * ZONES // (MAX + 1))][
            min(ZONES - 1, x * ZONES // (MAX + 1))
        ] -= 1
    (best, x, y) = max((zones[y][x], x, y) for y in range(ZONES) for x in range(ZONES))
    score = best
    taken = [[False] * (ZONES + 2) for _ in range(ZONES + 2)]
    taken[y + 1][x + 1] = True
    adjacent = {
        (x + dx, y + dy)
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]
        if 0 <= x + dx < ZONES and 0 <= y + dy < ZONES
    }
    best_res = [[25_000, 25_000], [25_000, 75_000], [75_000, 75_000], [75_000, 25_000]]
    for _ in range(100):
        (best, _, x, y) = max((zones[y][x], random.random(), x, y) for x, y in adjacent)
        taken[y + 1][x + 1] = True
        score += best
        # debug(sum(map(sum, taken)), score)
        if best < 0:
            break
        adjacent |= {
            (x + dx, y + dy)
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]
            if 0 <= x + dx < ZONES
            and 0 <= y + dy < ZONES
            and not taken[y + dy + 1][x + dx + 1]
        }
        adjacent.remove((x, y))
        res = res_from_taken(taken)
        length = sum(
            abs(x1 - x2) + abs(y1 - y2)
            for (x1, y1), (x2, y2) in zip(res, res[1:] + [res[0]])
        )
        if len(res) <= 1000 and length <= 400_000:
            best_res = res
    return best_res


def main():
    n = ir()
    mackerels = [lmir() for _ in range(n)]
    sardines = [lmir() for _ in range(n)]
    res = solve(n, mackerels, sardines)
    print(len(res))
    for x, y in res:
        print(x, y)


if __name__ == "__main__":
    main()
