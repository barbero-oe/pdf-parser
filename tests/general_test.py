import pytest

from pdf_parser.commands import PageGroup, InvalidGroupDefinition


@pytest.mark.parametrize(
    "definition,check,expected",
    [
        ("2", 2, True),
        ("1", 2, False),
        ("1,3,4", 3, True),
        ("1-4", 3, True),
        ("1,3,8-10", 9, True),
        ("1,3,8-10", 7, False),
        ("1,3,8-10", 2, False),
        ("1,3,8-10,12", 12, True),
    ],
)
def test_page_grouping(definition, check, expected):
    group = PageGroup(definition)
    assert (check in group) == expected


@pytest.mark.parametrize("definition", ["1,", ",,", "-", ",-,", "1,2-5-8"])
def test_correct_grouping_formatting(definition):
    pytest.raises(InvalidGroupDefinition, lambda: PageGroup(definition))


def test_iterates_over_pages():
    pages = [page for page in PageGroup("1,2,5-8,10")]
    assert pages == [1, 2, 5, 6, 7, 8, 10]
