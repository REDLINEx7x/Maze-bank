def generate_output(
    maze: list[list[int]],
    entry: tuple[int, int],
    exit: tuple[int, int],
    solution: list[str],
    output_file: str,
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
    try:
        with open(output_file, "w") as f:
            f.write(output)
    except PermissionError:
        print("\033[91mcan't open output file. "
              "Check the file path or permissions.\033[0m")
