#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for multiple TTS engines
"""

import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from src.speech_processor_multi import JapaneseSpeechProcessorMulti, PYTTSX3_AVAILABLE, GTTS_AVAILABLE

def test_all_engines():
    """Test all available TTS engines."""
    print("Testing multiple TTS engines for Japanese speech processing")
    print("=" * 60)
    
    # Print availability
    print(f"pyttsx3 available: {PYTTSX3_AVAILABLE}")
    print(f"gTTS available: {GTTS_AVAILABLE}")
    
    # Test text
    test_text = "こんにちは、これは音声合成のテストです。日本語でテキストを読み上げます。"
    print(f"\nTest text: {test_text}")
    
    # Test with different engines
    engines = []
    if PYTTSX3_AVAILABLE:
        engines.append('pyttsx3')
    if GTTS_AVAILABLE:
        engines.append('gtts')
    engines.append('auto')  # Always test auto mode
    
    for engine_name in engines:
        print(f"\n{'-' * 40}")
        print(f"Testing engine: {engine_name}")
        
        # Initialize processor with specific engine
        processor = JapaneseSpeechProcessorMulti(engine=engine_name)
        
        # Generate output filename
        output_file = f"test_{engine_name}.wav"
        
        # Convert text to speech
        success, message = processor.text_to_speech(test_text, output_file)
        print(f"Result: {'Success' if success else 'Failed'}")
        print(f"Message: {message}")
        
        # Analyze the output file
        props = processor.analyze_audio(output_file)
        print("File properties:")
        for key, value in props.items():
            print(f"  {key}: {value}")
    
    # Summary
    print("\n" + "=" * 60)
    print("Test completed.")
    print("Check the generated audio files in the data/audio directory.")

if __name__ == "__main__":
    test_all_engines()
