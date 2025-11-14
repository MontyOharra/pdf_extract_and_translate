# -*- coding: utf-8 -*-
"""
Unit tests for TextExtractor abstract base class.

Following TDD approach:
1. Write tests first (RED - tests fail)
2. Implement base class (GREEN - tests pass)
3. Refactor while keeping tests passing
"""

import pytest
from abc import ABC


class TestTextExtractorBaseClass:
    """Test suite for TextExtractor abstract base class."""

    def test_textextractor_is_abstract(self):
        """Test that TextExtractor cannot be instantiated directly."""
        from src.extractors.base import TextExtractor

        # Should not be able to create instance of abstract class
        with pytest.raises(TypeError):
            TextExtractor()

    def test_textextractor_requires_extract_text_method(self):
        """Test that subclasses must implement extract_text method."""
        from src.extractors.base import TextExtractor

        # Create incomplete subclass missing extract_text
        class IncompleteExtractor(TextExtractor):
            @property
            def name(self):
                return "Incomplete"

            def supports_format(self, file_format):
                return True

        # Should not be able to instantiate without extract_text
        with pytest.raises(TypeError):
            IncompleteExtractor()

    def test_textextractor_requires_name_property(self):
        """Test that subclasses must implement name property."""
        from src.extractors.base import TextExtractor

        # Create incomplete subclass missing name
        class IncompleteExtractor(TextExtractor):
            def extract_text(self, input_data):
                return "text"

            def supports_format(self, file_format):
                return True

        # Should not be able to instantiate without name
        with pytest.raises(TypeError):
            IncompleteExtractor()

    def test_textextractor_requires_supports_format_method(self):
        """Test that subclasses must implement supports_format method."""
        from src.extractors.base import TextExtractor

        # Create incomplete subclass missing supports_format
        class IncompleteExtractor(TextExtractor):
            @property
            def name(self):
                return "Incomplete"

            def extract_text(self, input_data):
                return "text"

        # Should not be able to instantiate without supports_format
        with pytest.raises(TypeError):
            IncompleteExtractor()

    def test_textextractor_can_be_subclassed_with_all_methods(self):
        """Test that complete subclass can be instantiated."""
        from src.extractors.base import TextExtractor

        # Create complete subclass
        class CompleteExtractor(TextExtractor):
            @property
            def name(self):
                return "Test Extractor"

            def extract_text(self, input_data):
                return "extracted text"

            def supports_format(self, file_format):
                return file_format.lower() == "pdf"

        # Should be able to instantiate complete implementation
        extractor = CompleteExtractor()
        assert extractor is not None
        assert extractor.name == "Test Extractor"
        assert extractor.extract_text("test.pdf") == "extracted text"
        assert extractor.supports_format("pdf") is True
        assert extractor.supports_format("docx") is False

    def test_textextractor_inherits_from_abc(self):
        """Test that TextExtractor inherits from ABC."""
        from src.extractors.base import TextExtractor

        # Should inherit from ABC
        assert issubclass(TextExtractor, ABC)

    def test_textextractor_extract_text_signature(self):
        """Test that extract_text has correct signature."""
        from src.extractors.base import TextExtractor
        import inspect

        # Get the extract_text method
        method = getattr(TextExtractor, 'extract_text')

        # Should be abstract
        assert getattr(method, '__isabstractmethod__', False) is True

    def test_textextractor_name_signature(self):
        """Test that name is an abstract property."""
        from src.extractors.base import TextExtractor
        import inspect

        # Get the name property
        prop = getattr(TextExtractor, 'name')

        # Should be a property
        assert isinstance(prop, property)

        # Should be abstract
        assert getattr(prop.fget, '__isabstractmethod__', False) is True

    def test_textextractor_supports_format_signature(self):
        """Test that supports_format has correct signature."""
        from src.extractors.base import TextExtractor
        import inspect

        # Get the supports_format method
        method = getattr(TextExtractor, 'supports_format')

        # Should be abstract
        assert getattr(method, '__isabstractmethod__', False) is True
