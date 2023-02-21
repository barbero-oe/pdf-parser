from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def assets():
    tests = Path(__file__).parent.resolve()
    return tests / "assets"


@pytest.fixture(scope="session")
def sample_pdf(assets):
    return assets / "sample.pdf"
