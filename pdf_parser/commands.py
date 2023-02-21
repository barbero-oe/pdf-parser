import dataclasses
from pathlib import Path
from typing import List, Callable, Any, Tuple, Dict, cast

import pdfplumber
from pdfplumber.page import Page
import yaml


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
        coords: Box = cast(Box, definition["box"])
        return Command(name, lambda page: crop(page, coords))
    else:
        raise UnknownAction(name)


Box = Tuple[int | float, int | float, int | float, int | float]


def crop(page: Page, box: Box) -> Page:
    return page.crop(box)


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
