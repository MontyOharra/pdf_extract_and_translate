# -*- coding: utf-8 -*-
"""
Unit tests for TranslationManager - unified translation with auto-detection.

Following TDD approach:
1. Write tests first (RED - tests fail)
2. Implement to pass tests (GREEN)
3. Refactor while keeping tests passing
"""

import pytest


class TestTranslationManager:
    """Test suite for TranslationManager unified translation functionality."""

    # ========== Basic Auto-Translation Tests ==========

    def test_auto_translate_english_to_spanish(self):
        """Test auto-translating English text to Spanish."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()
        result = manager.auto_translate("Hello, how are you?", target_lang="es")

        # Should return Spanish text
        assert isinstance(result, str)
        assert len(result) > 0
        assert "hola" in result.lower() or "como" in result.lower()

    def test_auto_translate_spanish_to_english(self):
        """Test auto-translating Spanish text to English."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()
        result = manager.auto_translate("Hola, como estas?", target_lang="en")

        # Should return English text
        assert isinstance(result, str)
        assert len(result) > 0
        assert "hello" in result.lower() or "how" in result.lower()

    def test_auto_translate_french_to_german(self):
        """Test auto-translating French text to German."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()
        result = manager.auto_translate("Bonjour, comment allez-vous?", target_lang="de")

        # Should return German text
        assert isinstance(result, str)
        assert len(result) > 0

    def test_auto_translate_german_to_french(self):
        """Test auto-translating German text to French."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()
        result = manager.auto_translate("Guten Tag, wie geht es Ihnen?", target_lang="fr")

        # Should return French text
        assert isinstance(result, str)
        assert len(result) > 0

    def test_auto_translate_detects_source_language_correctly(self):
        """Test that source language is correctly auto-detected."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()

        # English text should be detected and translated to Spanish
        english_text = "Good morning, I hope you are having a wonderful day."
        result = manager.auto_translate(english_text, target_lang="es")

        # Result should be in Spanish
        assert isinstance(result, str)
        assert len(result) > 0
        # Should contain Spanish words
        result_lower = result.lower()
        assert any(word in result_lower for word in ["buenos", "buenas", "dia", "espero", "tengas", "buen"])

    # ========== Error Handling Tests ==========

    def test_auto_translate_empty_string_raises_error(self):
        """Test that empty string raises ValueError."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()

        with pytest.raises(ValueError, match="empty"):
            manager.auto_translate("", target_lang="es")

    def test_auto_translate_none_raises_error(self):
        """Test that None text raises ValueError."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()

        with pytest.raises(ValueError):
            manager.auto_translate(None, target_lang="es")

    def test_auto_translate_whitespace_only_raises_error(self):
        """Test that whitespace-only text raises ValueError."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()

        with pytest.raises(ValueError, match="empty"):
            manager.auto_translate("   ", target_lang="es")

    def test_auto_translate_invalid_target_language_raises_error(self):
        """Test that invalid target language raises error."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()

        with pytest.raises((ValueError, Exception)):
            manager.auto_translate("Hello", target_lang="invalid_lang")

    def test_auto_translate_empty_target_language_raises_error(self):
        """Test that empty target language raises error."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()

        with pytest.raises(ValueError):
            manager.auto_translate("Hello", target_lang="")

    def test_auto_translate_none_target_language_raises_error(self):
        """Test that None target language raises error."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()

        with pytest.raises(ValueError):
            manager.auto_translate("Hello", target_lang=None)

    # ========== Text Variation Tests ==========

    def test_auto_translate_longer_text(self):
        """Test auto-translation of longer, multi-sentence text."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()
        long_text = """
        Hello, my name is John. I am writing to you today to discuss an important matter.
        I hope this message finds you well. Please let me know your thoughts on this topic.
        Thank you for your time and consideration.
        """
        result = manager.auto_translate(long_text, target_lang="es")

        # Should return translated text
        assert isinstance(result, str)
        assert len(result) > 0
        # Should be roughly similar length
        assert len(result) > len(long_text) * 0.5

    def test_auto_translate_text_with_punctuation(self):
        """Test auto-translation preserves or handles punctuation appropriately."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()
        result = manager.auto_translate("Hello! How are you?", target_lang="fr")

        # Should return translated text
        assert isinstance(result, str)
        assert len(result) > 0

    def test_auto_translate_text_with_numbers(self):
        """Test auto-translation of text containing numbers."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()
        result = manager.auto_translate("I have 5 apples and 3 oranges.", target_lang="es")

        # Should contain numbers or Spanish number words
        assert isinstance(result, str)
        assert "5" in result or "cinco" in result.lower()
        assert "3" in result or "tres" in result.lower()

    def test_auto_translate_single_word(self):
        """Test auto-translation of a single word."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()
        result = manager.auto_translate("Hello", target_lang="es")

        # Should return Spanish translation
        assert "hola" in result.lower()

    def test_auto_translate_short_phrase(self):
        """Test auto-translation of a short phrase."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()
        result = manager.auto_translate("Good morning", target_lang="fr")

        # Should return French translation
        assert isinstance(result, str)
        assert "bonjour" in result.lower() or "matin" in result.lower()

    # ========== Edge Cases ==========

    def test_auto_translate_same_source_and_target_language(self):
        """Test auto-translation when detected language matches target language."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()
        # English text, translating to English
        result = manager.auto_translate("Hello, how are you?", target_lang="en")

        # Should handle gracefully (might return same text or translate anyway)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_auto_translate_mixed_language_text(self):
        """Test auto-translation with mixed language text (detects primary language)."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()
        # Mostly English with one Spanish word
        mixed_text = "Hello, my name is Juan and I live in Madrid."
        result = manager.auto_translate(mixed_text, target_lang="es")

        # Should still work (detect English as primary)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_auto_translate_text_with_special_characters(self):
        """Test auto-translation with special characters."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()
        result = manager.auto_translate("Hello, this is a test!", target_lang="es")

        # Should handle special characters
        assert isinstance(result, str)
        assert len(result) > 0


    # ========== Language Detection Integration Tests ==========

    def test_auto_translate_portuguese_correctly_detected(self):
        """Test that Portuguese is correctly detected and translated."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()
        result = manager.auto_translate("Ola, como voce esta?", target_lang="en")

        # Should detect Portuguese and translate to English
        assert isinstance(result, str)
        assert "hello" in result.lower() or "hi" in result.lower()

    def test_auto_translate_italian_correctly_detected(self):
        """Test that Italian is correctly detected and translated."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()
        result = manager.auto_translate("Ciao, come stai?", target_lang="en")

        # Should detect Italian and translate to English
        assert isinstance(result, str)
        assert "hello" in result.lower() or "hi" in result.lower() or "how" in result.lower()

    def test_auto_translate_detects_various_languages(self):
        """Test that manager can detect and translate from various source languages."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()

        # Test multiple source languages, all translating to English
        test_cases = [
            ("Hello", "en"),  # English
            ("Hola", "es"),   # Spanish
            ("Bonjour", "fr"), # French
            ("Guten Tag", "de"), # German
            ("Ciao", "it"),   # Italian
        ]

        for text, _ in test_cases:
            result = manager.auto_translate(text, target_lang="en")
            assert isinstance(result, str)
            assert len(result) > 0

    # ========== Return Value Tests ==========

    def test_auto_translate_returns_string(self):
        """Test that auto_translate always returns a string."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()
        result = manager.auto_translate("Hello world", target_lang="es")

        assert isinstance(result, str)

    def test_auto_translate_returns_non_empty_string(self):
        """Test that auto_translate returns non-empty string for valid input."""
        from src.translators.manager import TranslationManager

        manager = TranslationManager()
        result = manager.auto_translate("Test", target_lang="fr")

        assert len(result) > 0
