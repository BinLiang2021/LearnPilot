#!/bin/bash

# Quick Test Script for PDF to Markdown Conversion
# Test with the Attention Is All You Need paper (first 3 pages only)

export PYTHONPATH=.:$PYTHONPATH
set -e

echo "🚀 Quick PDF to Markdown Test with Marker"
echo "=========================================="
echo ""

PDF_FILE="scripts/1706.03762v7.Attention_Is_All_You_Need.pdf"
OUTPUT_FILE="scripts/attention_test.md"
CONVERTER="src/learn_pilot/literature_utils/knowledge_parser/pdf_to_markdown.py"

# Check if files exist
if [ ! -f "$PDF_FILE" ]; then
    echo "❌ PDF file not found: $PDF_FILE"
    echo "Please make sure the file exists"
    exit 1
fi

if [ ! -f "$CONVERTER" ]; then
    echo "❌ Converter not found: $CONVERTER"
    exit 1
fi

echo "📄 Input:  $PDF_FILE"
echo "📝 Output: $OUTPUT_FILE"
echo ""

# Create output directory
mkdir -p scripts/images

echo "🔄 Converting first 3 pages (test mode)..."
echo ""

# Run conversion with new API parameters
python "$CONVERTER" \
    --pdf-path "$PDF_FILE" \
    --output "$OUTPUT_FILE" \
    --max-pages 3 \
    --image-dir "scripts/images" \
    --format-lines \
    --output-format markdown

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Conversion completed successfully!"
    echo ""
    echo "📊 Results:"
    
    if [ -f "$OUTPUT_FILE" ]; then
        echo "📄 Markdown file: $OUTPUT_FILE"
        echo "📏 File size: $(wc -c < "$OUTPUT_FILE") bytes"
        echo "📖 Lines: $(wc -l < "$OUTPUT_FILE")"
        echo ""
        
        echo "🔍 First few lines of output:"
        echo "---"
        head -20 "$OUTPUT_FILE"
        echo "---"
        echo ""
        
        # Check for images
        if [ -d "scripts/images" ] && [ "$(ls -A scripts/images 2>/dev/null)" ]; then
            echo "🖼️  Images extracted to: scripts/images"
            echo "   $(ls scripts/images | wc -l) files found"
        else
            echo "ℹ️  No images extracted"
        fi
        
        # Check for metadata
        METADATA_FILE="${OUTPUT_FILE%.*}_metadata.json"
        if [ -f "$METADATA_FILE" ]; then
            echo "📋 Metadata saved to: $METADATA_FILE"
        fi
    else
        echo "⚠️  Output file not found"
    fi
else
    echo ""
    echo "❌ Conversion failed!"
    exit 1
fi 