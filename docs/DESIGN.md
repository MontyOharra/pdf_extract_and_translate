# PDF Text Extraction and Translation System - Design Document

## Overview

An interactive CLI system for extracting text from PDF and image files, with support for both typed and handwritten text, followed by automatic language detection and translation. Built with a plugin architecture for ability to switch between translation and extraction provides

## Goals

- Extract text from PDF and image files (digital text and handwritten/scanned)
- Automatically detect source language
- Translate to user-specified target language
- Support multiple extraction and translation engines via plugin architecture
- Provide an intuitive interactive CLI experience
- Follow Test-Driven Development (TDD) practices
- Demonstrate clean architecture and separation of concerns

## Architecture

### Plugin-Based Design

The system uses abstract base classes to define interfaces, allowing multiple implementations to be registered and selected at runtime. This provides:

- **Extensibility**: Easy to add new extractors or translators
- **Flexibility**: Users can choose the best tool for their needs
- **Testability**: Abstract interfaces make mocking straightforward
- **Separation of Concerns**: Business logic separate from implementation details

### Core Components

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                       │
│                  (Interactive CLI)                      │
│  - File Picker (GUI)                                    │
│  - Menu Selection (Terminal)                            │
│  - Output Formatting                                    │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│                  Document Processor                     │
│         (Orchestrates extraction + translation)         │
└────────────┬────────────────────────────┬───────────────┘
             │                            │
             ▼                            ▼
┌─────────────────────────┐  ┌─────────────────────────┐
│   Extraction Manager    │  │   Translation Manager   │
│  (Plugin Registry)      │  │   (Plugin Registry)     │
│                         │  │                         │
│  - Register extractors  │  │  - Register translators │
│  - Select by name       │  │  - Register detectors   │
│  - Route requests       │  │  - Auto-detect language │
└─────────┬───────────────┘  └──────────┬──────────────┘
          │                             │
          ▼                             ▼
  ┌───────────────┐            ┌─────────────────┐
  │  Extractors   │            │   Translators   │
  │  (Plugins)    │            │   (Plugins)     │
  │               │            │                 │
  │  - PyMuPDF    │            │  - deep-trans.  │
  │  - Tesseract  │            │  - argostrans.  │
  │  - EasyOCR    │            │  - DeepL        │
  │  - Cloud APIs │            │  - Cloud APIs   │
  └───────────────┘            └─────────────────┘
```

## Module Design

### 1. Text Extraction System

**Abstract Base Class**: `TextExtractor`

```python
class TextExtractor(ABC):
    """Base class for all text extraction implementations."""

    @abstractmethod
    def extract_text(self, input_data: Union[str, Path, bytes]) -> List[dict]:
        """Extract text from document, returning text + metadata."""
        pass

    @abstractmethod
    def supports_format(self, file_format: str) -> bool:
        """Check if this extractor supports the given file format."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of this extractor."""
        pass
```

**Manager**: `ExtractionManager`
- Maintains registry of available extractors
- Routes extraction requests to appropriate plugins
- Handles plugin registration and lookup

**Potential Implementations**:
- **PyMuPDF**: Fast extraction of digital/typed text from PDFs
- **Tesseract**: OCR for scanned documents and handwriting
- **EasyOCR**: Deep learning-based OCR
- **Google Vision**: Cloud-based OCR (requires API key)
- **Azure Form Recognizer**: Cloud-based OCR for forms (requires API key)

### 2. Translation System

**Abstract Base Class**: `Translator`

```python
class Translator(ABC):
    """Base class for all translation implementations."""

    @abstractmethod
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text from source to target language."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of this translator."""
        pass

    def supports_language(self, lang_code: str) -> bool:
        """Check if language is supported."""
        pass
```

**Abstract Base Class**: `LanguageDetector`

```python
class LanguageDetector(ABC):
    """Base class for language detection."""

    @abstractmethod
    def detect(self, text: str) -> str:
        """Detect language, returning ISO 639-1 code (e.g., 'en', 'es')."""
        pass
```

**Manager**: `TranslationManager`
- Maintains registry of translators and detectors
- Auto-detection workflow: detect → translate
- Handles plugin registration and lookup

**Potential Implementations**:

*Translators*:
- **deep-translator**: Free, supports multiple backends (Google, MyMemory, etc.)
- **argostranslate**: Offline translation, no internet required
- **DeepL**: High quality, requires API key (500k chars/month free)
- **Google Cloud Translate**: Requires API key
- **LibreTranslate**: Self-hosted option

*Language Detectors*:
- **langdetect**: Fast, supports 55+ languages
- **fastText**: Facebook's detector, very accurate
- **lingua-py**: High accuracy for short text

### 3. Processing Pipeline

**DocumentProcessor**: Main orchestrator that coordinates:
1. File input handling
2. Text extraction
3. Language detection
4. Translation
5. Result formatting

**Result Data Structures**: Type-safe containers for extraction and translation results

### 4. Interactive CLI

**Components**:
- **File Picker** (tkinter): GUI popup for selecting files
- **Menus** (questionary): Terminal menus with arrow key navigation
- **Formatters**: Output results as text, JSON, or file

**User Flow**:
```
1. File picker → Select PDF/image
2. Menu → Select target language
3. Menu → Select translator
4. Menu → Select extractor
5. Confirmation → Review and proceed
6. Results → View output
```

### 5. Utilities

**file_handler**: File I/O, path/bytes handling, format detection
**image_preprocessor**: Image enhancement for better OCR results
**validators**: Input validation and error checking
**logger**: Logging configuration

## Directory Structure

```
pdf_extract_and_translate/
│
├── src/
│   ├── cli/                    # Interactive CLI components
│   │   ├── file_picker.py      # GUI file selection
│   │   ├── menus.py            # Terminal menus
│   │   └── formatters.py       # Output formatting
│   │
│   ├── extractors/             # Text extraction
│   │   ├── base.py             # Abstract TextExtractor
│   │   └── manager.py          # ExtractionManager
│   │
│   ├── translators/            # Translation
│   │   ├── base.py             # Abstract Translator & LanguageDetector
│   │   └── manager.py          # TranslationManager
│   │
│   ├── pipeline/               # Main processing
│   │   ├── processor.py        # DocumentProcessor
│   │   └── result.py           # Result data structures
│   │
│   └── utils/                  # Utilities
│       ├── file_handler.py
│       ├── image_preprocessor.py
│       ├── validators.py
│       └── logger.py
│
├── tests/
│   ├── unit/                   # Unit tests
│   │   ├── test_cli/
│   │   └── test_translators/
│   ├── integration/            # Integration tests
│   └── fixtures/               # Test data
│
├── docs/
│   ├── DESIGN.md               # This file
│   ├── API.md                  # API documentation
│   └── USAGE.md                # User guide
│
├── .env.example                # API key template
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── Makefile
├── main.py
└── README.md
```

## Technology Stack

**Text Extraction**:
- PyMuPDF (fitz) - PDF text extraction
- pytesseract - OCR for scanned documents
- EasyOCR - Deep learning OCR
- Pillow - Image processing
- pdf2image - PDF to image conversion

**Translation**:
- deep-translator - Multi-backend translation (Google, MyMemory, etc.)
- argostranslate - Offline translation
- langdetect - Language detection
- deepl - DeepL API (optional, requires key)

**CLI/UX**:
- questionary - Interactive terminal menus
- tkinter - GUI file picker (built into Python)

**Development**:
- pytest - Testing framework
- pytest-cov - Coverage reporting
- python-dotenv - Environment variable management

## Design Decisions

### Why Plugin Architecture?

**Pros**:
- Easy to add new extractors/translators without modifying core code
- Users can choose the best tool for their specific needs
- Testable through dependency injection
- Demonstrates SOLID principles (Open/Closed Principle)

**Cons**:
- More initial complexity than hardcoded implementations
- Requires abstract base classes and registration

**Decision**: The benefits outweigh the costs for an interview project, as it demonstrates software architecture skills.

### Why Interactive CLI Instead of Config Files?

**Pros**:
- Better user experience (no memorizing command args)
- Visual feedback with arrow key navigation
- No config file syntax to learn
- Impressive in demonstrations

**Cons**:
- Not ideal for automation/scripting
- Requires user interaction

**Decision**: For an interview demo, the visual impact and UX are more important. Could add non-interactive mode later.

### Why TDD (Test-Driven Development)?

**Pros**:
- Forces thinking about interfaces before implementation
- Results in more testable code
- Demonstrates testing proficiency
- Catches bugs early

**Workflow**:
1. Write failing test (RED)
2. Write minimal code to pass (GREEN)
3. Refactor for quality (REFACTOR)
4. Repeat

### Why Not a Package?

**Decision**: Keep it simple as a runnable project rather than an installable package.

**Rationale**:
- Interview project, not production library
- Simpler setup: `git clone` + `make setup` + `make run`
- No need for PyPI distribution
- Easier to understand for reviewers

### Local vs Cloud Extractors/Translators

**Local (No API Key)**:
- PyMuPDF, Tesseract, EasyOCR
- deep-translator, argostranslate
- Always available, privacy-focused

**Cloud (Requires API Key)**:
- Google Vision, Azure OCR
- DeepL API, Google Cloud Translate
- Higher quality, but requires setup

**Decision**: Support both, but make cloud optional via `.env` file.

## Data Flow

```
User Input
    │
    ├─→ File Selection (GUI)
    │       │
    │       └─→ File Path
    │
    ├─→ Target Language Selection (Menu)
    │       │
    │       └─→ Language Code
    │
    ├─→ Translator Selection (Menu)
    │       │
    │       └─→ Translator Name
    │
    └─→ Extractor Selection (Menu)
            │
            └─→ Extractor Name
                    │
                    ▼
            DocumentProcessor
                    │
                    ├─→ ExtractionManager.extract(file, extractor)
                    │       │
                    │       └─→ Extracted Text + Metadata
                    │
                    ├─→ TranslationManager.detect(text)
                    │       │
                    │       └─→ Source Language
                    │
                    └─→ TranslationManager.translate(text, src, tgt, translator)
                            │
                            └─→ Translated Text
                                    │
                                    ▼
                            Output Formatter
                                    │
                                    ├─→ Console
                                    ├─→ JSON
                                    └─→ File
```

## Error Handling Strategy

- **Input Validation**: Validate file types, language codes before processing
- **Graceful Degradation**: If extractor fails, provide helpful error message
- **API Key Errors**: Detect missing/invalid API keys early and guide user
- **User-Friendly Messages**: No stack traces in normal operation, clear error messages

## Testing Strategy

**Unit Tests**: Test individual classes in isolation
- Mock dependencies
- Test edge cases and error conditions
- Fast execution

**Integration Tests**: Test components working together
- Real extractors/translators (or test doubles)
- Verify data flows correctly
- May be slower

**Fixtures**: Sample PDFs and images for consistent testing

## Future Enhancements

- **Visual Overlay**: Display translated text over original PDF
- **Batch Processing**: Process multiple files at once
- **Caching**: Cache extraction results to avoid re-processing
- **Configuration Profiles**: Save favorite settings
- **Web UI**: Browser-based interface
- **API Mode**: RESTful API for integration with other tools
