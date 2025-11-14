# -*- coding: utf-8 -*-
"""
Interactive prompts for the CLI.
"""

import questionary
from pathlib import Path

from src.extractors.registry import TextExtractorRegistry


def select_extractor(registry: TextExtractorRegistry) -> str:
    """
    Prompt user to select text extractor.

    Args:
        registry: TextExtractorRegistry containing available extractors

    Returns:
        Name of selected extractor
    """
    extractors = registry.get_available_extractors()

    extractor = questionary.select(
        "Select text extraction method:",
        choices=extractors
    ).ask()

    return extractor


def select_target_language() -> str:
    """
    Prompt user to select target language for translation.

    Returns:
        Language code (e.g., 'en', 'es', 'fr')
    """
    languages = [
        questionary.Choice("English", value="en"),
        questionary.Choice("Spanish", value="es"),
        questionary.Choice("French", value="fr"),
        questionary.Choice("German", value="de"),
        questionary.Choice("Italian", value="it"),
        questionary.Choice("Chinese (Simplified)", value="zh-CN"),
        questionary.Choice("Japanese", value="ja"),
        questionary.Choice("Arabic", value="ar"),
        questionary.Choice("Hindi", value="hi"),
        questionary.Choice("Other", value="other"),
    ]

    language = questionary.select(
        "Select target language:",
        choices=languages
    ).ask()

    # If user selected "other", prompt for custom language code
    if language == "other":
        language = questionary.text(
            "Enter language code (e.g., 'hi' for Hindi, 'tr' for Turkish):",
            validate=lambda text: len(text) > 0 or "Language code cannot be empty"
        ).ask()

    return language


def select_output_file(input_file: str) -> str:
    """
    Prompt user to specify output file name.

    Args:
        input_file: Path to input file (used to suggest output name)

    Returns:
        Path to output file
    """
    # Suggest output filename based on input
    input_path = Path(input_file)
    suggested_output = input_path.stem + "_output.txt"

    output_file = questionary.text(
        "Enter output filename:",
        default=suggested_output
    ).ask()

    return output_file
