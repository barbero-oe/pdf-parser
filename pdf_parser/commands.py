import dataclasses
import itertools
from pathlib import Path
from typing import List, Callable, Any, Dict

import pdfplumber
import yaml
from pdfplumber.display import PageImage
from pdfplumber.page import Page


class InvalidGroupDefinition(Exception):
    pass


class PageGroup:
    def __init__(self, definition: str):
        try:
            parts: List[int] = []
            for part in definition.split(","):
                if "-" in part:
                    begin, end = part.split("-")
                    parts.extend(range(int(begin), int(end) + 1))
                else:
                    parts.append(int(part))
            self.pages = parts
        except Exception:
            raise InvalidGroupDefinition(definition)

    def __contains__(self, item):
        return item in self.pages

    def __iter__(self):
        return iter(self.pages)


@dataclasses.dataclass
class Command:
    name: str
    fun: Callable[[Page], Page]

    def __call__(self, page: Page) -> Page:
        return self.fun(page)


@dataclasses.dataclass
class Request:
    pages: PageGroup
    commands: List[Command]


class UnknownAction(Exception):
    pass


def parse_command(definition: Dict[str, Any]) -> Command:
    name = definition["type"]
    if name == "crop":
        box = Box(*definition["box"])
        return Command(name, lambda page: crop(page, box))
    else:
        raise UnknownAction(name)


@dataclasses.dataclass
class Coord:
    x: int | float
    y: int | float

    def __iter__(self):
        return iter([self.x, self.y])


class Box:
    def __init__(
        self, x0: int | float, y0: int | float, x1: int | float, y1: int | float
    ):
        self.bottomLeft = Coord(x0, y0)
        self.topRight = Coord(x1, y1)

    def __iter__(self):
        return itertools.chain(self.bottomLeft, self.topRight)


def preview_crop(page: PageImage, box: Box) -> Page:
    page.draw_rects(
        [
            (0, 0, box.bottomLeft.x, page.original.height),
            (0, 0, box.bottomLeft.x, page.original.height),
            (0, 0, box.bottomLeft.x, page.original.height),
            (0, 0, box.bottomLeft.x, page.original.height),
        ]
    )


def crop(page: Page, box: Box) -> Page:
    return page.crop(tuple(box))


def parse(request: str) -> Request:
    req = yaml.safe_load(request)
    pages = PageGroup(req["pages"])
    commands = [parse_command(command) for command in req["commands"]]
    return Request(pages=pages, commands=commands)


def dispatch(request: str, input: Path, output: Path):
    req: Request = parse(request)
    pdf: pdfplumber.PDF
    with pdfplumber.open(input) as pdf:
        for index in req.pages:
            page = pdf.pages[index - 1]
            for command in req.commands:
                page = command(page)
            img = page.to_image()
            img.save(output / "1.jpeg", format="jpeg")
