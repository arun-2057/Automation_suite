# Document Extractor

A unified tool for extracting text from PDFs and text documents.

## Features

- 📄 PDF text extraction using PyPDF2
- 📝 Support for TXT, MD, LOG files  
- 📊 Text analysis and statistics
- 💾 Save extracted text to files
- 🔍 Automatic file type detection

## Usage

```python
from document_extractor.extractor import DocumentExtractor

# Initialize extractor
extractor = DocumentExtractor()

# Extract from any supported file
text, stats = extractor.extract_from_file("document.pdf")

# Save extracted text
extractor.save_extracted_text(text, "output.txt")