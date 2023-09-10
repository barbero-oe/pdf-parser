from pathlib import Path
from typing import Any, Dict

import pdfplumber
import yaml
from pdf_parser.types import Command, Request
from pdfplumber.display import PageImage
from pdfplumber.page import Page

from pdf_parser.extract import Extract
from pdf_parser.page_group import PageGroup
from pdf_parser.types import Box


class UnknownAction(Exception):
    pass


def parse_command(definition: Dict[str, Any]) -> Command:
    name = definition["type"]
    if name == "crop":
        box = Box(*definition["box"])
        return Command(name, lambda page: crop(page, box))
    else:
        raise UnknownAction(name)


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
    commands = [parse_command(command) for command in req["commands"]] + [Extract()]
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
