# Test PDF Fixtures

This directory contains PDF files for testing OCR extraction functionality.

## Directory Structure

```
pdfs/
├── README.md                    # This file
├── typed/                       # PDFs with typed/digital text
│   ├── simple_text.pdf         # Single line of simple text
│   ├── multi_line.pdf          # Multiple lines of text
│   └── multi_page.pdf          # Multiple pages
├── scanned/                     # Scanned/image-based PDFs
│   ├── clean_scan.pdf          # High quality scan
│   ├── noisy_scan.pdf          # Scan with noise/artifacts
│   └── skewed_scan.pdf         # Slightly rotated scan
└── expected_outputs/            # Text files with expected outputs
    ├── simple_text.txt
    ├── multi_line.txt
    └── ...
```

## Creating Test PDFs

### Method 1: Using Google Docs/Word
1. Create a document with your test text
2. Export/Save as PDF
3. Name it descriptively (e.g., `simple_hello_world.pdf`)
4. Create corresponding `.txt` file with expected output

### Method 2: Using Online Tools
1. Use a tool like Canva, PDF creator, or similar
2. Add text or images
3. Download as PDF

### Method 3: Scanned PDFs
1. Print a document
2. Scan it to create an image-based PDF
3. This tests true OCR capabilities

## Naming Convention

Use descriptive names that indicate:
- Content type: `typed_`, `scanned_`, `handwritten_`
- Complexity: `simple_`, `complex_`, `multi_page_`
- Language: `_english`, `_spanish`, `_french`

Examples:
- `typed_simple_hello.pdf` - Simple typed "Hello World"
- `scanned_multi_line_english.pdf` - Scanned multi-line English text
- `typed_numbers_and_text.pdf` - Mixed numbers and text

## Expected Output Files

For each PDF, create a corresponding `.txt` file with the exact expected output:

```
pdfs/typed/simple_text.pdf
→ pdfs/expected_outputs/simple_text.txt
```

The test will read the PDF, extract text, and compare against the `.txt` file.

## Test Scenarios to Cover

1. **Simple typed text** - Single line, no special formatting
2. **Multi-line typed text** - Paragraphs with line breaks
3. **Special characters** - Punctuation, symbols, accents
4. **Numbers** - Digits, monetary amounts, dates
5. **Mixed content** - Text and numbers together
6. **Different fonts/sizes** - Bold, italic, various sizes
7. **Multi-page** - Content across multiple pages
8. **Scanned clean** - High-quality scanned image
9. **Scanned noisy** - Lower quality with artifacts
10. **Skewed/rotated** - Slightly rotated text

## Quick Start

1. Create `simple_text.pdf` with content: "Hello World"
2. Create `expected_outputs/simple_text.txt` with content: "Hello World"
3. Write test that loads PDF, extracts text, compares to expected output
4. Run test (should fail initially - RED)
5. Implement OCR extractor
6. Run test (should pass - GREEN)
