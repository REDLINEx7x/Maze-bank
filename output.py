def generate_output(
    maze: list[list[int]],
    entry: tuple[int, int],
    exit: tuple[int, int],
    solution: list[str],
) -> None:
    output = ""
    for row in maze:
        for cell in row:
            output += f"{cell:X}"
        output += "\n"
    output += "\n"
    output += f"{entry[0]},{entry[1]}\n"
    output += f"{exit[0]},{exit[1]}\n"
    for sol in solution:
        output += f"{sol}"
    output += "\n"
    with open("maze.txt", "w") as f:
        f.write(output)
