import dataclasses
import itertools
from typing import Callable, List, Any

from pdfplumber.page import Page

from pdf_parser.page_group import PageGroup


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


@dataclasses.dataclass
class Word:
    def __init__(self, word: dict[str, Any]):
        self.text: str = word["text"]
        self.box: Box = Box(word["x0"], word["bottom"], word["x1"], word["top"])
        self.fontname: str = word["fontname"]
        self.size: float = word["size"]
