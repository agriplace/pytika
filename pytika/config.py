from typing import Callable

from typing_extensions import Literal, NotRequired, TypedDict

Bool = Literal["true", "false"]
GetTextOptions = TypedDict(
    "GetTextOptions",
    {
        "X-Tika-OCRoutputType": NotRequired[Literal["hocr", "txt"]],
        "X-Tika-OCRtimeoutSeconds": NotRequired[str],
        "X-Tika-OCRskipOcr": NotRequired[Bool],
        "X-Tika-PDFextractInlineImages": NotRequired[Bool],
    },
)


# TODO: Extend config using all TikaOCRConfig parameters
# https://github.com/apache/tika/blob/16c964611b7f086fdd56b7880908d82b508e0eb8/tika-parsers/tika-parsers-standard/tika-parsers-standard-modules/tika-parser-ocr-module/src/main/java/org/apache/tika/parser/ocr/TesseractOCRConfig.java#L564
class GetTextOptionsBuilder:
    @staticmethod
    def OnlyOCR() -> Callable[..., GetTextOptions]:
        """Returns only the OCR text, no other metadata."""

        def _only_ocr(opts: GetTextOptions) -> GetTextOptions:
            opts["X-Tika-OCRskipOcr"] = "true"
            return opts

        return _only_ocr

    @staticmethod
    def WithTimeout(timeout: int) -> Callable[..., GetTextOptions]:
        # Validate timeout
        try:
            t = int(timeout)
        except ValueError:
            raise ValueError("Timeout must be a positive integer")

        if t < 0:
            raise ValueError("Timeout must be a positive integer")

        def _with_timeout(opts: GetTextOptions) -> GetTextOptions:
            opts["X-Tika-OCRtimeoutSeconds"] = str(t)
            return opts

        return _with_timeout

    @staticmethod
    def WithBoundingBoxes() -> Callable[..., GetTextOptions]:
        """Returns OCR text in the HOCR format with bounding boxes."""

        def _with_bounding_boxes(opts: GetTextOptions) -> GetTextOptions:
            opts["X-Tika-OCRoutputType"] = "hocr"
            opts["Accept"] = "*/*"
            return opts

        return _with_bounding_boxes

    @staticmethod
    def AsPlainText() -> Callable[..., GetTextOptions]:
        """Returns a plain text response from Tika"""

        def _with_bounding_boxes(opts: GetTextOptions) -> GetTextOptions:
            opts["Accept"] = "text/plain"
            return opts

        return _with_bounding_boxes

    @staticmethod
    def SkipOCR():
        """Skip OCR completely. This will override any other OCR options"""

        def _skip_ocr(opts: GetTextOptions) -> GetTextOptions:
            opts["X-Tika-OCRskipOcr"] = "true"
            return opts

        return _skip_ocr

    def InlineOCR():
        """Extract inline images and run OCR on each if True.
        WARNING: This can be very slow, make sure you know what you're doing.
        For more info: https://cwiki.apache.org/confluence/display/tika/PDFParser%20(Apache%20PDFBox)
        """

        def _inline_ocr(opts: GetTextOptions) -> GetTextOptions:
            opts["X-Tika-PDFextractInlineImages"] = "true"
            return opts

        return _inline_ocr

    def OCROnly():
        """Enabled by default. This will render each PDF page and then run OCR on that image."""

        def _page_ocr(opts: GetTextOptions) -> GetTextOptions:
            opts["X-Tika-PDFOcrStrategy"] = "ocr_only"
            return opts

        return _page_ocr

    def OCRWithText():
        def _ocr_with_text(opts: GetTextOptions) -> GetTextOptions:
            opts["X-Tika-PDFOcrStrategy"] = "ocr_and_text_extraction"
            return opts

        return _ocr_with_text
