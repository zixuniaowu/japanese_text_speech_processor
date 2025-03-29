#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple test script for pyttsx3
"""

import pyttsx3
import time

def test_tts():
    print("Initializing TTS engine...")
    engine = pyttsx3.init()
    
    # Print available voices
    voices = engine.getProperty('voices')
    print(f"Available voices: {len(voices)}")
    for i, voice in enumerate(voices):
        print(f"Voice {i}: ID={voice.id}, Name={voice.name}, Languages={voice.languages}")
    
    # Set properties
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    
    # Test with English text first
    print("\nTesting with English text...")
    engine.say("This is a test of the text to speech engine.")
    engine.runAndWait()
    time.sleep(1)
    
    # Test with Japanese text
    print("\nTesting with Japanese text...")
    engine.say("こんにちは、世界！")
    engine.runAndWait()
    time.sleep(1)
    
    # Save to file
    print("\nSaving to file...")
    output_file = "test_output.wav"
    engine.save_to_file("こんにちは、これはテストです。", output_file)
    engine.runAndWait()
    time.sleep(1)
    
    print(f"Test complete. Check if '{output_file}' was created.")

if __name__ == "__main__":
    test_tts()
