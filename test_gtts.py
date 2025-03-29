#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for gTTS (Google Text-to-Speech)
"""

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("gTTS not installed. Please install with: pip install gtts")

def test_gtts():
    if not GTTS_AVAILABLE:
        return
        
    print("Testing Google Text-to-Speech...")
    
    # Japanese text
    text = "こんにちは、世界！これは日本語のテキスト読み上げテストです。"
    
    print(f"Converting text: {text}")
    
    # Create gTTS object with Japanese language
    tts = gTTS(text=text, lang='ja')
    
    # Save to file
    output_file = "gtts_test.mp3"
    print(f"Saving to {output_file}...")
    tts.save(output_file)
    
    print(f"Test complete. Check if '{output_file}' was created.")
    print("Note: This requires an internet connection as it uses Google's servers.")

if __name__ == "__main__":
    test_gtts()
