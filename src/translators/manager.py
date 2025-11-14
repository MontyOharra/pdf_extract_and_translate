from typing import Optional
from src.translators.language_detector import LangDetectDetector
from src.translators.deep_translator_wrapper import DeepTranslatorWrapper


class TranslationManager:
    """
    Manages the complete translation workflow with automatic language detection.
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
                     LangDetectDetector instance
            translator: Optional translator instance. If None, creates a new
                       DeepTranslatorWrapper instance with Google backend
        """
        self.detector = detector if detector is not None else LangDetectDetector()
        self.translator = translator if translator is not None else DeepTranslatorWrapper(backend='google')

    def auto_translate(self, text: str, target_lang: str) -> str:
        """
        Translate text that may contain multiple languages line-by-line

        Args:
            text: The text to translate. May contain multiple languages
            target_lang: Target language code

        Returns:
            The translated text with all lines in the target language
        """
        # Validate inputs
        if text is None:
            raise ValueError("Text cannot be None")

        if not isinstance(text, str):
            raise ValueError(f"Text must be a string, got {type(text).__name__}")

        if not text.strip():
            raise ValueError("Text cannot be empty or contain only whitespace")

        if target_lang is None or not isinstance(target_lang, str) or not target_lang.strip():
            raise ValueError("Target language must be a non-empty string")

        # Split into lines
        lines = text.splitlines()
        translated_lines = []

        for line in lines:
            # Preserve empty lines
            if not line.strip():
                translated_lines.append(line)
                continue

            try:
                # Detect language of this line
                source_lang = self.detector.detect(line.strip())

                # If already in target language, keep as is
                if source_lang == target_lang.strip():
                    translated_lines.append(line)
                else:
                    # Translate this line
                    translated_line = self.translator.translate(
                        text=line.strip(),
                        source_lang=source_lang,
                        target_lang=target_lang.strip()
                    )
                    translated_lines.append(translated_line)
            except Exception:
                # If detection or translation fails for a line, keep original
                translated_lines.append(line)

        return '\n'.join(translated_lines)
