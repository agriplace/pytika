import pytest

from tika.api import TikaApi


@pytest.fixture
def api() -> TikaApi:
    return TikaApi()
