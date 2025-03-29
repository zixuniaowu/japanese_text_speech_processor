#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Markdown to Speech Converter
---------------------------
This script converts Japanese Markdown text to speech.
"""

import os
import sys
import argparse
from pathlib import Path
import re

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from src.text_processor import JapaneseTextProcessor
from src.speech_processor_gtts import JapaneseSpeechProcessor

def clean_markdown(markdown_text):
    """
    Remove Markdown formatting to get clean text for speech synthesis.
    
    Args:
        markdown_text: Raw markdown text
        
    Returns:
        Clean text suitable for speech synthesis
    """
    # Remove code blocks
    text = re.sub(r'```.*?```', '', markdown_text, flags=re.DOTALL)
    
    # Remove headers
    text = re.sub(r'^#{1,6}\s+(.+)$', r'\1.', text, flags=re.MULTILINE)
    
    # Convert bullet points to sentences
    text = re.sub(r'^\s*[-*+]\s+(.+)$', r'\1.', text, flags=re.MULTILINE)
    
    # Convert numbered lists to sentences
    text = re.sub(r'^\s*\d+\.\s+(.+)$', r'\1.', text, flags=re.MULTILINE)
    
    # Remove formatting markers (bold, italic, etc.)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'__(.+?)__', r'\1', text)
    text = re.sub(r'_(.+?)_', r'\1', text)
    
    # Remove links but keep the text
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    
    # Remove images
    text = re.sub(r'!\[.+?\]\(.+?\)', '', text)
    
    # Convert multiple new lines to a single one
    text = re.sub(r'\n\s*\n', '\n', text)
    
    return text.strip()

def main():
    parser = argparse.ArgumentParser(
        description="Convert Japanese Markdown to speech",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('markdown_file', help='Path to the markdown file')
    parser.add_argument('--output', '-o', default='output.mp3', help='Output audio file')
    parser.add_argument('--clean', '-c', action='store_true', help='Output clean text file also')
    
    args = parser.parse_args()
    
    try:
        # Initialize processors
        text_processor = JapaneseTextProcessor()
        speech_processor = JapaneseSpeechProcessor()
        
        # Read markdown content
        print(f"Reading markdown file: {args.markdown_file}")
        markdown_content = text_processor.read_text_file(args.markdown_file)
        
        # Clean markdown to get plain text
        print("Processing markdown content...")
        clean_text = clean_markdown(markdown_content)
        
        # Optionally save the clean text
        if args.clean:
            clean_file = Path(args.output).with_suffix('.txt')
            with open(clean_file, 'w', encoding='utf-8') as f:
                f.write(clean_text)
            print(f"Clean text saved to: {clean_file}")
        
        # Convert to speech
        print(f"Converting to speech, output file: {args.output}")
        speech_processor.text_to_speech(clean_text, args.output)
        
        print("\nConversion completed successfully!")
        print(f"Output audio file: {args.output}")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
