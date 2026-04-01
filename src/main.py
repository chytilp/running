import json
import os
from pathlib import Path

import toml


def main() -> None:
    config = toml.load("./src/config.toml")
    data_file = config['dataFile']
    folder = os.path.dirname(os.path.realpath(__file__))
    data = json.load(open(Path(folder, data_file)))
    print(f"data: {data}")

if __name__ == "__main__":
    main()
