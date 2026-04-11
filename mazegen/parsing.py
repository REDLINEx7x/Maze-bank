from typing import Any
from mazegen.utilis import get_42_cells


def parse_config(filename: str) -> dict[str, Any]:

    with open(filename) as f:
        config = {}
        final_config: dict[str, Any] = {}
        keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]

        for line in f:
            clean_line = line.strip()
            if clean_line == "" or clean_line[0] == "#":
                continue
            elif "=" not in clean_line:
                raise Exception("invalid configuration")
            parts = clean_line.split("=")
            if len(parts) != 2:
                raise Exception("invalid configuration")
            config[parts[0].strip().upper()] = parts[1].strip()

        for key in keys:
            if key not in config:
                raise Exception(f"missing key {key}")

        for key in config:
            if key == "WIDTH" or key == "HEIGHT":
                final_config[key] = int(config[key])
            elif key == "ENTRY" or key == "EXIT":
                parts = config[key].split(",")
                if len(parts) != 2:
                    raise Exception("invalid configuration")
                coords_list = [int(s) for s in parts]
                final_config[key] = tuple(coords_list)
            elif key == "PERFECT":
                if config[key].upper() == "TRUE":
                    final_config[key] = True
                elif config[key].upper() == "FALSE":
                    final_config[key] = False
                else:
                    raise Exception("invalid configuration")
            elif key == "OUTPUT_FILE":
                final_config[key] = config[key].lower()
            elif key == "SEED":
                try:
                    final_config[key] = int(config[key])
                except ValueError:
                    raise Exception("SEED must be an integer.")
        if "SEED" not in final_config:
            final_config["SEED"] = None

        width = final_config["WIDTH"]
        height = final_config["HEIGHT"]
        entry = final_config["ENTRY"]
        exit = final_config["EXIT"]
        ex, ey = entry
        xx, xy = exit

        if not (0 <= ex < width and 0 <= ey < height):
            raise Exception(
                f"ENTRY {entry} is outside maze bounds ({width}x{height})."
            )

        if not (0 <= xx < width and 0 <= xy < height):
            raise Exception(
                f"EXIT {exit} is outside maze bounds ({width}x{height})."
            )

        if entry == exit:
            raise Exception("ENTRY and EXIT must be different cells.")

        pattern_cells = get_42_cells(width, height)
        entry_cell = (ey, ex)
        exit_cell = (xy, xx)
        for cell in pattern_cells:
            if entry_cell == cell:
                raise ValueError(
                    f"Entry {entry} overlaps with the '42' pattern."
                )
            if exit_cell == cell:
                raise ValueError(
                    f"Exit {exit} overlaps with the '42' pattern."
                )

        return final_config
