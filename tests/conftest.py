import os.path
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def sample_pdf():
    folder = Path(__file__).parent.resolve()
    return folder / "assets" / "sample.pdf"
