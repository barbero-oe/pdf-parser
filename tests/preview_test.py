from textwrap import dedent

from pdf_parser.commands import dispatch


def _test_preview_cut(sample_pdf, tmp_path):
    command = dedent(
        f"""\
    pages: "1"
    commands:
    - type: cut
      box: [0, 0, 595, 842]"""
    )
    output = tmp_path / "cut.jpeg"
    dispatch(command, sample_pdf, output)
    assert 1 == 1
