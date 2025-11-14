# -*- coding: utf-8 -*-
"""
Main CLI runner for PDF Extract and Translate.
"""

import sys

from src.extractors.registry import TextExtractorRegistry
from src.extractors.tesseract_extractor import TesseractExtractor
from src.extractors.azure_ocr_extractor import AzureOCRExtractor
from src.translators.manager import TranslationManager
from src.cli.prompts import (
    select_extractor,
    select_target_language,
    select_output_file,
)
from src.cli.file_picker import pick_file

allowed_extensions = [
    '.pdf', '.png', '.jpg', '.jpeg'
]


def setup_extractors():
    """
    Setup and register all available extractors.

    Returns:
        TextExtractorRegistry with all available extractors registered
    """
    registry = TextExtractorRegistry()

    # Always available
    registry.register("Tesseract OCR (Local)", TesseractExtractor)

    # Optional - requires credentials
    registry.register("Azure Document Intelligence (Cloud)", AzureOCRExtractor)

    return registry


def run_cli():
    """Run the interactive CLI."""
    try:
        # Setup
        registry = setup_extractors()

        # Welcome message
        print("\n" + "="*60)
        print("  PDF Extract and Translate")
        print("="*60 + "\n")

        # Step 1: Select input file
        input_file = pick_file(allowed_extensions)
        if not input_file:
            print("\nNo file selected. Exiting.")
            return

        print(f"\nSelected: {input_file}")

        # Step 2: Select extractor
        extractor_name = select_extractor(registry)
        if not extractor_name:
            print("\nNo extractor selected. Exiting.")
            return

        print(f"\nUsing: {extractor_name}")

        # Create extractor instance
        try:
            extractor = registry.create_extractor(extractor_name)
        except (ValueError, Exception) as e:
            print(f"\nFailed to initialize extractor: {e}")
            return

        # Step 3: Extract text
        print("\nExtracting text from document...")
        try:
            extracted_text = extractor.extract_text(input_file)
        except Exception as e:
            print(f"\nExtraction failed: {e}")
            return

        target_lang = select_target_language()
        if not target_lang:
            print("\nNo language selected. Skipping translation.")
            translated_text = extracted_text
        else:
            # Step 6: Translate
            print(f"\nTranslating to {target_lang.upper()}...")
            try:
                manager = TranslationManager()
                translated_text = manager.auto_translate(extracted_text, target_lang)
                print(f"Translation complete")
            except Exception as e:
                print(f"\nTranslation failed: {e}")
                print("Saving extracted text only...")
                translated_text = extracted_text

        # Step 7: Select output file
        output_file = select_output_file(input_file)
        if not output_file:
            print("\nNo output file specified. Exiting...")
            return

        # Step 8: Save output
        print(f"\n💾 Saving to: {output_file}")
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(translated_text)
            print("File saved successfully")
        except Exception as e:
            print(f"\nFailed to save file: {e}")
            return

        # Success!
        print("\n" + "="*60)
        print(" Process Complete")
        print("="*60)
        print(f"\nInput:  {input_file}")
        print(f"Output: {output_file}")
        print()

    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
