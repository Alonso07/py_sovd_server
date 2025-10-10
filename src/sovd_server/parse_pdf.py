#!/usr/bin/env python3
"""
Script to parse PDF using docling and convert to markdown
"""

import os
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend

def parse_pdf_to_markdown(pdf_path, output_path):
    """
    Parse a PDF file using docling and save as markdown
    """
    try:
        # Initialize the document converter
        converter = DocumentConverter()
        
        # Configure PDF pipeline options for better parsing
        pdf_options = PdfPipelineOptions()
        pdf_options.do_ocr = True  # Enable OCR for better text extraction
        pdf_options.do_table_structure = True  # Enable table structure detection
        
        # Convert the PDF to markdown
        print(f"Parsing PDF: {pdf_path}")
        result = converter.convert(pdf_path)
        
        # Get the markdown content
        markdown_content = result.document.export_to_markdown()
        
        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"Successfully converted PDF to markdown: {output_path}")
        print(f"Content length: {len(markdown_content)} characters")
        
        return True
        
    except Exception as e:
        print(f"Error parsing PDF: {str(e)}")
        return False

if __name__ == "__main__":
    # Define paths
    pdf_file = "ISO_DIS_17978-3(en).pdf"
    markdown_file = "ISO_DIS_17978-3(en).md"
    
    # Check if PDF file exists
    if not os.path.exists(pdf_file):
        print(f"Error: PDF file '{pdf_file}' not found!")
        exit(1)
    
    # Parse PDF to markdown
    success = parse_pdf_to_markdown(pdf_file, markdown_file)
    
    if success:
        print("PDF parsing completed successfully!")
    else:
        print("PDF parsing failed!")
        exit(1)
