import hashlib
import shutil
from pathlib import Path
from textwrap import dedent

from pdf_parser.commands import dispatch


def md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def expected_preview(actual: Path, expected: Path):
    if md5(actual) == md5(expected):
        return True
    name = f"{expected.stem}.actual{expected.suffix}"
    shutil.copy(actual, expected.parent / name)
    return False


def test_preview_crop(sample_pdf, tmp_path, assets):
    command = dedent(
        f"""\
        pages: "1"
        commands:
        - type: crop
          box: [30, 130, 538, 740]"""
    )
    dispatch(command, sample_pdf, tmp_path)
    assert expected_preview(tmp_path / "1.jpeg", assets / "crop.jpeg")
