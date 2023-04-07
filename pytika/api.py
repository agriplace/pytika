import os
from enum import Enum
from io import BufferedReader
from typing import Callable, List

import requests

from pytika import errors
from pytika.config import GetTextOptions, GetTextOptionsBuilder


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

    def get_meta(self, file: BufferedReader, key=None) -> dict:
        """
        Get metadata from file-like object
        :param file: file-like object
        :param key optional: metadata key to retrieve only one value
        :return: dict with metadata
        """
        headers = self.headers
        url = f"{self.url}/meta"

        if key:
            url += f"/{key}"

        res = requests.put(url, data=file, headers=headers)

        self.handle_errors(res)

        metadata = res.json()
        return metadata

    def get_text(
        self,
        file: BufferedReader,
        *opts: List[Callable[..., GetTextOptions]],
    ) -> bytes:
        """
        Get text from file-like object. By default returns xml without bounding boxes.
        Use WithBoundingBoxes or AsPlainText options to change this behaviour.
        Reference: https://cwiki.apache.org/confluence/display/tika/TikaOCR

        :param file: file-like object
        :return: text as bytes
        """
        headers = self.headers
        headers["Accept"] = "*/*"  # Do not want to force json

        defaults = [GetTextOptionsBuilder.OCROnly()]
        defaults.extend(opts)
        for opt in defaults:
            headers = opt(headers)

        url = f"{self.url}/tika"

        res = requests.put(url, data=file, headers=headers)

        self.handle_errors(res)

        return res.content
