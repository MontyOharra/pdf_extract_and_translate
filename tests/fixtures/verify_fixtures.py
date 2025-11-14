#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick script to verify test PDF fixtures are set up correctly.

Run this to check if your PDF files and expected outputs are in place.
"""

from pathlib import Path
import sys

FIXTURES_DIR = Path(__file__).parent / "pdfs"
TYPED_DIR = FIXTURES_DIR / "typed"
SCANNED_DIR = FIXTURES_DIR / "scanned"
EXPECTED_DIR = FIXTURES_DIR / "expected_outputs"

# Define required test fixtures
REQUIRED_FIXTURES = [
    {
        "name": "Simple Text",
        "pdf": "simple_text.pdf",
        "type": "typed",
        "expected_txt": "simple_text.txt",
        "description": "Single line: 'Hello World'"
    },
    {
        "name": "Multi-line Text",
        "pdf": "multi_line.pdf",
        "type": "typed",
        "expected_txt": "multi_line.txt",
        "description": "Three lines of text"
    },
    {
        "name": "Numbers and Text",
        "pdf": "numbers_text.pdf",
        "type": "typed",
        "expected_txt": "numbers_text.txt",
        "description": "Text with numbers: 'I have 5 apples and 3 oranges.'"
    },
    {
        "name": "Punctuation",
        "pdf": "punctuation.pdf",
        "type": "typed",
        "expected_txt": "punctuation.txt",
        "description": "Text with punctuation marks"
    },
]


def check_fixture(fixture):
    """Check if a single fixture is properly set up."""
    pdf_dir = TYPED_DIR if fixture["type"] == "typed" else SCANNED_DIR
    pdf_path = pdf_dir / fixture["pdf"]
    txt_path = EXPECTED_DIR / fixture["expected_txt"]

    pdf_exists = pdf_path.exists()
    txt_exists = txt_path.exists()

    status = "✓" if (pdf_exists and txt_exists) else "✗"

    print(f"\n{status} {fixture['name']}")
    print(f"  Description: {fixture['description']}")
    print(f"  PDF: {pdf_path}")
    print(f"    Exists: {'YES ✓' if pdf_exists else 'NO ✗ - CREATE THIS FILE'}")

    if txt_exists:
        with open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"  Expected Output: {txt_path}")
        print(f"    Exists: YES ✓")
        print(f"    Content: '{content[:50]}{'...' if len(content) > 50 else ''}'")
    else:
        print(f"  Expected Output: {txt_path}")
        print(f"    Exists: NO ✗ - CREATE THIS FILE")

    return pdf_exists and txt_exists


def main():
    """Main verification function."""
    print("=" * 70)
    print("PDF TEST FIXTURE VERIFICATION")
    print("=" * 70)

    # Check if directories exist
    print("\nChecking directories...")
    dirs_ok = True
    for dir_name, dir_path in [
        ("Typed PDFs", TYPED_DIR),
        ("Scanned PDFs", SCANNED_DIR),
        ("Expected Outputs", EXPECTED_DIR)
    ]:
        exists = dir_path.exists()
        print(f"  {dir_name}: {dir_path}")
        print(f"    {'✓ Exists' if exists else '✗ Missing'}")
        if not exists:
            dirs_ok = False

    if not dirs_ok:
        print("\n✗ Some directories are missing. Please create them.")
        return False

    # Check each required fixture
    print("\n" + "=" * 70)
    print("REQUIRED TEST FIXTURES")
    print("=" * 70)

    all_ok = True
    results = []
    for fixture in REQUIRED_FIXTURES:
        is_ok = check_fixture(fixture)
        results.append((fixture["name"], is_ok))
        if not is_ok:
            all_ok = False

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    ready_count = sum(1 for _, ok in results if ok)
    total_count = len(results)

    for name, ok in results:
        status = "✓ READY" if ok else "✗ MISSING"
        print(f"  {status}: {name}")

    print(f"\n{ready_count}/{total_count} fixtures ready")

    if all_ok:
        print("\n🎉 All fixtures are ready! You can run the tests now.")
        print("   Run: make test")
    else:
        print("\n⚠️  Some fixtures are missing. Please create them.")
        print("   See the output above for details.")

    print("=" * 70)
    return all_ok


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
