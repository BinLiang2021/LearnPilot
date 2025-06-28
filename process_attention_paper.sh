#!/bin/bash
export PYTHONPATH=.:$PYTHONPATH
# PDF to Markdown Conversion Script
# Process the Attention Is All You Need paper

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
PDF_FILE="scripts/1706.03762v7.Attention_Is_All_You_Need.pdf"
OUTPUT_FILE="scripts/1706.03762v7.Attention_Is_All_You_Need.md"
IMAGE_DIR="scripts/images"
CONVERTER_SCRIPT="src/learn_pilot/literature_utils/knowledge_parser/pdf_to_markdown.py"

echo -e "${BLUE}🔄 PDF to Markdown Conversion Script - Marker Edition${NC}"
echo -e "${BLUE}====================================================${NC}"
echo ""

# Function to print status messages
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Check if PDF file exists
if [ ! -f "$PDF_FILE" ]; then
    print_error "PDF file not found: $PDF_FILE"
    echo "Please make sure the Attention Is All You Need paper is available at this path."
    exit 1
fi

# Check if converter script exists
if [ ! -f "$CONVERTER_SCRIPT" ]; then
    print_error "Converter script not found: $CONVERTER_SCRIPT"
    exit 1
fi

# Display configuration
print_status "Configuration:"
echo "  📄 Input PDF: $PDF_FILE"
echo "  📝 Output MD: $OUTPUT_FILE"
echo "  🖼️  Image Dir: $IMAGE_DIR"
echo "  🔧 Converter: $CONVERTER_SCRIPT"
echo ""

# Create output directory for images
print_status "Creating output directories..."
mkdir -p "$(dirname "$OUTPUT_FILE")"
mkdir -p "$IMAGE_DIR"

# Get PDF info
if command -v pdfinfo >/dev/null 2>&1; then
    print_status "PDF Information:"
    pdfinfo "$PDF_FILE" | head -10
    echo ""
fi

# Start conversion
print_status "Starting PDF to Markdown conversion..."
echo -e "${PURPLE}Using Marker - High-quality AI-powered conversion${NC}"
echo ""

# Record start time
START_TIME=$(date +%s)

# Run conversion with comprehensive options
python "$CONVERTER_SCRIPT" \
    --pdf-path "$PDF_FILE" \
    --output "$OUTPUT_FILE" \
    --image-dir "$IMAGE_DIR" \
    --format-lines \
    --output-format markdown \
    --force-ocr \
    2>&1 | tee conversion.log

# Check if conversion was successful
if [ $? -eq 0 ] && [ -f "$OUTPUT_FILE" ]; then
    # Calculate processing time
    END_TIME=$(date +%s)
    PROCESSING_TIME=$((END_TIME - START_TIME))
    
    print_success "Conversion completed successfully!"
    echo ""
    
    # Display results
    echo -e "${BLUE}📊 Conversion Results:${NC}"
    echo "⏱️  Processing time: ${PROCESSING_TIME} seconds"
    
    # File statistics
    FILE_SIZE=$(wc -c < "$OUTPUT_FILE")
    LINE_COUNT=$(wc -l < "$OUTPUT_FILE")
    WORD_COUNT=$(wc -w < "$OUTPUT_FILE")
    
    echo "📏 Output file size: ${FILE_SIZE} bytes"
    echo "📖 Lines: ${LINE_COUNT}"
    echo "🔤 Words: ${WORD_COUNT}"
    
    # Check for images
    if [ -d "$IMAGE_DIR" ] && [ "$(ls -A "$IMAGE_DIR" 2>/dev/null)" ]; then
        IMAGE_COUNT=$(ls "$IMAGE_DIR" | wc -l)
        echo "🖼️  Images extracted: ${IMAGE_COUNT} files"
        echo "   📂 Location: $IMAGE_DIR"
    else
        echo "ℹ️  No images extracted"
    fi
    
    # Check for metadata
    METADATA_FILE="${OUTPUT_FILE%.*}_metadata.json"
    if [ -f "$METADATA_FILE" ]; then
        echo "📋 Metadata saved: $METADATA_FILE"
        if command -v jq >/dev/null 2>&1; then
            echo "   📝 Preview:"
            jq -r '.pages // "N/A"' "$METADATA_FILE" | sed 's/^/     Pages: /'
            jq -r '.title // "N/A"' "$METADATA_FILE" | sed 's/^/     Title: /'
        fi
    fi
    
    echo ""
    echo -e "${BLUE}🔍 Content Preview (first 30 lines):${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    head -30 "$OUTPUT_FILE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Provide additional options
    echo -e "${BLUE}💡 Additional Options:${NC}"
    echo "• View full file: cat '$OUTPUT_FILE'"
    echo "• Open with editor: nano '$OUTPUT_FILE' or code '$OUTPUT_FILE'"
    echo "• View images: ls '$IMAGE_DIR'"
    if [ -f "$METADATA_FILE" ]; then
        echo "• View metadata: cat '$METADATA_FILE'"
    fi
    echo ""
    
    print_success "All done! The Attention Is All You Need paper has been converted to Markdown."
    
else
    print_error "Conversion failed!"
    if [ -f "conversion.log" ]; then
        echo ""
        echo "Error log:"
        tail -20 conversion.log
    fi
    exit 1
fi

# Clean up log file (optional)
if [ -f "conversion.log" ]; then
    print_status "Cleaning up temporary files..."
    rm conversion.log
fi

echo ""
echo -e "${GREEN}🎉 Script completed successfully!${NC}" 