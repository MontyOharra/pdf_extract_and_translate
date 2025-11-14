from pathlib import Path
from typing import Union, Optional
import os
from dotenv import load_dotenv

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from src.extractors.base import TextExtractor


class AzureOCRExtractor(TextExtractor):
    """
    Text extractor using Azure Document Intelligence (prebuilt-read model).

    Authentication:
        Credentials can be provided via constructor or environment variables:
        - AZURE_DOCUMENT_INTELLIGENCE_KEY: Your API key
        - AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT: Your endpoint URL
    """

    # Supported file formats

    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None
    ):
        """
        Initialize the Azure Document Intelligence extractor.

        Args:
            api_key: Azure Document Intelligence API key. If not provided, reads from
                    AZURE_DOCUMENT_INTELLIGENCE_KEY environment variable.
            endpoint: Azure Document Intelligence endpoint URL. If not provided, reads
                     from AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT environment variable.
        """

        self.SUPPORTED_FORMATS = {'pdf', 'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'tif'}

        load_dotenv()

        self.api_key = api_key or os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        self.endpoint = endpoint or os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")

        # Validate credentials
        if not self.api_key or not self.endpoint:
            raise ValueError(
                "Azure credentials not provided. Either pass api_key and endpoint "
                "to constructor, or set AZURE_DOCUMENT_INTELLIGENCE_KEY."
            )

        # Create Azure Document Intelligence client
        self._client = DocumentIntelligenceClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.api_key)
        )

    @property
    def name(self) -> str:
        return "Azure Document Intelligence OCR"

    def supports_format(self, file_format: str) -> bool:
        if not file_format or not isinstance(file_format, str):
            return False

        return file_format.lower() in self.SUPPORTED_FORMATS

    def extract_text(self, input_data: Union[str, Path]) -> str:
        """
        Extract text from a PDF or image file using Azure Document Intelligence.

        Args:
            input_data: Path to the file (PDF or image) to extract text from.
                       Can be a string path or pathlib.Path object.

        Returns:
            The extracted text as a string. Multiple lines are concatenated
            with newlines.
        """
        file_path = Path(input_data) if isinstance(input_data, str) else input_data

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        file_ext = file_path.suffix.lower().lstrip('.')

        if not self.supports_format(file_ext):
            raise ValueError(
                f"Unsupported file format: {file_ext}. "
                f"Supported formats: {', '.join(self.SUPPORTED_FORMATS)}"
            )

        return self._extract_with_azure_document_intelligence(file_path)

    def _extract_with_azure_document_intelligence(self, file_path: Path) -> str:
        """
        Extract text using Azure Document Intelligence prebuilt-read model.

        Args:
            file_path: Path to the file to process.

        Returns:
            Extracted text from the file.
        """
        try:
            # Open file in binary mode and submit to Azure Document Intelligence
            with open(file_path, "rb") as document_file:
                poller = self._client.begin_analyze_document(
                    model_id="prebuilt-read",
                    body=document_file,
                    content_type="application/pdf"
                )

                # Wait for result
                result = poller.result()

            # Extract text from result
            return self._extract_text_from_result(result)

        except Exception as e:
            raise Exception(
                f"Failed to extract text with Azure Document Intelligence: {str(e)}"
            ) from e

    def _extract_text_from_result(self, result) -> str:
        """
        Extract text lines from Azure Document Intelligence result.

        Args:
            result: The analysis result from Azure Document Intelligence.

        Returns:
            Extracted text with lines joined by newlines.
        """
        extracted_lines = []

        # Iterate through pages
        if hasattr(result, 'pages') and result.pages:
            for page in result.pages:
                # Extract each line of text from the page
                if hasattr(page, 'lines') and page.lines:
                    for line in page.lines:
                        extracted_lines.append(line.content)

        # Join all lines with newlines
        return '\n'.join(extracted_lines)
