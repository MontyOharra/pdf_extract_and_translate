"""
Abstract base classes for translation system.

This module defines the interfaces that all language detectors and translators
must implement, enabling a plugin-based architecture.
"""

from abc import ABC, abstractmethod
from typing import Optional


class LanguageDetector(ABC):
    """
    Abstract base class for language detection implementations.

    All language detectors must inherit from this class and implement
    the detect() method.
    """

    @abstractmethod
    def detect(self, text: str) -> str:
        """
        Detect the language of the given text.

        Args:
            text: The text to analyze for language detection.
                  Should not be empty.

        Returns:
            ISO 639-1 language code (e.g., 'en' for English, 'es' for Spanish,
            'fr' for French, 'de' for German, etc.)

        Raises:
            ValueError: If text is empty, None, or invalid.
        """
        pass


class Translator(ABC):
    """
    Abstract base class for translation implementations.

    All translators must inherit from this class and implement the
    translate() method and name property.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Return the name of this translator.

        This is used for identification and selection in the CLI.

        Returns:
            A human-readable name for this translator (e.g., "Google Translate",
            "DeepL", "Argos Translate")
        """
        pass

    @abstractmethod
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text from source language to target language.

        Args:
            text: The text to translate. Should not be empty.
            source_lang: Source language code (ISO 639-1, e.g., 'en', 'es').
            target_lang: Target language code (ISO 639-1, e.g., 'en', 'es').

        Returns:
            The translated text in the target language.

        Raises:
            ValueError: If text is empty, None, or if language codes are invalid.
            NotImplementedError: If the language pair is not supported.
        """
        pass

    def supports_language(self, lang_code: str) -> bool:
        """
        Check if this translator supports the given language.

        This is a default implementation that returns True for all languages.
        Subclasses should override this method with their specific logic to
        check against their supported language list.

        Args:
            lang_code: ISO 639-1 language code (e.g., 'en', 'es', 'fr')

        Returns:
            True if the language is supported, False otherwise.
            Default implementation returns True (assumes all languages supported).

        Example:
            >>> translator = SomeTranslator()
            >>> translator.supports_language('en')
            True
            >>> translator.supports_language('invalid')
            False  # If subclass implements proper validation
        """
        return True  # Default: assume all languages supported
