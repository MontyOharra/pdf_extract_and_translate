# -*- coding: utf-8 -*-
"""
Unit tests for AzureOCRExtractor - Azure Document Intelligence OCR-based text extraction.

NOTE: These tests require Azure credentials to be set in environment variables:
- AZURE_DOCUMENT_INTELLIGENCE_KEY: Your Azure Document Intelligence API key
- AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT: Your Azure Document Intelligence endpoint URL

Tests will be skipped if credentials are not available.
"""

import pytest
import os
from dotenv import load_dotenv
from tests.fixtures.pdf_fixtures import PDFFixtures

# Load environment variables from .env file before checking credentials
load_dotenv()

# Check if Azure credentials are available
AZURE_CREDENTIALS_AVAILABLE = (
    os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY") is not None and
    os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT") is not None
)

skip_if_no_azure = pytest.mark.skipif(
    not AZURE_CREDENTIALS_AVAILABLE,
    reason="Azure credentials not found in environment variables"
)


class TestAzureOCRExtractor:
    """Test suite for AzureOCRExtractor functionality."""

    def test_extractor_can_be_created_with_credentials(self):
        """Test that extractor can be instantiated with explicit credentials."""
        from src.extractors.azure_ocr_extractor import AzureOCRExtractor

        extractor = AzureOCRExtractor(
            api_key="test_key",
            endpoint="https://test.cognitiveservices.azure.com/"
        )

        assert extractor is not None

    @skip_if_no_azure
    def test_extract_multilingual_pdf(self):
        """
        Test extracting text from a PDF with multiple languages using Azure OCR.

        Uses: tests/fixtures/pdfs/typed/3-languages.pdf
        """
        from src.extractors.azure_ocr_extractor import AzureOCRExtractor

        pdf_path, expected = PDFFixtures.get_pdf_and_expected("3-languages.pdf", pdf_type="typed")

        extractor = AzureOCRExtractor()
        result = extractor.extract_text(pdf_path)

        assert result is not None
        assert isinstance(result, str)
        assert len(result.strip()) > 0

    @skip_if_no_azure
    def test_extract_text_from_png_image(self):
        """
        Test extracting text from a PNG image file using Azure OCR.

        Uses: tests/fixtures/pdfs/scanned/hello-world-en-es.png
        """
        from src.extractors.azure_ocr_extractor import AzureOCRExtractor

        file_path, expected = PDFFixtures.get_file_and_expected("hello-world-en-es.png", file_type="scanned")

        extractor = AzureOCRExtractor()
        result = extractor.extract_text(file_path)

        assert result is not None
        assert isinstance(result, str)
        assert len(result.strip()) > 0

    @skip_if_no_azure
    def test_extract_scanned_pdf_with_handwriting(self):
        """
        Test extracting text from a PDF with both typed and handwritten text.

        Uses: tests/fixtures/pdfs/scanned/typed-with-drawn.pdf
        """
        from src.extractors.azure_ocr_extractor import AzureOCRExtractor

        pdf_path, expected = PDFFixtures.get_pdf_and_expected("typed-with-drawn.pdf", pdf_type="scanned")

        extractor = AzureOCRExtractor()
        result = extractor.extract_text(pdf_path)

        assert result is not None
        assert isinstance(result, str)
        assert len(result.strip()) > 0

    def test_extract_from_nonexistent_file_raises_error(self):
        """Test that extracting from non-existent file raises error."""
        from src.extractors.azure_ocr_extractor import AzureOCRExtractor

        extractor = AzureOCRExtractor(
            api_key="test_key",
            endpoint="https://test.cognitiveservices.azure.com/"
        )

        with pytest.raises((FileNotFoundError, Exception)):
            extractor.extract_text("nonexistent.pdf")

    @skip_if_no_azure
    def test_extractor_is_reusable(self):
        """Test that same extractor instance can process multiple files."""
        from src.extractors.azure_ocr_extractor import AzureOCRExtractor

        extractor = AzureOCRExtractor()

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
