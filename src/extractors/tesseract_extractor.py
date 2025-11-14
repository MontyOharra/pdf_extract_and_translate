from pathlib import Path
from typing import Union
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from src.extractors.base import TextExtractor


class TesseractExtractor(TextExtractor):
    """
    Text extractor using Tesseract OCR.
    """

    # Supported file formats

    def __init__(self, dpi: int = 300, lang: str = 'eng'):
        """
        Initialize the Tesseract extractor.

        Args:
            dpi: DPI (dots per inch) for PDF to image conversion.
            lang: Language(s) for OCR. Default: 'eng' (English).
        """
        self.SUPPORTED_FORMATS = {'pdf', 'png', 'jpg', 'jpeg'}
        self.dpi = dpi
        self.lang = lang

    @property
    def name(self) -> str:
        return "Tesseract OCR"

    def supports_format(self, file_format: str) -> bool:
        if not file_format or not isinstance(file_format, str):
            return False

        return file_format.lower() in self.SUPPORTED_FORMATS

    def extract_text(self, input_data: Union[str, Path]) -> str:
        """
        Extract text from a PDF or image file using Tesseract OCR.

        This method handles both PDFs and images:
        - For PDFs: Converts each page to an image, then applies OCR
        - For images: Applies OCR directly

        Args:
            input_data: Path to the file (PDF or image) to extract text from.
                       Can be a string path or pathlib.Path object.

        Returns:
            The extracted text as a string. Multiple pages/images are
            concatenated with newlines.
        """
        # Convert to Path object
        file_path = Path(input_data) if isinstance(input_data, str) else input_data

        # Check if file exists
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Get file extension
        file_ext = file_path.suffix.lower().lstrip('.')

        # Check if format is supported
        if not self.supports_format(file_ext):
            raise ValueError(
                f"Unsupported file format: {file_ext}. "
                f"Supported formats: {', '.join(self.SUPPORTED_FORMATS)}"
            )

        # Extract text based on file type
        if file_ext == 'pdf':
            return self._extract_from_pdf(file_path)
        else:
            # Image file (png, jpg, jpeg)
            return self._extract_from_image(file_path)

    def _extract_from_pdf(self, pdf_path: Path) -> str:
        """
        Extract text from a PDF file.

        Converts each page to an image and applies OCR.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            Extracted text from all pages, concatenated with newlines.
        """
        try:
            # Convert PDF to images (one image per page)
            images = convert_from_path(
                str(pdf_path),
                dpi=self.dpi
            )

            # Extract text from each page
            extracted_texts = []
            for image in images:
                text = self._ocr_image(image)
                if text.strip():  # Only add non-empty text
                    extracted_texts.append(text)

            # Combine all pages
            return '\n'.join(extracted_texts)

        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}") from e

    def _extract_from_image(self, image_path: Path) -> str:
        """
        Extract text from an image file.

        Args:
            image_path: Path to the image file (PNG, JPG, JPEG).

        Returns:
            Extracted text from the image.
        """
        try:
            # Open image
            image = Image.open(image_path)

            # Extract text using OCR
            text = self._ocr_image(image)

            return text

        except Exception as e:
            raise Exception(f"Failed to extract text from image: {str(e)}") from e

    def _ocr_image(self, image: Image.Image) -> str:
        """
        Perform OCR on a PIL Image object.

        Args:
            image: PIL Image object to perform OCR on.

        Returns:
            Extracted text from the image.
        """
        # Configure Tesseract with language setting
        custom_config = f'-l {self.lang}'

        text = pytesseract.image_to_string(image, config=custom_config)

        return text.strip()
