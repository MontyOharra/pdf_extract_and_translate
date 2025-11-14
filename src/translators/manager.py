# -*- coding: utf-8 -*-
"""
Translation Manager - unified translation with automatic language detection.

This module provides a high-level interface that combines language detection
and translation into a single, easy-to-use workflow.
"""

from typing import Optional
from src.translators.language_detector import LangDetectDetector
from src.translators.deep_translator_wrapper import DeepTranslatorWrapper


class TranslationManager:
    """
    Manages the complete translation workflow with automatic language detection.

    This class combines language detection and translation into a unified interface.
    It automatically detects the source language of input text and translates it
    to the specified target language.

    Attributes:
        detector: Language detector instance for auto-detecting source language.
        translator: Translator instance for performing translations.

    Example:
        >>> manager = TranslationManager()
        >>> result = manager.auto_translate("Hello, how are you?", target_lang="es")
        >>> print(result)
        'Hola, como estas?'
    """

    def __init__(
        self,
        detector: Optional[LangDetectDetector] = None,
        translator: Optional[DeepTranslatorWrapper] = None
    ):
        """
        Initialize the translation manager.

        Args:
            detector: Optional language detector instance. If None, creates a new
                     LangDetectDetector instance.
            translator: Optional translator instance. If None, creates a new
                       DeepTranslatorWrapper instance with Google backend.

        Example:
            >>> manager = TranslationManager()
            >>> # Or with custom instances:
            >>> detector = LangDetectDetector()
            >>> translator = DeepTranslatorWrapper(backend='google')
            >>> manager = TranslationManager(detector=detector, translator=translator)
        """
        self.detector = detector if detector is not None else LangDetectDetector()
        self.translator = translator if translator is not None else DeepTranslatorWrapper(backend='google')

    def auto_translate(self, text: str, target_lang: str) -> str:
        """
        Automatically detect source language and translate to target language.

        This method performs a complete translation workflow:
        1. Validates input text and target language
        2. Detects the source language of the input text
        3. Translates from detected source language to target language
        4. Returns the translated text

        Args:
            text: The text to translate. Must not be empty or None.
            target_lang: Target language code (ISO 639-1, e.g., 'en', 'es', 'fr').
                        Must not be empty or None.

        Returns:
            The translated text in the target language.

        Raises:
            ValueError: If text is empty, None, or if target_lang is invalid.

        Example:
            >>> manager = TranslationManager()
            >>> manager.auto_translate("Hello", target_lang="es")
            'Hola'
            >>> manager.auto_translate("Bonjour", target_lang="en")
            'Hello'
            >>> manager.auto_translate("Guten Tag", target_lang="fr")
            'Bonjour'
        """
        # Validate text input
        if text is None:
            raise ValueError("Text cannot be None")

        if not isinstance(text, str):
            raise ValueError(f"Text must be a string, got {type(text).__name__}")

        # Strip whitespace and check if empty
        stripped_text = text.strip()
        if not stripped_text:
            raise ValueError("Text cannot be empty or contain only whitespace")

        # Validate target language
        if target_lang is None:
            raise ValueError("Target language cannot be None")

        if not isinstance(target_lang, str):
            raise ValueError(f"Target language must be a string, got {type(target_lang).__name__}")

        if not target_lang or not target_lang.strip():
            raise ValueError("Target language cannot be empty")

        # Step 1: Detect source language
        try:
            source_lang = self.detector.detect(stripped_text)
        except ValueError as e:
            # Re-raise detection errors with more context
            raise ValueError(f"Failed to detect source language: {str(e)}") from e

        # Step 2: Translate from detected source to target language
        try:
            translated_text = self.translator.translate(
                text=stripped_text,
                source_lang=source_lang,
                target_lang=target_lang.strip()
            )
            return translated_text
        except Exception as e:
            # Re-raise translation errors with context
            raise ValueError(
                f"Failed to translate from {source_lang} to {target_lang}: {str(e)}"
            ) from e
