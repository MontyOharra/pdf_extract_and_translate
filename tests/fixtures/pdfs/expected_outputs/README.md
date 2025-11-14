# Expected Output Files

This directory contains the expected text outputs for your test PDFs and images.

## How to Create Expected Output Files

For each PDF or image file in `typed/` or `scanned/`, you need to create a corresponding `.txt` file here with the **exact text** that should be extracted.

### File Naming Convention

The `.txt` file should have the same base name as your test file:

```
typed/3-languages.pdf → expected_outputs/3-languages.txt
scanned/hello-world-en-es.png → expected_outputs/hello-world-en-es.txt
scanned/typed-with-drawn.pdf → expected_outputs/typed-with-drawn.txt
```

### Steps to Create Expected Output Files

1. **Open your PDF or image** and look at the text
2. **Create a `.txt` file** with the same base name
3. **Type the exact text** that appears in the file
4. **Save with UTF-8 encoding**

### Example

If your `3-languages.pdf` contains:
```
Hello World
Hola Mundo
Bonjour le Monde
```

Then create `3-languages.txt` with exactly:
```
Hello World
Hola Mundo
Bonjour le Monde
```

## Current Files Needed

Based on your fixtures, you need to create:

- [ ] `3-languages.txt` (for 3-languages.pdf)
- [ ] `hello-world-en-es.txt` (for hello-world-en-es.png)
- [ ] `typed-with-drawn.txt` (for typed-with-drawn.pdf)

## Tips

- **Preserve line breaks** - If text is on separate lines, keep them separate
- **Include spacing** - Match the spacing in the original
- **Case sensitive** - Use exact capitalization
- **UTF-8 encoding** - Save as UTF-8 to support special characters
- **No extra whitespace** - Don't add extra blank lines at the end
