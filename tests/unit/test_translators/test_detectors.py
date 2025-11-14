# -*- coding: utf-8 -*-
"""
Unit tests for language detector implementations.

Following TDD approach:
1. Write tests first (RED - tests fail)
2. Implement to pass tests (GREEN)
3. Refactor while keeping tests passing
"""

import pytest


class TestLangDetectDetector:
    """Test suite for LangDetectDetector implementation."""

    def test_detect_english(self):
        """Test detection of English text."""
        from src.translators.langdetect_detector import LangDetectDetector

        detector = LangDetectDetector()
        result = detector.detect("Good morning, how are you doing today? I hope you are having a wonderful day.")

        assert result == "en"

    def test_detect_spanish(self):
        """Test detection of Spanish text."""
        from src.translators.langdetect_detector import LangDetectDetector

        detector = LangDetectDetector()
        result = detector.detect("Hola, ¿cómo estás?")

        assert result == "es"

    def test_detect_french(self):
        """Test detection of French text."""
        from src.translators.langdetect_detector import LangDetectDetector

        detector = LangDetectDetector()
        result = detector.detect("Bonjour, comment allez-vous?")

        assert result == "fr"

    def test_detect_german(self):
        """Test detection of German text."""
        from src.translators.langdetect_detector import LangDetectDetector

        detector = LangDetectDetector()
        result = detector.detect("Guten Tag, wie geht es Ihnen?")

        assert result == "de"

    def test_detect_empty_string_raises_error(self):
        """Test that empty string raises ValueError."""
        from src.translators.langdetect_detector import LangDetectDetector

        detector = LangDetectDetector()

        with pytest.raises(ValueError, match="empty"):
            detector.detect("")

    def test_detect_none_raises_error(self):
        """Test that None raises ValueError."""
        from src.translators.langdetect_detector import LangDetectDetector

        detector = LangDetectDetector()

        with pytest.raises(ValueError):
            detector.detect(None)

    def test_detect_whitespace_only_raises_error(self):
        """Test that whitespace-only text raises ValueError."""
        from src.translators.langdetect_detector import LangDetectDetector

        detector = LangDetectDetector()

        with pytest.raises(ValueError, match="empty"):
            detector.detect("   ")

    def test_detect_very_short_text(self):
        """Test detection with very short text (single word)."""
        from src.translators.langdetect_detector import LangDetectDetector

        detector = LangDetectDetector()
        # langdetect might be unreliable with very short text
        # but should not crash
        result = detector.detect("hello")

        # Should return a valid 2-character language code
        assert isinstance(result, str)
        assert len(result) == 2

    def test_detect_longer_text(self):
        """Test detection with longer, more complex text."""
        from src.translators.langdetect_detector import LangDetectDetector

        detector = LangDetectDetector()
        long_text = """
        This is a longer piece of English text that should be very easy
        to detect. Language detection algorithms work better with more
        context and more words to analyze. This should definitely be
        detected as English without any issues.
        """
        result = detector.detect(long_text)

        assert result == "en"

    def test_detect_text_with_numbers(self):
        """Test detection of text containing numbers."""
        from src.translators.langdetect_detector import LangDetectDetector

        detector = LangDetectDetector()
        result = detector.detect("I have 5 apples and 3 oranges today.")

        assert result == "en"

    def test_detect_text_with_punctuation(self):
        """Test detection of text with lots of punctuation."""
        from src.translators.langdetect_detector import LangDetectDetector

        detector = LangDetectDetector()
        result = detector.detect("Hello! How are you? I'm doing great!!!")

        assert result == "en"

    def test_detect_portuguese(self):
        """Test detection of Portuguese text."""
        from src.translators.langdetect_detector import LangDetectDetector

        detector = LangDetectDetector()
        result = detector.detect("Olá, como você está?")

        assert result == "pt"

    def test_detect_italian(self):
        """Test detection of Italian text."""
        from src.translators.langdetect_detector import LangDetectDetector

        detector = LangDetectDetector()
        result = detector.detect("Ciao, come stai?")

        assert result == "it"

    def test_multiple_detections_are_consistent(self):
        """Test that detecting the same text multiple times gives same result."""
        from src.translators.langdetect_detector import LangDetectDetector

        detector = LangDetectDetector()
        text = "This is a test sentence in English."

        result1 = detector.detect(text)
        result2 = detector.detect(text)
        result3 = detector.detect(text)

        assert result1 == result2 == result3 == "en"

    def test_detector_is_reusable(self):
        """Test that same detector instance can be used multiple times."""
        from src.translators.langdetect_detector import LangDetectDetector

        detector = LangDetectDetector()

        result1 = detector.detect("Hello, how are you?")
        result2 = detector.detect("Hola, �c�mo est�s?")
        result3 = detector.detect("Bonjour, comment allez-vous?")

        assert result1 == "en"
        assert result2 == "es"
        assert result3 == "fr"
