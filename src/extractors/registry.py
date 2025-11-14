# -*- coding: utf-8 -*-
"""
Extractor registry for managing available text extractors.
"""

from typing import Dict, Type, List
from src.extractors.base import TextExtractor


class TextExtractorRegistry:
    """Registry for available text extractors."""

    def __init__(self):
        self._extractors: Dict[str, Type[TextExtractor]] = {}

    def register(self, name: str, extractor_class: Type[TextExtractor]):
        """
        Register an extractor with a display name.

        Args:
            name: Display name for the extractor
            extractor_class: The extractor class to register
        """
        self._extractors[name] = extractor_class

    def get_available_extractors(self) -> List[str]:
        """
        Get list of available extractor names.

        Returns:
            List of registered extractor display names
        """
        return list(self._extractors.keys())

    def create_extractor(self, name: str) -> TextExtractor:
        """
        Create an instance of the specified extractor.

        Args:
            name: Display name of the extractor to create

        Returns:
            Instance of the requested extractor
        """
        if name not in self._extractors:
            raise ValueError(f"Unknown extractor: {name}")

        extractor_class = self._extractors[name]

        # Try to instantiate - some may need credentials
        try:
            return extractor_class()
        except ValueError as e:
            # If credentials are missing, inform user
            print(f"\nError: {str(e)}")
            print("Please ensure credentials are set in .env file or environment variables.")
            raise
