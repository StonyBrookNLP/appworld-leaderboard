import json


def read_json(file_path: str) -> list[dict] | dict:
    with open(file_path) as file:
        content = file.read()
    data = json.loads(content)
    return data


def write_json(data: list[dict] | dict, file_path: str) -> None:
    with open(file_path, "w") as file:
        with open(file_path, "w") as file:
            file.write(json.dumps(data, indent=4))
