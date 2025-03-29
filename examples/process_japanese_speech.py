#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example script demonstrating Japanese speech processing.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the src modules
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from src.speech_processor import JapaneseSpeechProcessor
from src.text_processor import JapaneseTextProcessor

def main():
    """Demonstrate Japanese speech processing capabilities."""
    print("日本語音声処理の例")
    print("=" * 50)
    
    # 使用绝对路径
    text_data_dir = parent_dir / "data" / "text"
    audio_data_dir = parent_dir / "data" / "audio"
    
    # Initialize the processors
    speech_processor = JapaneseSpeechProcessor(str(audio_data_dir))
    text_processor = JapaneseTextProcessor(str(text_data_dir))
    
    # Create necessary directories
    os.makedirs(audio_data_dir, exist_ok=True)
    
    # 1. Text-to-Speech conversion
    print("\n1. テキストから音声への変換:")
    print("-" * 50)
    try:
        # Read sample text
        sample_text = text_processor.read_text_file("sample_japanese.txt")
        print("入力テキスト:")
        print(sample_text[:200] + "..." if len(sample_text) > 200 else sample_text)
        
        # Convert to speech
        output_file = "example_tts_output.wav"
        speech_processor.text_to_speech(sample_text, output_file)
        print(f"\n音声ファイル '{output_file}' を作成しました。")
        print("注意: 実際の音声変換機能を使用するには、TTSライブラリをインストールする必要があります。")
        
    except Exception as e:
        print(f"Error in text-to-speech conversion: {e}")
    
    # 2. Speech analysis
    print("\n2. 音声ファイルの分析:")
    print("-" * 50)
    try:
        # Use the output file from the previous step as an example
        # In a real scenario, you would use an actual audio file
        audio_file = "example_tts_output.wav"
        
        # Analyze audio properties
        properties = speech_processor.analyze_audio(audio_file)
        
        print("音声ファイルのプロパティ:")
        for key, value in properties.items():
            print(f"  {key}: {value}")
        
        print("\n注意: 実際の音声分析機能を使用するには、librosaなどのライブラリをインストールする必要があります。")
        
    except Exception as e:
        print(f"Error analyzing audio: {e}")
    
    # 3. Speech-to-Text (STT) conversion
    print("\n3. 音声からテキストへの変換:")
    print("-" * 50)
    try:
        # In a real scenario, you would use an actual audio file
        audio_file = "example_tts_output.wav"
        
        # Convert speech to text
        transcribed_text = speech_processor.speech_to_text(audio_file)
        
        print("音声認識結果:")
        print(transcribed_text)
        
        print("\n注意: 実際の音声認識機能を使用するには、SpeechRecognitionなどのライブラリをインストールする必要があります。")
        
    except Exception as e:
        print(f"Error in speech-to-text conversion: {e}")
    
    # 4. Working with Japanese text and speech together
    print("\n4. 日本語テキストと音声の連携処理:")
    print("-" * 50)
    try:
        # Create a custom Japanese text
        japanese_text = """
音声合成の例文です。
この文章は音声に変換されます。
日本語のテキスト処理と音声処理の連携のテストです。
"""
        print("カスタムテキスト:")
        print(japanese_text)
        
        # Write to a file
        custom_file = "custom_japanese.txt"
        text_processor.write_text_file(custom_file, japanese_text.strip())
        
        # Convert to speech
        custom_audio = "custom_tts_output.wav"
        speech_processor.text_to_speech(japanese_text.strip(), custom_audio)
        
        print(f"\nテキストファイル '{custom_file}' と音声ファイル '{custom_audio}' を作成しました。")
        print("注意: 実際の機能を使用するには、追加のライブラリが必要です。")
        
    except Exception as e:
        print(f"Error in combined processing: {e}")

if __name__ == "__main__":
    main()
