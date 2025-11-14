from langdetect import detect, LangDetectException, DetectorFactory

# Set seed for deterministic results
# langdetect uses random sampling, so we fix the seed for consistency
DetectorFactory.seed = 0


class LangDetectDetector():

    def detect(self, text: str) -> str:
        """
        Detect the language of the given text.

        Args:
            text: The text to analyze for language detection.
                  Should not be empty or None.

        Returns:
            ISO 639-1 language code (e.g., 'en' for English, 'es' for Spanish).
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
            language_code = detect(stripped_text)
            return language_code

        except LangDetectException as e:
            # This can happen with very short or ambiguous text
            raise ValueError(f"Could not detect language: {str(e)}") from e
