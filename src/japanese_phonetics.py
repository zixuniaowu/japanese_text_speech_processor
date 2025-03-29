#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Japanese Phonetics Converter
---------------------------
This module provides functionality for converting Japanese text to phonetic forms
(hiragana, katakana, romaji) which can be useful for speech processing.
"""

import logging
from typing import Dict, List, Optional

try:
    from janome.tokenizer import Tokenizer
    JANOME_AVAILABLE = True
except ImportError:
    JANOME_AVAILABLE = False
    
try:
    import pykakasi
    KAKASI_AVAILABLE = True
except ImportError:
    KAKASI_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class JapanesePhoneticConverter:
    """Class for converting Japanese text to various phonetic forms."""
    
    def __init__(self):
        """Initialize the Japanese phonetic converter."""
        # Initialize Janome tokenizer if available
        if JANOME_AVAILABLE:
            self.tokenizer = Tokenizer()
            logger.info("Janome tokenizer initialized")
        else:
            self.tokenizer = None
            logger.warning("Janome not available. Some functionality will be limited.")
        
        # Initialize kakasi converter if available
        if KAKASI_AVAILABLE:
            self.kakasi = pykakasi.kakasi()
            self.kakasi_conv = self.kakasi.getConverter()
            logger.info("Kakasi converter initialized")
        else:
            self.kakasi_conv = None
            logger.warning("Pykakasi not available. Some functionality will be limited.")
    
    def to_hiragana(self, text: str) -> str:
        """
        Convert Japanese text to hiragana.
        
        Args:
            text: Japanese text that may contain kanji and katakana
            
        Returns:
            Text converted to hiragana
        """
        if not text:
            return ""
            
        if self.tokenizer:
            # Use Janome for accurate kanji to hiragana conversion
            result = ""
            for token in self.tokenizer.tokenize(text):
                result += token.reading
            return result
        elif self.kakasi_conv:
            # Use kakasi as fallback
            result = self.kakasi_conv.do(text)
            return result.get('hira', text)
        else:
            logger.warning("No conversion libraries available. Returning original text.")
            return text
    
    def to_romaji(self, text: str) -> str:
        """
        Convert Japanese text to romaji (Latin alphabet).
        
        Args:
            text: Japanese text
            
        Returns:
            Text converted to romaji
        """
        if not text:
            return ""
            
        if self.kakasi_conv:
            result = self.kakasi_conv.do(text)
            return result.get('hepburn', text)
        else:
            logger.warning("Pykakasi not available for romaji conversion. Returning original text.")
            return text
    
    def to_katakana(self, text: str) -> str:
        """
        Convert Japanese text to katakana.
        
        Args:
            text: Japanese text
            
        Returns:
            Text converted to katakana
        """
        if not text:
            return ""
            
        if self.kakasi_conv:
            result = self.kakasi_conv.do(text)
            return result.get('kana', text)
        else:
            logger.warning("Pykakasi not available for katakana conversion. Returning original text.")
            return text
    
    def tokenize(self, text: str) -> List[Dict[str, str]]:
        """
        Tokenize Japanese text and provide detailed information.
        
        Args:
            text: Japanese text
            
        Returns:
            List of tokens with their information
        """
        if not text:
            return []
            
        if self.tokenizer:
            result = []
            for token in self.tokenizer.tokenize(text):
                token_info = {
                    'surface': token.surface,
                    'base_form': token.base_form,
                    'reading': token.reading,
                    'part_of_speech': token.part_of_speech.split(',')[0]
                }
                result.append(token_info)
            return result
        else:
            logger.warning("Janome not available for tokenization.")
            return [{'surface': text, 'error': 'Tokenizer not available'}]

# Example usage
if __name__ == "__main__":
    converter = JapanesePhoneticConverter()
    
    sample_text = "日本語の音声処理は難しいです。"
    print(f"Original text: {sample_text}")
    
    # Convert to different forms
    hiragana = converter.to_hiragana(sample_text)
    print(f"Hiragana: {hiragana}")
    
    romaji = converter.to_romaji(sample_text)
    print(f"Romaji: {romaji}")
    
    katakana = converter.to_katakana(sample_text)
    print(f"Katakana: {katakana}")
    
    # Tokenize
    tokens = converter.tokenize(sample_text)
    print("\nTokenization:")
    for token in tokens:
        print(f"  {token['surface']} ({token['part_of_speech']}): {token['reading']}")
