from typing import Any


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

        width  = final_config["WIDTH"]
        height = final_config["HEIGHT"]
        entry  = final_config["ENTRY"]
        exit_  = final_config["EXIT"]
        ex, ey = entry
        xx, xy = exit_

        if not (0 <= ex < width and 0 <= ey < height):
            raise Exception(
                f"ENTRY {entry} is outside maze bounds ({width}x{height})."
            )

        if not (0 <= xx < width and 0 <= xy < height):
            raise Exception(
                f"EXIT {exit_} is outside maze bounds ({width}x{height})."
            )

        if entry == exit_:
            raise Exception("ENTRY and EXIT must be different cells.")

        return final_config


#try:
#    data = parse_config("config.txt")
#    print(data)
#except FileNotFoundError as e:
#    print(e)
#except ValueError as e:
#    print("Error: invalid configuration")
#except Exception as e:
#    print(e)
