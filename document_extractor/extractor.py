import PyPDF2
import pandas as pd
import re
from datetime import datetime
import os

class DocumentExtractor:
    """Extract text from PDF and text documents"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.txt', '.md', '.log']
    
    def extract_pdf_text(self, file_path):
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n\n"
                return text, len(pdf_reader.pages)
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def extract_text_file(self, file_path):
        """Extract text from various text file formats"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    return file.read()
            except Exception as e:
                raise Exception(f"Error reading text file: {str(e)}")
    
    def analyze_text_content(self, text):
        """Analyze extracted text and provide statistics"""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        paragraphs = [p for p in text.split('\n\n') if p.strip()]
        
        # Word frequency analysis
        word_freq = {}
        for word in words:
            clean_word = re.sub(r'[^\w]', '', word.lower())
            if clean_word and len(clean_word) > 2:
                word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
        
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'char_count': len(text),
            'word_count': len(words),
            'sentence_count': len([s for s in sentences if s.strip()]),
            'paragraph_count': len(paragraphs),
            'top_words': top_words,
            'file_size_mb': len(text.encode('utf-8')) / (1024 * 1024)
        }
    
    def extract_from_file(self, file_path):
        """Main method to extract text from any supported file"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            text, page_count = self.extract_pdf_text(file_path)
            stats = self.analyze_text_content(text)
            stats['page_count'] = page_count
            return text, stats
        
        elif file_ext in ['.txt', '.md', '.log']:
            text = self.extract_text_file(file_path)
            stats = self.analyze_text_content(text)
            stats['page_count'] = 1
            return text, stats
        
        else:
            raise ValueError(f"Unsupported file format: {file_ext}. Supported: {self.supported_formats}")
    
    def save_extracted_text(self, text, output_path):
        """Save extracted text to file"""
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(text)
        return output_path