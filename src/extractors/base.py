from abc import ABC, abstractmethod
from typing import Union
from pathlib import Path


class TextExtractor(ABC):
    """
    Abstract base class for all text extraction implementations.

    All text extractors (OCR, PDF readers, etc.) must inherit from this class
    and implement the required methods. This enables a plugin-based architecture
    where different extraction engines can be used interchangeably.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Return the name of this extractor.

        This is used for identification and selection in the CLI.

        Returns:
            A human-readable name for this extractor (e.g., "Tesseract OCR",
            "PyMuPDF", "EasyOCR")
        """
        pass

    @abstractmethod
    def extract_text(self, input_data: Union[str, Path]) -> str:
        """
        Extract text from a document.

        Args:
            input_data: Path to the document to extract text from.
                       Can be a string path or pathlib.Path object.

        Returns:
            The extracted text as a string.
        """
        pass

    @abstractmethod
    def supports_format(self, file_format: str) -> bool:
        """
        Check if this extractor supports the given file format.

        Args:
            file_format: File format/extension to check (e.g., 'pdf', 'png', 'jpg').
                        Should be case-insensitive.

        Returns:
            True if the format is supported, False otherwise.
        """
        pass
