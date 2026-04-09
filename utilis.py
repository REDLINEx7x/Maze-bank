def get_42_cells(width: int, height: int) -> set[tuple[int, int]]:

    pattern = [
        "#   ###",
        "#     #",
        "### ###",
        "  # #  ",
        "  # ###"
        ]
    patt_height = len(pattern)
    patt_width = len(pattern[0])

    cells: set[tuple[int, int]] = set()

    if height < patt_height + 2 or width < patt_width + 2:
        return cells

    start_row = (height - patt_height) // 2
    start_col = (width - patt_width) // 2

    for p_row, line in enumerate(pattern):
        for p_col, char in enumerate(line):
            if char == "#":
                r = start_row + p_row
                c = start_col + p_col
                cells.add((r, c))
    return cells
