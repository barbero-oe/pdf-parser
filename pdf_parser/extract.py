from typing import Any

from pdf_parser.types import Command
from pdfplumber.page import Page

from pdf_parser.types import Word


class Extract(Command):
    def __init__(self):
        self.name = "extract"
        self.fun = self.extract

    def extract(self, page: Page) -> Any:
        words: list[dict[str, Any]] = page.extract_words(
            extra_attrs=["fontname", "size"]
        )
        for word in [Word(w) for w in words]:
            ...
