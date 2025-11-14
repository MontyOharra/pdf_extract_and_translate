# PDF Text Extraction and Translation System - Design Document

## Overview

An interactive CLI system for extracting text from PDF and image files, with support for both typed and scanned text, followed by automatic language detection and translation. Built with a registry-based architecture for flexibility in choosing extraction and translation engines.

## Goals

- Extract text from PDF and image files (digital text and scanned/OCR)
- Automatically detect source language(s) in extracted text
- Handle multilingual documents (line-by-line language detection and translation)
- Translate to user-specified target language
- Support multiple extraction engines via registry pattern
- Provide an intuitive interactive CLI experience
- Follow Test-Driven Development (TDD) practices
- Demonstrate clean architecture and separation of concerns

## Architecture

### Registry-Based Design

The system uses abstract base classes to define interfaces, with a registry pattern for managing multiple implementations. This provides:

- **Extensibility**: Easy to add new extractors or translators
- **Flexibility**: Users can choose the best tool for their needs
- **Testability**: Abstract interfaces make mocking straightforward
- **Separation of Concerns**: Business logic separate from implementation details

### Core Components

```
┌─────────────────────────────────────────────────────────┐
│                    CLI Interface                        │
│                  (Interactive CLI)                      │
│  - File Picker                                          │
│  - Extractor Selection Menu                             │
│  - Language Selection Menu                              │
│  - Output File Specification                            │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│                    CLI Runner                           │
│         (Orchestrates extraction + translation)         │
│  1. Setup registry                                      │
│  2. Get user selections                                 │
│  3. Extract text                                        │
│  4. Translate text (multilingual support)               │
│  5. Save output                                         │
└────────────┬────────────────────────────┬───────────────┘
             │                            │
             ▼                            ▼
┌─────────────────────────┐  ┌─────────────────────────┐
│  Extractor Registry     │  │  Translation Manager    │
│                         │  │                         │
│  - Register extractors  │  │  - Language detection   │
│  - Create instances     │  │  - Translation wrapper  │
│  - Manage availability  │  │  - Line-by-line trans.  │
└─────────┬───────────────┘  └──────────┬──────────────┘
          │                             │
          ▼                             ▼
  ┌───────────────┐            ┌─────────────────┐
  │  Extractors   │            │  Translators    │
  │               │            │                 │
  │  - Tesseract  │            │  - langdetect   │
  │  - Azure OCR  │            │  - deep-trans.  │
  └───────────────┘            └─────────────────┘
```

## Module Design

### 1. Text Extraction System

**Abstract Base Class**: `TextExtractor`
- Defines interface for all text extraction implementations
- Key method: `extract_text(file_path: str) -> str`
- Returns extracted text as a single string

**Registry**: `ExtractorRegistry`
- Maintains registry of available extractors
- Registers extractors with display names
- Creates extractor instances on demand
- Handles credential validation for cloud extractors

**Current Implementations**:
- **Tesseract OCR (Local)**:
  - Local OCR engine for scanned documents
  - Supports PDF and image files (PNG, JPG, JPEG)
  - No credentials required
  - Uses pytesseract and pdf2image

- **Azure Document Intelligence (Cloud)**:
  - Cloud-based OCR using Microsoft Azure
  - High-quality text extraction with prebuilt-read model
  - Requires API key and endpoint (configured via .env)
  - Supports complex layouts and handwriting

### 2. Translation System

**Abstract Base Class**: `LanguageDetector`
- Defines interface for language detection implementations
- Key method: `detect(text: str) -> str`
- Returns ISO 639-1 language code (e.g., 'en', 'ja', 'de')

**Wrapper Class**: `DeepTranslatorWrapper`
- Wraps the deep-translator library
- Provides unified interface for translation
- Key method: `translate(text, source_lang, target_lang) -> str`
- Currently uses Google Translate backend
- Supports common ISO 639-1 language codes

**Manager**: `TranslationManager`
- Combines language detection and translation into unified workflow
- Two translation modes:
  - **Single Language**: `auto_translate()` - detects one language for entire document
  - **Multilingual**: `auto_translate_multilingual()` - detects and translates line-by-line
- Handles validation and error recovery

**Key Feature: Multilingual Document Support**
- Splits document into individual lines
- Detects language of each line independently
- Translates each line from its source language to target language
- Preserves lines already in target language
- Maintains document structure (empty lines, formatting)

**Current Implementations**:
- **Language Detector**: langdetect (supports 55+ languages)
- **Translator**: deep-translator with Google Translate backend (free, no API key)

### 3. Interactive CLI

**Components**:
- **File Picker**: Custom file selection with extension filtering
- **Prompts** (questionary): Interactive menus for extractor and language selection
- **Runner**: Main orchestrator that coordinates the workflow

**User Flow**:
```
1. File picker → Select PDF/image
2. Menu → Select extractor (Tesseract or Azure)
3. [Extraction occurs automatically]
4. Menu → Select target language (with "Other" option for custom codes)
5. [Multilingual translation occurs automatically]
6. Text input → Specify output filename (with suggested default)
7. [Save output and display summary]
```

**CLI Modules**:
- `file_picker.py`: File selection with extension filtering
- `prompts.py`: Interactive menus (extractor, language, output file)
- `runner.py`: Main workflow orchestration
- `__init__.py`: Module exports

## Directory Structure

```
pdf_extract_and_translate/
│
├── src/
│   ├── cli/                          # Interactive CLI components
│   │   ├── __init__.py               # Module exports
│   │   ├── file_picker.py            # File selection with filtering
│   │   ├── prompts.py                # Interactive menus
│   │   └── runner.py                 # Main workflow orchestration
│   │
│   ├── extractors/                   # Text extraction
│   │   ├── __init__.py
│   │   ├── base.py                   # Abstract TextExtractor
│   │   ├── registry.py               # ExtractorRegistry
│   │   ├── tesseract_extractor.py    # Tesseract OCR implementation
│   │   └── azure_ocr_extractor.py    # Azure Document Intelligence
│   │
│   └── translators/                  # Translation
│       ├── __init__.py
│       ├── base.py                   # Abstract LanguageDetector
│       ├── language_detector.py      # langdetect implementation
│       ├── deep_translator_wrapper.py # deep-translator wrapper
│       └── manager.py                # TranslationManager
│
├── tests/
│   ├── unit/                         # Unit tests
│   │   ├── test_extractors/
│   │   │   ├── test_tesseract.py
│   │   │   └── test_azure_ocr.py
│   │   └── test_translators/
│   │       ├── test_language_detector.py
│   │       ├── test_deep_translator.py
│   │       └── test_manager.py
│   └── fixtures/                     # Test data (PDFs and images)
│       ├── 3-languages.pdf
│       ├── hello-world-en-es.png
│       └── typed-with-drawn.pdf
│
├── docs/
│   └── design.md                     # This file
│
├── conda_env/                        # Conda environment (local)
├── .env                              # API credentials (gitignored)
├── .env.example                      # API key template
├── .gitignore
├── requirements.txt                  # Production dependencies
├── requirements-dev.txt              # Development dependencies
├── Makefile                          # Build automation
├── main.py                           # Entry point
└── README.md
```

## Technology Stack

**Text Extraction**:
- pytesseract - OCR for scanned documents and images
- pdf2image - PDF to image conversion for OCR
- Pillow - Image processing
- azure-ai-documentintelligence - Cloud-based OCR (optional, requires credentials)
- poppler - PDF rendering utilities (installed via conda)

**Translation**:
- deep-translator - Google Translate backend (free, no API key)
- langdetect - Language detection (supports 55+ languages)

**CLI/UX**:
- questionary - Interactive terminal menus with arrow key navigation
- Custom file picker with extension filtering

**Development**:
- pytest - Testing framework
- pytest-cov - Coverage reporting
- python-dotenv - Environment variable management
- conda - Environment and dependency management

## Design Decisions

### Why Registry Pattern?

**Pros**:
- Easy to add new extractors without modifying core code
- Users can choose the best tool for their specific needs
- Clean separation between registration and usage
- Demonstrates design pattern knowledge

**Cons**:
- More initial setup than hardcoded implementations
- Requires registry management

**Decision**: The registry pattern provides flexibility while keeping the code organized and extensible.

### Why Interactive CLI?

**Pros**:
- Better user experience than command-line arguments
- Visual feedback with arrow key navigation
- Guided workflow - users can't skip steps
- Professional appearance

**Cons**:
- Not ideal for automation/scripting
- Requires user interaction

**Decision**: Interactive CLI provides the best user experience for manual document processing tasks.

### Why Line-by-Line Translation for Multilingual Documents?

**Problem**: Documents with mixed languages (e.g., Japanese + English + German) would be detected as only one language, causing incorrect translations.

**Solution**: Detect and translate each line independently.

**Pros**:
- Handles multilingual documents correctly
- Preserves document structure
- Each language section translated appropriately

**Cons**:
- More API calls (slower for large documents)
- May not handle multi-line sentences perfectly

**Decision**: Accuracy is more important than speed for this use case.

### Why Conda Instead of venv?

**Pros**:
- Can install system dependencies (Tesseract, Poppler) alongside Python packages
- Consistent environment across platforms
- Local environment support (project-specific, not global)

**Cons**:
- Larger download size
- Requires Conda/Miniconda installed

**Decision**: The ability to manage system dependencies makes Conda the better choice for this project.

### Local vs Cloud Extractors

**Local (Tesseract)**:
- No API key required
- Works offline
- Free
- Good for general use

**Cloud (Azure Document Intelligence)**:
- Requires API key and endpoint
- Higher quality extraction
- Better handling of complex layouts
- Supports handwriting better

**Decision**: Support both, but make cloud optional via `.env` file. This gives users flexibility based on their needs and available resources.

## Data Flow

```
CLI Runner (run_cli)
    │
    ├─→ 1. Setup Registry
    │       │
    │       └─→ Register Tesseract OCR & Azure Document Intelligence
    │
    ├─→ 2. File Selection
    │       │
    │       └─→ File Path (PDF/PNG/JPG/JPEG)
    │
    ├─→ 3. Extractor Selection
    │       │
    │       └─→ Extractor Name
    │               │
    │               └─→ ExtractorRegistry.create_extractor(name)
    │                       │
    │                       └─→ Extractor Instance
    │
    ├─→ 4. Text Extraction
    │       │
    │       └─→ extractor.extract_text(file_path)
    │               │
    │               └─→ Extracted Text (string)
    │
    ├─→ 5. Target Language Selection
    │       │
    │       └─→ Language Code (en/es/ja/etc. or custom)
    │
    ├─→ 6. Multilingual Translation
    │       │
    │       └─→ TranslationManager.auto_translate_multilingual(text, target_lang)
    │               │
    │               ├─→ For each line:
    │               │   ├─→ LangDetectDetector.detect(line)
    │               │   │       └─→ Source Language Code
    │               │   │
    │               │   └─→ DeepTranslatorWrapper.translate(line, src, target)
    │               │           └─→ Translated Line
    │               │
    │               └─→ Translated Text (all lines joined)
    │
    ├─→ 7. Output File Selection
    │       │
    │       └─→ Output Path (with suggested default)
    │
    └─→ 8. Save to File
            │
            └─→ Write translated text to file
                    │
                    └─→ Display Summary (input, output, line count)
```

## Error Handling Strategy

- **File Selection**: Exit gracefully if no file selected
- **Extractor Selection**: Exit gracefully if no extractor chosen
- **Missing Credentials**: Detect missing Azure credentials early and inform user
- **Extraction Failures**: Catch exceptions, display error message, exit gracefully
- **Translation Failures**: Catch exceptions, save extracted text without translation
- **Line-Level Failures**: If a single line fails to translate, keep original text for that line
- **Keyboard Interrupt**: Handle Ctrl+C cleanly without stack traces
- **User-Friendly Messages**: Clear error messages without technical jargon

## Testing Strategy

**Unit Tests**: Test individual classes in isolation
- Mock external dependencies (APIs, file system)
- Test edge cases and error conditions
- Fast execution

**Functional Tests**: Test with real fixtures
- Use actual PDF and image files with known content
- Test multilingual documents (3-languages.pdf)
- Test various formats (PNG, PDF with handwriting)
- Skip Azure tests if credentials not available

**Fixtures**: Sample PDFs and images created manually
- `3-languages.pdf`: German, English, and Japanese text
- `hello-world-en-es.png`: English and Spanish text
- `typed-with-drawn.pdf`: Mixed typed and handwritten text

**Test Organization**:
- `tests/unit/test_extractors/`: Tesseract and Azure extractor tests
- `tests/unit/test_translators/`: Language detection, translation, and manager tests
- `tests/fixtures/`: Sample files for testing

## Future Enhancements

- **Paragraph-Level Translation**: Group lines into paragraphs for better context
- **Batch Processing**: Process multiple files at once
- **Progress Indicators**: Show progress for long documents
- **Configuration Profiles**: Save favorite extractor/language combinations
- **Additional Extractors**: Add support for more OCR engines
- **Output Formats**: Support for formatted output (Markdown, HTML)
- **Translation History**: Keep track of previous translations
