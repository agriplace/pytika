import os
from enum import Enum
from io import BufferedReader

import requests

from tika import errors


class Status(Enum):
    OK = 200
    NO_CONTENT = 204  # Request completed successfully, no content
    UNPROCESSABLE_ENTITY = 422  # Unsupported mime-type, encrypted document, etc
    ERROR = 500


class TikaApi:
    def __init__(self, host=None, port=None):
        self.host = host or os.environ.get("TIKA_HOST", "localhost")
        self.port = port or os.environ.get("TIKA_PORT", 9998)

    @property
    def url(self):
        return f"http://{self.host}:{self.port}"

    @property
    def headers(self):
        return {"Accept": "application/json"}

    def handle_errors(self, res):
        if res.status_code == Status.UNPROCESSABLE_ENTITY.value:
            raise errors.UnprocessableEntityException(res.text)

        if res.status_code == Status.ERROR.value:
            raise errors.InternalServerException(res.text)

    def get_meta(self, file: BufferedReader) -> dict:
        """
        Get metadata from file-like object
        :param file: file-like object
        :return: dict with metadata
        """
        headers = self.headers
        res = requests.put(f"{self.url}/meta", data=file, headers=headers)

        self.handle_errors(res)

        metadata = res.json()
        return metadata