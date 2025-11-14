from typing import Optional
from deep_translator import GoogleTranslator

class DeepTranslatorWrapper:
    """
    Wrapper for deep-translator library using Google Translate.
    """

    # Mapping of backend names to their corresponding deep-translator classes
    BACKENDS = {
        'google': GoogleTranslator,
    }

    # Supported languages for validation
    # Common ISO 639-1 language codes supported by most backends
    SUPPORTED_LANGUAGES = {
        'en', 'es', 'fr', 'de', 'it', 'pt', 'nl', 'pl', 'ru', 'ja',
        'ko', 'zh-CN', 'zh-TW', 'ar', 'hi', 'tr', 'vi', 'th', 'sv',
        'da', 'fi', 'no', 'cs', 'el', 'he', 'id', 'ms', 'ro', 'uk',
        'auto'  # auto-detect source language
    }

    def __init__(self, backend: str = 'google', api_key: Optional[str] = None):
        """
        Initialize the translator with a specific backend.

        Args:
            backend: Which translation backend to use. Currently only 'google' is supported.
                    Defaults to 'google'.
            api_key: Optional API key for services that require it (future use).
        """
        if not backend or backend not in self.BACKENDS:
            raise ValueError(
                f"Unsupported backend: {backend}. "
                f"Supported backends: {', '.join(self.BACKENDS.keys())}"
            )

        self.backend = backend
        self.api_key = api_key
        self._backend_class = self.BACKENDS[backend]

    @property
    def name(self) -> str:
        """
        Return the name of this translator.

        Returns:
            A human-readable name reflecting the backend being used.
        """
        return f"{self.backend.title()} Translator"

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text from source language to target language.

        Args:
            text: The text to translate. Must not be empty or None.
            source_lang: Source language code ISO 639-1
                        Use 'auto' to auto-detect the source language.
            target_lang: Target language code ISO 639-1

        Returns:
            The translated text in the target language.
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

        # Validate language codes
        if not source_lang or not isinstance(source_lang, str):
            raise ValueError("Source language code must be a non-empty string")

        if not target_lang or not isinstance(target_lang, str):
            raise ValueError("Target language code must be a non-empty string")

        # Create translator instance with the specified languages
        try:
            translator_instance = self._backend_class(
                source=source_lang,
                target=target_lang
            )

            result = translator_instance.translate(stripped_text)

            return result

        except Exception as e:
            # Re-raise with more context if it's a language-related error
            error_msg = str(e).lower()
            if 'language' in error_msg or 'lang' in error_msg:
                raise ValueError(
                    f"Invalid language code. Source: {source_lang}, Target: {target_lang}. "
                    f"Error: {str(e)}"
                ) from e
            raise

    def supports_language(self, lang_code: str) -> bool:
        """
        Check if this translator supports the given language.

        Args:
            lang_code: ISO 639-1 language code

        Returns:
            True if the language is supported, False otherwise.
        """
        if not lang_code or not isinstance(lang_code, str):
            return False

        # Check against our known supported languages
        return lang_code.lower() in self.SUPPORTED_LANGUAGES
