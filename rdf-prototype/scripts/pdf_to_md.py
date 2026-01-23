import sys
import os
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
from docling.datamodel.base_models import InputFormat

def convert_pdf_to_md(pdf_path, output_path):
    """
    Converts a PDF file to Markdown using Docling with OCR and Table recognition enabled.
    """
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File not found: {pdf_path}")
        return

    print(f"⚙️  Configuring Docling pipeline (OCR & Tables enabled)...")

    # 1. Configure Pipeline Options
    # This ensures scanned pages (images) and complex tables are parsed correctly.
    pipeline_options = PdfPipelineOptions(
        do_ocr=True,                      # Enable OCR for images/scans
        do_table_structure=True,          # Enhanced table structure recognition
        table_structure_mode=TableFormerMode.ACCURATE  # Use more precise model
    )

    # 2. Initialize Converter with options
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    print(f"🔄 Starting conversion for: {pdf_path}...")
    print(f"   (This might take a while due to OCR processing)")
    
    try:
        # 3. Convert
        result = converter.convert(pdf_path)
        
        # 4. Export to Markdown
        markdown_content = result.document.export_to_markdown()
        
        # 5. Save to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
            
        print(f"✅ Success! Markdown saved at: {output_path}")
        
    except Exception as e:
        print(f"💥 An error occurred: {e}")

if __name__ == "__main__":
    # Usage: python scripts/pdf_to_md.py path/to/file.pdf [output.md]
    if len(sys.argv) < 2:
        print("Please provide the PDF path. Usage: python scripts/pdf_to_md.py <input.pdf> [output.md]")
        sys.exit(1)
        
    input_file = sys.argv[1]
    
    # Generate output name automatically if not provided
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        output_file = os.path.splitext(input_file)[0] + ".md"
        
    convert_pdf_to_md(input_file, output_file)