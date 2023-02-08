import pytest

from tika import errors
from tika.api import TikaApi


def test_get_meta(api: TikaApi):
    with open("tests/data/test.pdf", "rb") as file:
        metadata = api.get_meta(file)
        assert metadata["Content-Type"] == "application/pdf"


def test_get_meta_with_corrupt_file(api: TikaApi):
    with open("tests/data/corrupt.pdf", "rb") as file:
        with pytest.raises(errors.UnprocessableEntityException):
            api.get_meta(file)
