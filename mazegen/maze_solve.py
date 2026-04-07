from collections import deque


NORTH = 1
EAST  = 2
SOUTH = 4
WEST  = 8

DIRECTIONS = {
    NORTH: (-1,  0, 'N'),
    EAST:  ( 0, +1, 'E'),
    SOUTH: (+1,  0, 'S'),
    WEST:  ( 0, -1, 'W'),
}


def solve(
    grid: list[list[int]],
    entry: tuple[int, int],
    exit: tuple[int, int],
    width: int,
    height: int,
) -> list[str]:

    start = (entry[1], entry[0])   # convert (col,row) to (row,col)
    end   = (exit[1],  exit[0])

    # queue stores: (row, col, path so far)
    queue: deque[tuple[int, int, list[str]]] = deque()
    queue.append((start[0], start[1], []))
    visited: set[tuple[int, int]] = {start}

    while queue:
        row, col, path = queue.popleft()

        if (row, col) == end:
            return path

        for direction, (dr, dc, letter) in DIRECTIONS.items():


            if grid[row][col] & direction:
                continue

            new_row = row + dr
            new_col = col + dc

            # out of bounds
            if not (0 <= new_row < height):
                continue
            if not (0 <= new_col < width):
                continue

            # already visited
            if (new_row, new_col) in visited:
                continue

            visited.add((new_row, new_col))
            queue.append((new_row, new_col, path + [letter]))

    return []


