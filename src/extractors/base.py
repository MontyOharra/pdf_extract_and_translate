# -*- coding: utf-8 -*-
"""
Abstract base classes for text extraction system.

This module defines the interfaces that all text extractors must implement,
enabling a plugin-based architecture for different extraction methods.
"""

from abc import ABC, abstractmethod
from typing import Union
from pathlib import Path


class TextExtractor(ABC):
    """
    Abstract base class for all text extraction implementations.

    All text extractors (OCR, PDF readers, etc.) must inherit from this class
    and implement the required methods. This enables a plugin-based architecture
    where different extraction engines can be used interchangeably.

    Example:
        >>> class MyExtractor(TextExtractor):
        ...     @property
        ...     def name(self):
        ...         return "My Extractor"
        ...
        ...     def extract_text(self, input_data):
        ...         # Implementation here
        ...         return "extracted text"
        ...
        ...     def supports_format(self, file_format):
        ...         return file_format.lower() == "pdf"
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

        Example:
            >>> extractor = SomeExtractor()
            >>> extractor.name
            'Tesseract OCR'
        """
        pass

    @abstractmethod
    def extract_text(self, input_data: Union[str, Path]) -> str:
        """
        Extract text from a document.

        This is the main method that performs text extraction from the given
        input. The input can be a file path (as string or Path object).

        Args:
            input_data: Path to the document to extract text from.
                       Can be a string path or pathlib.Path object.

        Returns:
            The extracted text as a string.

        Raises:
            FileNotFoundError: If the input file doesn't exist.
            ValueError: If the file format is not supported.
            Exception: For other extraction errors.

        Example:
            >>> extractor = SomeExtractor()
            >>> text = extractor.extract_text("document.pdf")
            >>> print(text)
            'This is the extracted text...'
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

        Example:
            >>> extractor = SomeExtractor()
            >>> extractor.supports_format('pdf')
            True
            >>> extractor.supports_format('docx')
            False
        """
        pass
