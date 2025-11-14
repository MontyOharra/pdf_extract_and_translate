import os
from pathlib import Path
from typing import Tuple


class PDFFixtures:
    """Helper class for managing PDF and image test fixtures."""

    # Base fixtures directory
    FIXTURES_DIR = Path(__file__).parent / "pdfs"
    TYPED_DIR = FIXTURES_DIR / "typed"
    SCANNED_DIR = FIXTURES_DIR / "scanned"
    EXPECTED_DIR = FIXTURES_DIR / "expected_outputs"

    # Supported file extensions
    SUPPORTED_EXTENSIONS = ['.pdf', '.png', '.jpg', '.jpeg']

    @classmethod
    def get_file_path(cls, filename: str, file_type: str = "typed") -> Path:
        """
        Get the full path to a test file (PDF or image).

        Args:
            filename: Name of the file (e.g., "simple_text.pdf", "image.png")
            file_type: Type of file - "typed" or "scanned". Defaults to "typed".

        Returns:
            Path object pointing to the file.

        Raises:
            FileNotFoundError: If the file doesn't exist.
        """
        if file_type == "typed":
            file_path = cls.TYPED_DIR / filename
        elif file_type == "scanned":
            file_path = cls.SCANNED_DIR / filename
        else:
            raise ValueError(f"Invalid file_type: {file_type}. Must be 'typed' or 'scanned'.")

        if not file_path.exists():
            raise FileNotFoundError(
                f"Fixture file not found: {file_path}\n"
                f"Please create this file in the fixtures directory."
            )

        return file_path

    @classmethod
    def get_pdf_path(cls, filename: str, pdf_type: str = "typed") -> Path:
        """
        Legacy method name for backwards compatibility.
        Use get_file_path instead.
        """
        return cls.get_file_path(filename, pdf_type)

    @classmethod
    def get_expected_output(cls, filename: str) -> str:
        """
        Get the expected text output for a test file (PDF or image).

        Args:
            filename: Name of the file (e.g., "simple_text.pdf", "image.png")

        Returns:
            The expected text content as a string.

        Raises:
            FileNotFoundError: If the expected output file doesn't exist.
        """
        # Get base filename without extension
        base_name = Path(filename).stem
        txt_filename = f"{base_name}.txt"
        txt_path = cls.EXPECTED_DIR / txt_filename

        if not txt_path.exists():
            raise FileNotFoundError(
                f"Expected output file not found: {txt_path}\n"
                f"Please create a .txt file with the expected OCR output."
            )

        with open(txt_path, 'r', encoding='utf-8') as f:
            return f.read()

    @classmethod
    def get_file_and_expected(cls, filename: str, file_type: str = "typed") -> Tuple[Path, str]:
        """
        Get both the file path and expected output in one call.

        Convenience method that combines get_file_path and get_expected_output.

        Args:
            filename: Name of the file (e.g., "simple_text.pdf", "image.png")
            file_type: Type of file - "typed" or "scanned". Defaults to "typed".

        Returns:
            Tuple of (file path, expected text output)
        """
        file_path = cls.get_file_path(filename, file_type)
        expected = cls.get_expected_output(filename)
        return file_path, expected

    @classmethod
    def get_pdf_and_expected(cls, filename: str, pdf_type: str = "typed") -> Tuple[Path, str]:
        """
        Legacy method name for backwards compatibility.
        Use get_file_and_expected instead.
        """
        return cls.get_file_and_expected(filename, pdf_type)

    @classmethod
    def list_available_files(cls, file_type: str = "typed") -> list:
        """
        List all available test fixtures (PDFs and images) of a given type.

        Args:
            file_type: Type of file - "typed" or "scanned". Defaults to "typed".

        Returns:
            List of filenames available for testing.
        """
        if file_type == "typed":
            directory = cls.TYPED_DIR
        elif file_type == "scanned":
            directory = cls.SCANNED_DIR
        else:
            raise ValueError(f"Invalid file_type: {file_type}. Must be 'typed' or 'scanned'.")

        if not directory.exists():
            return []

        files = []
        for ext in cls.SUPPORTED_EXTENSIONS:
            files.extend([f.name for f in directory.glob(f"*{ext}")])
        return sorted(files)
