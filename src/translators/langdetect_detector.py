# -*- coding: utf-8 -*-
"""
Language detection implementation using the langdetect library.

This module provides a concrete implementation of the LanguageDetector
abstract base class using Google's langdetect library.
"""

from langdetect import detect, LangDetectException, DetectorFactory
from src.translators.base import LanguageDetector

# Set seed for deterministic results
# langdetect uses random sampling, so we fix the seed for consistency
DetectorFactory.seed = 0


class LangDetectDetector(LanguageDetector):
    """
    Language detector using the langdetect library.

    This implementation uses langdetect, a port of Google's language-detection
    library, which supports 55+ languages. It uses a Naive Bayesian classifier
    to determine the language of text.

    Note: langdetect has non-deterministic behavior for very short texts due to
    its random seed initialization. For consistent results, use texts with at
    least a few words.
    """

    def detect(self, text: str) -> str:
        """
        Detect the language of the given text.

        Args:
            text: The text to analyze for language detection.
                  Should not be empty or None.

        Returns:
            ISO 639-1 language code (e.g., 'en' for English, 'es' for Spanish).

        Raises:
            ValueError: If text is None, empty, or contains only whitespace.

        Examples:
            >>> detector = LangDetectDetector()
            >>> detector.detect("Hello, how are you?")
            'en'
            >>> detector.detect("Hola")
            'es'
            >>> detector.detect("Bonjour")
            'fr'
        """
        # Validate input
        if text is None:
            raise ValueError("Text cannot be None")

        if not isinstance(text, str):
            raise ValueError(f"Text must be a string, got {type(text).__name__}")

        # Strip whitespace and check if empty
        stripped_text = text.strip()
        if not stripped_text:
            raise ValueError("Text cannot be empty or contain only whitespace")

        try:
            # Use langdetect to detect the language
            # Returns ISO 639-1 code (e.g., 'en', 'es', 'fr')
            language_code = detect(stripped_text)
            return language_code

        except LangDetectException as e:
            # This can happen with very short or ambiguous text
            # Re-raise as ValueError with a clearer message
            raise ValueError(f"Could not detect language: {str(e)}") from e
