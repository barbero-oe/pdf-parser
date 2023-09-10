from typing import List


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
