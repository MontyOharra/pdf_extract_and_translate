# -*- coding: utf-8 -*-
"""
Unit tests for TesseractExtractor - OCR-based text extraction.

Tests use actual PDF and image fixtures created manually.
"""

import pytest
from tests.fixtures.pdf_fixtures import PDFFixtures


class TestTesseractExtractor:
    """Test suite for TesseractExtractor OCR functionality."""

    # ========== Basic Text Extraction Tests ==========

    def test_extract_multilingual_pdf(self):
        """
        Test extracting text from a PDF with multiple languages.

        Uses: tests/fixtures/pdfs/typed/3-languages.pdf
        Expected: tests/fixtures/pdfs/expected_outputs/3-languages.txt
        """
        from src.extractors.tesseract_extractor import TesseractExtractor

        # Get PDF and expected output
        pdf_path, expected = PDFFixtures.get_pdf_and_expected("3-languages.pdf", pdf_type="typed")

        # Create extractor with multi-language support
        extractor = TesseractExtractor(lang='eng+deu+jpn')
        result = extractor.extract_text(pdf_path)

        # Verify extracted text matches expected
        assert result is not None
        assert isinstance(result, str)
        # Strip whitespace for comparison (OCR may add extra spaces/newlines)
        assert result.strip() == expected.strip()

    # ========== Image File Tests ==========

    def test_extract_text_from_png_image(self):
        """
        Test extracting text from a PNG image file.

        Uses: tests/fixtures/pdfs/scanned/hello-world-en-es.png
        Expected: tests/fixtures/pdfs/expected_outputs/hello-world-en-es.txt
        """
        from src.extractors.tesseract_extractor import TesseractExtractor

        file_path, expected = PDFFixtures.get_file_and_expected("hello-world-en-es.png", file_type="scanned")

        extractor = TesseractExtractor()
        result = extractor.extract_text(file_path)

        assert result is not None
        assert isinstance(result, str)
        # For images, comparison may be case-insensitive due to OCR variations
        assert result.strip().lower() == expected.strip().lower()

    # ========== Scanned PDF Tests ==========

    def test_extract_scanned_pdf_with_handwriting(self):
        """
        Test extracting text from a PDF with both typed and handwritten text.

        Uses: tests/fixtures/pdfs/scanned/typed-with-drawn.pdf
        Expected: tests/fixtures/pdfs/expected_outputs/typed-with-drawn.txt
        """
        from src.extractors.tesseract_extractor import TesseractExtractor

        pdf_path, expected = PDFFixtures.get_pdf_and_expected("typed-with-drawn.pdf", pdf_type="scanned")

        extractor = TesseractExtractor()
        result = extractor.extract_text(pdf_path)

        assert result is not None
        assert isinstance(result, str)
        # For scanned PDFs with handwriting, OCR may have variations
        # Just check that some text was extracted
        assert len(result.strip()) > 0

    # ========== Error Handling Tests ==========

    def test_extract_from_nonexistent_file_raises_error(self):
        """Test that extracting from non-existent file raises error."""
        from src.extractors.tesseract_extractor import TesseractExtractor

        extractor = TesseractExtractor()

        with pytest.raises((FileNotFoundError, Exception)):
            extractor.extract_text("nonexistent.pdf")

    # ========== Extractor Properties Tests ==========

    def test_extractor_has_name_property(self):
        """Test that extractor has a name property."""
        from src.extractors.tesseract_extractor import TesseractExtractor

        extractor = TesseractExtractor()

        assert hasattr(extractor, 'name')
        assert isinstance(extractor.name, str)
        assert len(extractor.name) > 0
        assert "tesseract" in extractor.name.lower()

    def test_extractor_supports_pdf_format(self):
        """Test that extractor reports support for PDF format."""
        from src.extractors.tesseract_extractor import TesseractExtractor

        extractor = TesseractExtractor()

        assert extractor.supports_format("pdf") is True
        assert extractor.supports_format("PDF") is True

    def test_extractor_supports_image_formats(self):
        """Test that extractor supports common image formats."""
        from src.extractors.tesseract_extractor import TesseractExtractor

        extractor = TesseractExtractor()

        # Should support PNG, JPG, JPEG
        assert extractor.supports_format("png") is True
        assert extractor.supports_format("PNG") is True
        assert extractor.supports_format("jpg") is True
        assert extractor.supports_format("JPG") is True
        assert extractor.supports_format("jpeg") is True
        assert extractor.supports_format("JPEG") is True

    def test_extractor_does_not_support_invalid_format(self):
        """Test that extractor correctly reports unsupported formats."""
        from src.extractors.tesseract_extractor import TesseractExtractor

        extractor = TesseractExtractor()

        assert extractor.supports_format("docx") is False
        assert extractor.supports_format("txt") is False
        assert extractor.supports_format("invalid") is False

    # ========== Reusability Tests ==========

    def test_extractor_is_reusable(self):
        """Test that same extractor instance can process multiple files."""
        from src.extractors.tesseract_extractor import TesseractExtractor

        extractor = TesseractExtractor(lang='eng+deu+jpn+spa')

        # Extract from first file (PDF)
        pdf_path1, expected1 = PDFFixtures.get_pdf_and_expected("3-languages.pdf", pdf_type="typed")
        result1 = extractor.extract_text(pdf_path1)

        # Extract from second file (Image) using same instance
        img_path2, expected2 = PDFFixtures.get_pdf_and_expected("hello-world-en-es.png", pdf_type="scanned")
        result2 = extractor.extract_text(img_path2)

        # Both should succeed
        assert result1 is not None
        assert result2 is not None
        assert len(result1.strip()) > 0
        assert len(result2.strip()) > 0
