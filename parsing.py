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
        return final_config

CONFIG = parse_config("config.txt")

#try:
#    data = parse_config("config.txt")
#    print(data)
#except FileNotFoundError as e:
#    print(e)
#except ValueError as e:
#    print("Error: invalid configuration")
#except Exception as e:
#    print(e)
