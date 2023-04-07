import pytest

from pytika import errors
from pytika.api import TikaApi
from pytika.config import GetTextOptionsBuilder as opt


def test_get_meta(api: TikaApi):
    with open("tests/data/test.pdf", "rb") as file:
        metadata = api.get_meta(file)
        assert metadata["Content-Type"] == "application/pdf"


def test_get_meta_with_corrupt_file(api: TikaApi):
    with open("tests/data/corrupt.pdf", "rb") as file:
        with pytest.raises(errors.UnprocessableEntityException):
            api.get_meta(file)


def test_get_text_basic(api: TikaApi):
    with open("tests/data/test.pdf", "rb") as file:
        out = api.get_text(file, opt.AsPlainText()).decode()
        words = out.strip().replace("\n", "").split()
        assert words == ["dummy", "pdf", "file"]


def test_get_text_with_bounding_boxes(api: TikaApi):
    # Load expected data
    with open("tests/data/test.pdf.hocr") as file:
        want = file.read()

    with open("tests/data/test.pdf", "rb") as file:
        got = api.get_text(file, opt.WithBoundingBoxes()).decode()

    # Remove variable parts of the output
    index = want.find("tika-pdfbox-rendering")
    want = want[:index]
    got = got[:index]
    assert got == want
