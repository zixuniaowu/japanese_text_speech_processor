#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Japanese Speech Processing Demo
------------------------------
A comprehensive demo script for Japanese text and speech processing.
"""

import os
import sys
import time
from pathlib import Path

# Add the parent directory to the path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from src.text_processor import JapaneseTextProcessor
from src.speech_processor import JapaneseSpeechProcessor
from src.japanese_phonetics import JapanesePhoneticConverter

def main():
    """Run a comprehensive demo of Japanese speech processing."""
    print("日本語音声処理デモ")
    print("=" * 60)
    
    # Initialize processors
    text_dir = parent_dir / "data" / "text"
    audio_dir = parent_dir / "data" / "audio"
    
    text_processor = JapaneseTextProcessor(str(text_dir))
    speech_processor = JapaneseSpeechProcessor(str(audio_dir))
    phonetic_converter = JapanesePhoneticConverter()
    
    # Create demo directories
    demo_text_dir = parent_dir / "data" / "demo" / "text"
    demo_audio_dir = parent_dir / "data" / "demo" / "audio"
    
    os.makedirs(demo_text_dir, exist_ok=True)
    os.makedirs(demo_audio_dir, exist_ok=True)
    
    # 1. Sample Japanese phrases for TTS demo
    print("\n1. 音声合成のデモ（Text-to-Speech）")
    print("-" * 60)
    
    phrases = [
        {
            "text": "こんにちは、私は音声合成システムです。",
            "description": "基本的な挨拶（Basic greeting）",
            "filename": "greeting.wav"
        },
        {
            "text": "日本語の音声処理技術は、自然言語処理の一部です。",
            "description": "技術的な文（Technical statement）",
            "filename": "technical.wav"
        },
        {
            "text": "桜の花が春風に舞い散る様子は、とても美しいです。",
            "description": "描写的な文（Descriptive sentence）",
            "filename": "descriptive.wav"
        },
        {
            "text": "AI（人工知能）は、私たちの生活を大きく変えつつあります。",
            "description": "カタカナと記号を含む文（Sentence with katakana and symbols）",
            "filename": "mixed.wav"
        }
    ]
    
    # Process each phrase
    for i, phrase in enumerate(phrases):
        print(f"\n{i+1}. {phrase['description']}:")
        print(f"   テキスト: {phrase['text']}")
        
        # Convert text to different forms
        hiragana = phonetic_converter.to_hiragana(phrase['text'])
        romaji = phonetic_converter.to_romaji(phrase['text'])
        
        print(f"   ひらがな: {hiragana}")
        print(f"   ローマ字: {romaji}")
        
        # Save text to file
        text_file = f"demo_{i+1}.txt"
        text_path = demo_text_dir / text_file
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(phrase['text'] + "\n\n")
            f.write(f"ひらがな: {hiragana}\n")
            f.write(f"ローマ字: {romaji}\n")
        
        # Convert to speech
        audio_file = demo_audio_dir / phrase['filename']
        print(f"   音声ファイルを生成中: {phrase['filename']}...")
        
        # Generate speech
        speech_processor.text_to_speech(phrase['text'], str(audio_file))
        
        # Analyze the audio
        audio_properties = speech_processor.analyze_audio(str(audio_file))
        print(f"   音声ファイル分析:")
        print(f"     長さ: {audio_properties.get('duration', 'N/A'):.2f} 秒")
        print(f"     テンポ: {audio_properties.get('tempo', 'N/A'):.1f} BPM")
    
    # 2. Text analysis with tokenization
    print("\n\n2. テキスト分析とトークン化")
    print("-" * 60)
    
    analysis_text = "自然言語処理は人工知能の重要な分野であり、機械翻訳や音声認識などに応用されています。"
    print(f"分析テキスト: {analysis_text}")
    
    # Tokenize the text
    tokens = phonetic_converter.tokenize(analysis_text)
    
    print("\nトークン化結果:")
    for i, token in enumerate(tokens):
        print(f"{i+1}. {token['surface']} ({token['part_of_speech']})")
        print(f"   基本形: {token['base_form']}")
        print(f"   読み方: {token['reading']}")
    
    # 3. Speech to text (if a real audio file exists)
    print("\n\n3. 音声認識のデモ（Speech-to-Text）")
    print("-" * 60)
    print("注意: この機能はインターネット接続を使用し、Google Speech Recognition APIを利用します。")
    
    # Use one of our generated audio files
    if os.path.exists(demo_audio_dir / "greeting.wav"):
        try:
            print("\n音声ファイルから文字起こしを行っています...")
            result = speech_processor.speech_to_text(str(demo_audio_dir / "greeting.wav"))
            print(f"認識結果: {result}")
        except Exception as e:
            print(f"音声認識中にエラーが発生しました: {e}")
    else:
        print("音声ファイルが存在しないため、音声認識をスキップします。")
    
    # 4. Comprehensive example
    print("\n\n4. 総合的な例: 長い日本語テキストの処理と音声合成")
    print("-" * 60)
    
    # Read a longer text from our sample file
    try:
        long_text = text_processor.read_text_file("sample_japanese.txt")
        print("サンプルテキスト（一部）:")
        print(long_text[:150] + "...")
        
        # Convert to speech
        long_audio_file = demo_audio_dir / "long_sample.wav"
        print(f"\n音声ファイルを生成中: {long_audio_file}...")
        speech_processor.text_to_speech(long_text, str(long_audio_file))
        
        # Analyze the generated audio
        long_audio_props = speech_processor.analyze_audio(str(long_audio_file))
        print(f"生成された音声ファイルの情報:")
        print(f"  長さ: {long_audio_props.get('duration', 'N/A'):.2f} 秒")
        print(f"  サンプルレート: {long_audio_props.get('sample_rate', 'N/A')} Hz")
        
    except Exception as e:
        print(f"長いテキストの処理中にエラーが発生しました: {e}")
    
    # Summary
    print("\n\nデモ完了")
    print("=" * 60)
    print(f"テキストファイルの保存先: {demo_text_dir}")
    print(f"音声ファイルの保存先: {demo_audio_dir}")
    print("=" * 60)

if __name__ == "__main__":
    main()
