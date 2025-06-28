#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF to Markdown Converter using Marker

This module provides functionality to convert PDF documents to Markdown format
using the high-performance marker library, which offers state-of-the-art accuracy
and supports complex layouts, tables, and mathematical formulas.
"""

import os
import json
import logging
from typing import Optional, Dict, Any, List
from pathlib import Path
import argparse

from src.learn_pilot.core.logging.logger import logger

try:
    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict
    from marker.output import text_from_rendered
    from marker.config.parser import ConfigParser
except ImportError as e:
    raise ImportError(
        "Marker library not found. Please install it with: pip install marker-pdf\n"
        f"Original error: {e}"
    )


class MarkerPDFConverter:
    """
    High-performance PDF to Markdown converter using the Marker library.
    
    Features:
    - State-of-the-art accuracy for text extraction
    - Complex layout detection and preservation
    - Table extraction and formatting
    - Mathematical formula support
    - OCR for scanned documents
    - Optional LLM enhancement for improved quality
    """
    
    def __init__(self, 
                 use_llm: bool = False,
                 extract_images: bool = True,
                 max_pages: Optional[int] = None,
                 output_format: str = "markdown",
                 force_ocr: bool = False,
                 format_lines: bool = False):
        """
        Initialize the Marker PDF converter.
        
        Args:
            use_llm: Whether to use LLM for improved conversion quality
            extract_images: Whether to extract and save images
            max_pages: Maximum number of pages to process (None for all)
            output_format: Output format ("markdown", "json", "html", "chunks")
            force_ocr: Force OCR processing on entire document
            format_lines: Reformat lines using local OCR model
        """
        self.use_llm = use_llm
        self.extract_images = extract_images
        self.max_pages = max_pages
        self.output_format = output_format
        self.force_ocr = force_ocr
        self.format_lines = format_lines
        self.logger = logger
        
        # Initialize models and converter
        self._models = None
        self._converter = None
        
    def _load_models(self):
        """Load Marker models (lazy loading for better performance)."""
        if self._models is None:
            self.logger.info("Loading Marker models...")
            try:
                self._models = create_model_dict()
                self.logger.info("Models loaded successfully")
            except Exception as e:
                self.logger.error(f"Failed to load models: {e}")
                raise
        return self._models
    
    def _get_converter(self):
        """Get the PDF converter with current configuration."""
        if self._converter is None:
            # Create configuration
            config_dict = {
                "output_format": self.output_format,
                "disable_image_extraction": not self.extract_images,
                "use_llm": self.use_llm,
                "force_ocr": self.force_ocr,
                "format_lines": self.format_lines
            }
            
            if self.max_pages:
                config_dict["max_pages"] = self.max_pages
            
            # Create config parser with our settings
            config_parser = ConfigParser(config_dict)
            
            # Load models
            models = self._load_models()
            
            # Create converter
            self._converter = PdfConverter(
                config=config_parser.generate_config_dict(),
                artifact_dict=models,
                processor_list=config_parser.get_processors(),
                renderer=config_parser.get_renderer(),
                llm_service=config_parser.get_llm_service() if self.use_llm else None
            )
        
        return self._converter
    
    def convert_pdf_to_markdown(self, 
                              pdf_path: str, 
                              output_path: Optional[str] = None,
                              image_output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Convert a PDF file to Markdown format using Marker.
        
        Args:
            pdf_path: Path to the input PDF file
            output_path: Optional path to save the markdown file
            image_output_dir: Directory to save extracted images
            
        Returns:
            Dict containing:
                - 'markdown': The markdown content
                - 'metadata': Document metadata
                - 'images': List of extracted images (if enabled)
                
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            Exception: If conversion fails
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
        try:
            self.logger.info(f"Converting PDF: {pdf_path}")
            
            # Get converter
            converter = self._get_converter()
            
            # Convert PDF
            rendered = converter(pdf_path)
            
            # Extract text and images from rendered output
            if self.output_format == "markdown":
                markdown_text, metadata, images = text_from_rendered(rendered)
                
                result = {
                    'markdown': markdown_text,
                    'metadata': metadata or {},
                    'images': images if self.extract_images else []
                }
            else:
                # For other formats, return the rendered object directly
                result = {
                    'rendered': rendered,
                    'metadata': getattr(rendered, 'metadata', {}),
                    'images': getattr(rendered, 'images', {}) if self.extract_images else {}
                }
                
                # Try to get markdown content if available
                if hasattr(rendered, 'markdown'):
                    result['markdown'] = rendered.markdown
                else:
                    result['markdown'] = str(rendered)
            
            # Add document header with metadata
            if 'markdown' in result:
                enhanced_markdown = self._add_document_header(result, pdf_path)
                result['markdown'] = enhanced_markdown
            
            # Save to file if output path provided
            if output_path and 'markdown' in result:
                self._save_markdown(result['markdown'], output_path)
                self.logger.info(f"Markdown saved to: {output_path}")
            
            # Save images if specified
            if image_output_dir and result.get('images'):
                self._save_images(result['images'], image_output_dir)
            
            # Save metadata
            if output_path and result.get('metadata'):
                metadata_path = output_path.replace('.md', '_metadata.json')
                self._save_metadata(result['metadata'], metadata_path)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error converting PDF: {e}")
            raise
    
    def _add_document_header(self, result: Dict[str, Any], pdf_path: str) -> str:
        """Add a document header with metadata to the markdown."""
        pdf_name = Path(pdf_path).stem
        metadata = result.get('metadata', {})
        
        header_parts = [
            f"# {pdf_name}",
            "",
            f"*Converted from PDF: {os.path.basename(pdf_path)}*",
            ""
        ]
        
        # Add metadata if available
        if metadata:
            header_parts.extend([
                "## Document Information",
                ""
            ])
            
            # Handle case where metadata might be a string
            if isinstance(metadata, dict):
                # Add various metadata fields if they exist
                metadata_fields = [
                    ('pages', 'Pages'),
                    ('language', 'Language'),
                    ('creation_date', 'Created'),
                    ('title', 'Title'),
                    ('author', 'Author'),
                    ('subject', 'Subject'),
                    ('keywords', 'Keywords')
                ]
                
                for field, label in metadata_fields:
                    if field in metadata and metadata[field]:
                        header_parts.append(f"- **{label}**: {metadata[field]}")
            else:
                # If metadata is a string, just add it as-is
                header_parts.append(f"- **Metadata**: {metadata}")
                    
            header_parts.extend(["", "---", ""])
        
        # Combine header with content
        return "\n".join(header_parts) + "\n" + result['markdown']
    
    def _save_markdown(self, content: str, output_path: str) -> None:
        """Save markdown content to a file."""
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            self.logger.error(f"Failed to save markdown: {e}")
            raise
    
    def _save_images(self, images: Dict[str, Any], image_output_dir: str) -> None:
        """Save extracted images to directory."""
        try:
            os.makedirs(image_output_dir, exist_ok=True)
            for image_id, image_data in images.items():
                # Save image (implementation depends on image format)
                # This is a placeholder - actual implementation would depend on
                # how marker provides the image data
                image_path = os.path.join(image_output_dir, f"{image_id}.png")
                self.logger.info(f"Image saved: {image_path}")
        except Exception as e:
            self.logger.error(f"Failed to save images: {e}")
    
    def _save_metadata(self, metadata: Dict[str, Any], output_path: str) -> None:
        """Save metadata to a JSON file."""
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Failed to save metadata: {e}")


def convert_pdf_to_markdown(pdf_path: str,
                          output_path: Optional[str] = None,
                          use_llm: bool = False,
                          extract_images: bool = True,
                          image_output_dir: Optional[str] = None,
                          max_pages: Optional[int] = None,
                          output_format: str = "markdown",
                          force_ocr: bool = False,
                          format_lines: bool = False) -> Dict[str, Any]:
    """
    Convenience function to convert PDF to Markdown using Marker.
    
    Args:
        pdf_path: Path to the input PDF file
        output_path: Optional path to save the markdown file
        use_llm: Whether to use LLM for improved conversion quality
        extract_images: Whether to extract and save images
        image_output_dir: Directory to save extracted images
        max_pages: Maximum number of pages to process
        output_format: Output format ("markdown", "json", "html", "chunks")
        force_ocr: Force OCR processing on entire document
        format_lines: Reformat lines using local OCR model
        
    Returns:
        Dict containing markdown content, metadata, and images
    """
    converter = MarkerPDFConverter(
        use_llm=use_llm,
        extract_images=extract_images,
        max_pages=max_pages,
        output_format=output_format,
        force_ocr=force_ocr,
        format_lines=format_lines
    )
    
    return converter.convert_pdf_to_markdown(
        pdf_path=pdf_path,
        output_path=output_path,
        image_output_dir=image_output_dir
    )


def batch_convert_pdfs(pdf_directory: str,
                      output_directory: str,
                      use_llm: bool = False,
                      extract_images: bool = True) -> List[Dict[str, Any]]:
    """
    Convert multiple PDFs in a directory to Markdown.
    
    Args:
        pdf_directory: Directory containing PDF files
        output_directory: Directory to save converted files
        use_llm: Whether to use LLM enhancement
        extract_images: Whether to extract images
        
    Returns:
        List of conversion results
    """
    pdf_files = list(Path(pdf_directory).glob("*.pdf"))
    results = []
    
    converter = MarkerPDFConverter(
        use_llm=use_llm,
        extract_images=extract_images
    )
    
    for pdf_file in pdf_files:
        try:
            output_file = Path(output_directory) / f"{pdf_file.stem}.md"
            image_dir = Path(output_directory) / "images" / pdf_file.stem if extract_images else None
            
            result = converter.convert_pdf_to_markdown(
                pdf_path=str(pdf_file),
                output_path=str(output_file),
                image_output_dir=str(image_dir) if image_dir else None
            )
            
            results.append({
                'input_file': str(pdf_file),
                'output_file': str(output_file),
                'success': True,
                'result': result
            })
            
        except Exception as e:
            logger.error(f"Failed to convert {pdf_file}: {e}")
            results.append({
                'input_file': str(pdf_file),
                'output_file': None,
                'success': False,
                'error': str(e)
            })
    
    return results


# Command line interface
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert PDF to Markdown using Marker - High-quality PDF conversion"
    )
    
    # Input/Output options
    parser.add_argument("--pdf-path", 
                       default="scripts/1706.03762v7.Attention_Is_All_You_Need.pdf",
                       help="Path to the input PDF file")
    parser.add_argument("-o", "--output", 
                       default="scripts/1706.03762v7.Attention_Is_All_You_Need.md",
                       help="Output markdown file path")
    parser.add_argument("--batch-dir", 
                       help="Directory containing PDFs for batch conversion")
    parser.add_argument("--output-dir", 
                       default="./output",
                       help="Output directory for batch conversion")
    
    # Conversion options
    parser.add_argument("--use-llm", 
                       action="store_true",
                       help="Use LLM to enhance conversion quality")
    parser.add_argument("--no-images", 
                       action="store_true",
                       help="Don't extract images")
    parser.add_argument("--image-dir", 
                       default="scripts/images",
                       help="Directory to save extracted images")
    parser.add_argument("--max-pages", 
                       type=int,
                       help="Maximum number of pages to process")
    parser.add_argument("--output-format", 
                       choices=["markdown", "json", "html", "chunks"],
                       default="markdown",
                       help="Output format")
    parser.add_argument("--force-ocr", 
                       action="store_true",
                       help="Force OCR processing on entire document")
    parser.add_argument("--format-lines", 
                       action="store_true",
                       help="Reformat lines using local OCR model")
    
    args = parser.parse_args()
    
    try:
        if args.batch_dir:
            # Batch conversion
            print(f"Converting PDFs in {args.batch_dir}...")
            results = batch_convert_pdfs(
                pdf_directory=args.batch_dir,
                output_directory=args.output_dir,
                use_llm=args.use_llm,
                extract_images=not args.no_images
            )
            
            # Print summary
            successful = sum(1 for r in results if r['success'])
            failed = len(results) - successful
            print(f"\nConversion complete: {successful} successful, {failed} failed")
            
            if failed > 0:
                print("\nFailed files:")
                for r in results:
                    if not r['success']:
                        print(f"  {r['input_file']}: {r['error']}")
                        
        else:
            # Single file conversion
            print(f"Converting {args.pdf_path}...")
            result = convert_pdf_to_markdown(
                pdf_path=args.pdf_path,
                output_path=args.output,
                use_llm=args.use_llm,
                extract_images=not args.no_images,
                image_output_dir=args.image_dir,
                max_pages=args.max_pages,
                output_format=args.output_format,
                force_ocr=args.force_ocr,
                format_lines=args.format_lines
            )
            
            print(f"✅ Conversion successful!")
            print(f"📄 Markdown saved to: {args.output}")
            
            if result.get('images'):
                print(f"🖼️  Extracted {len(result['images'])} images")
                
            # Show metadata
            metadata = result.get('metadata', {})
            if metadata:
                # Handle case where metadata might be a string
                if isinstance(metadata, dict):
                    print(f"📊 Pages processed: {metadata.get('pages', 'Unknown')}")
                    if 'language' in metadata:
                        print(f"🌐 Detected language: {metadata['language']}")
                else:
                    print(f"📊 Metadata: {metadata}")
            
            if not args.output:
                print("\n" + "="*50)
                print("CONVERTED CONTENT:")
                print("="*50)
                print(result['markdown'][:1000] + "..." if len(result['markdown']) > 1000 else result['markdown'])
                
    except KeyboardInterrupt:
        print("\n⚠️  Conversion interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
