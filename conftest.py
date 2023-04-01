import pytest

from pytika.api import TikaApi


@pytest.fixture
def api() -> TikaApi:
    return TikaApi()
