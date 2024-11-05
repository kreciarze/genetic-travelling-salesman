from typing import TextIO


def parse_headers(file: TextIO) -> dict[str, str]:
    headers = {}

    for line in file:
        line = line.strip()

        if line.endswith("SECTION"):
            break

        parts = line.split(":")
        if len(parts) == 2:
            key, value = parts
            headers[key.strip()] = value.strip()

    return headers
