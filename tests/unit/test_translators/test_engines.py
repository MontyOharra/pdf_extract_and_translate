# -*- coding: utf-8 -*-
"""
Unit tests for translator engine implementations.

Following TDD approach:
1. Write tests first (RED - tests fail)
2. Implement to pass tests (GREEN)
3. Refactor while keeping tests passing
"""

import pytest


class TestDeepTranslatorWrapper:
    """Test suite for DeepTranslatorWrapper implementation."""

    # ========== Backend Selection Tests ==========

    def test_create_with_google_backend(self):
        """Test creating translator with Google backend."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')

        assert translator is not None
        assert translator.backend == 'google'

    def test_create_with_default_backend(self):
        """Test that default backend is google when not specified."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper()

        assert translator.backend == 'google'

    def test_create_with_invalid_backend_raises_error(self):
        """Test that invalid backend raises ValueError."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        with pytest.raises(ValueError, match="Unsupported backend"):
            DeepTranslatorWrapper(backend='invalid_backend')

    def test_create_with_empty_backend_raises_error(self):
        """Test that empty backend string raises ValueError."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        with pytest.raises(ValueError, match="Unsupported backend"):
            DeepTranslatorWrapper(backend='')

    # ========== Name Property Tests ==========

    def test_name_property_returns_string(self):
        """Test that name property returns a non-empty string."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')

        assert isinstance(translator.name, str)
        assert len(translator.name) > 0

    def test_name_reflects_google_backend(self):
        """Test that name reflects Google backend."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')

        assert 'google' in translator.name.lower()

    # ========== Basic Translation Tests ==========

    def test_translate_english_to_spanish(self):
        """Test translating from English to Spanish."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')
        result = translator.translate("Hello", "en", "es")

        # Should contain "hola" (case insensitive)
        assert "hola" in result.lower()

    def test_translate_english_to_french(self):
        """Test translating from English to French."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')
        result = translator.translate("Hello", "en", "fr")

        # Should contain "bonjour" or "salut"
        result_lower = result.lower()
        assert "bonjour" in result_lower or "salut" in result_lower

    def test_translate_spanish_to_english(self):
        """Test translating from Spanish to English."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')
        result = translator.translate("Hola", "es", "en")

        # Should contain "hello" or "hi"
        result_lower = result.lower()
        assert "hello" in result_lower or "hi" in result_lower

    def test_translate_english_to_german(self):
        """Test translating from English to German."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')
        result = translator.translate("Good morning", "en", "de")

        # Should contain "guten" or "morgen"
        result_lower = result.lower()
        assert "guten" in result_lower or "morgen" in result_lower

    # ========== Error Handling Tests ==========

    def test_translate_empty_string_raises_error(self):
        """Test that empty string raises ValueError."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')

        with pytest.raises(ValueError, match="empty"):
            translator.translate("", "en", "es")

    def test_translate_none_raises_error(self):
        """Test that None text raises ValueError."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')

        with pytest.raises(ValueError):
            translator.translate(None, "en", "es")

    def test_translate_whitespace_only_raises_error(self):
        """Test that whitespace-only text raises ValueError."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')

        with pytest.raises(ValueError, match="empty"):
            translator.translate("   ", "en", "es")

    def test_translate_invalid_source_language_raises_error(self):
        """Test that invalid source language code raises error."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')

        with pytest.raises((ValueError, Exception)):
            translator.translate("Hello", "invalid_lang", "es")

    def test_translate_invalid_target_language_raises_error(self):
        """Test that invalid target language code raises error."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')

        with pytest.raises((ValueError, Exception)):
            translator.translate("Hello", "en", "invalid_lang")

    def test_translate_empty_source_language_raises_error(self):
        """Test that empty source language raises error."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')

        with pytest.raises((ValueError, Exception)):
            translator.translate("Hello", "", "es")

    def test_translate_empty_target_language_raises_error(self):
        """Test that empty target language raises error."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')

        with pytest.raises((ValueError, Exception)):
            translator.translate("Hello", "en", "")

    # ========== Longer Text Tests ==========

    def test_translate_longer_text(self):
        """Test translation of longer, multi-sentence text."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')
        long_text = "Hello, how are you? I hope you are having a wonderful day. The weather is nice today."
        result = translator.translate(long_text, "en", "es")

        # Should return translated text
        assert isinstance(result, str)
        assert len(result) > 0
        # Should be roughly similar length (translations vary but shouldn't be drastically different)
        assert len(result) > len(long_text) * 0.5

    def test_translate_text_with_punctuation(self):
        """Test translation preserves or handles punctuation appropriately."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')
        result = translator.translate("Hello! How are you?", "en", "es")

        # Should return translated text with some punctuation
        assert isinstance(result, str)
        assert len(result) > 0

    def test_translate_text_with_numbers(self):
        """Test translation of text containing numbers."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')
        result = translator.translate("I have 5 apples and 3 oranges.", "en", "es")

        # Numbers should be preserved
        assert "5" in result or "cinco" in result.lower()
        assert "3" in result or "tres" in result.lower()

    def test_translate_sentence_with_special_characters(self):
        """Test translation of text with special characters."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')
        result = translator.translate("Hello, it's a beautiful day!", "en", "es")

        assert isinstance(result, str)
        assert len(result) > 0

    # ========== Language Support Tests ==========

    def test_supports_common_languages(self):
        """Test that common languages are supported."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')

        # These should work without errors
        common_langs = ['en', 'es', 'fr', 'de', 'it', 'pt']
        for lang in common_langs:
            assert translator.supports_language(lang) is True

    def test_supports_language_with_invalid_code_returns_false(self):
        """Test that invalid language codes return False."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')

        assert translator.supports_language('invalid_code') is False
        assert translator.supports_language('xyz') is False
        assert translator.supports_language('') is False

    # ========== Reusability Tests ==========

    def test_translator_is_reusable(self):
        """Test that same translator instance can be used multiple times."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')

        result1 = translator.translate("Hello", "en", "es")
        result2 = translator.translate("Good morning", "en", "fr")
        result3 = translator.translate("Thank you", "en", "de")

        # All should return valid results
        assert "hola" in result1.lower()
        assert len(result2) > 0
        assert len(result3) > 0

    def test_multiple_translations_same_text(self):
        """Test that translating same text multiple times gives consistent results."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')
        text = "Hello, how are you?"

        result1 = translator.translate(text, "en", "es")
        result2 = translator.translate(text, "en", "es")
        result3 = translator.translate(text, "en", "es")

        # Results should be consistent
        assert result1 == result2 == result3

    # ========== Auto-detect Source Language Tests ==========

    def test_translate_with_auto_detect_source_language(self):
        """Test translation with 'auto' as source language for auto-detection."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')
        # Use 'auto' to let deep-translator auto-detect the source language
        result = translator.translate("Hello", "auto", "es")

        assert "hola" in result.lower()

    # ========== Edge Cases ==========

    def test_translate_same_source_and_target_language(self):
        """Test translating when source and target languages are the same."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')
        result = translator.translate("Hello", "en", "en")

        # Should return the same or very similar text
        assert "hello" in result.lower()

    def test_translate_single_word(self):
        """Test translation of a single word."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')
        result = translator.translate("cat", "en", "es")

        assert "gato" in result.lower()

    def test_translate_very_short_text(self):
        """Test translation of very short text (2-3 characters)."""
        from src.translators.deep_translator_wrapper import DeepTranslatorWrapper

        translator = DeepTranslatorWrapper(backend='google')
        result = translator.translate("Hi", "en", "es")

        # Should return some valid Spanish greeting
        assert isinstance(result, str)
        assert len(result) > 0
