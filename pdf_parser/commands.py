from pathlib import Path
from typing import List

import pdfplumber


class PageGroup:
    def __init__(self, definition: str):
        parts: List[int] = []
        for part in definition.split(","):
            if "-" in part:
                begin, end = part.split("-")
                parts.extend(range(int(begin), int(end) + 1))
            else:
                parts.append(int(part))
        self.pages = parts

    def __contains__(self, item):
        return item in self.pages


def dispatch(command: str, input: Path, output: Path):
    # comm = yaml.safe_load(command)
    pdf: pdfplumber.PDF
    with pdfplumber.open(input) as pdf:
        page = pdf.pages[0].crop((0, 0, 595, 842))
        img = page.to_image()
        img.save(output, format="jpeg")
