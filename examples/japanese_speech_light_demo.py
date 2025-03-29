#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Japanese Speech Processing Demo (Light Version)
----------------------------------------------
A lightweight demo script that works without complex audio libraries.
"""

import os
import sys
import time
from pathlib import Path

# Add the parent directory to the path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from src.text_processor import JapaneseTextProcessor
from src.speech_processor_light import JapaneseSpeechProcessorLight

# Try to import the phonetics module, but handle gracefully if missing
try:
    from src.japanese_phonetics import JapanesePhoneticConverter
    PHONETICS_AVAILABLE = True
except ImportError:
    PHONETICS_AVAILABLE = False

def main():
    """Run a lightweight demo of Japanese speech processing."""
    print("日本語音声処理デモ (軽量版)")
    print("=" * 60)
    
    # Initialize processors
    text_dir = parent_dir / "data" / "text"
    audio_dir = parent_dir / "data" / "audio"
    
    text_processor = JapaneseTextProcessor(str(text_dir))
    speech_processor = JapaneseSpeechProcessorLight(str(audio_dir))
    
    # Initialize phonetic converter if available
    phonetic_converter = None
    if PHONETICS_AVAILABLE:
        try:
            phonetic_converter = JapanesePhoneticConverter()
            print("日本語音声変換モジュールが利用可能です。")
        except Exception as e:
            print(f"音声変換モジュールの初期化中にエラーが発生しました: {e}")
    else:
        print("注意: 日本語音声変換モジュールがインストールされていません。一部の機能は利用できません。")
    
    # Create demo directories
    demo_text_dir = parent_dir / "data" / "demo" / "text"
    demo_audio_dir = parent_dir / "data" / "demo" / "audio"
    
    os.makedirs(demo_text_dir, exist_ok=True)
    os.makedirs(demo_audio_dir, exist_ok=True)
    
    # 1. Sample Japanese phrases for TTS demo
    print("\n1. 音声合成のシミュレーション（Text-to-Speech Simulation）")
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
        }
    ]
    
    # Process each phrase
    for i, phrase in enumerate(phrases):
        print(f"\n{i+1}. {phrase['description']}:")
        print(f"   テキスト: {phrase['text']}")
        
        # Convert text to different forms if phonetics available
        if phonetic_converter:
            try:
                hiragana = phonetic_converter.to_hiragana(phrase['text'])
                romaji = phonetic_converter.to_romaji(phrase['text'])
                
                print(f"   ひらがな: {hiragana}")
                print(f"   ローマ字: {romaji}")
            except Exception as e:
                print(f"   テキスト変換中にエラーが発生しました: {e}")
        
        # Save text to file
        text_file = f"demo_{i+1}.txt"
        text_path = demo_text_dir / text_file
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(phrase['text'] + "\n")
            if phonetic_converter:
                try:
                    f.write(f"\nひらがな: {phonetic_converter.to_hiragana(phrase['text'])}\n")
                    f.write(f"ローマ字: {phonetic_converter.to_romaji(phrase['text'])}\n")
                except:
                    pass
        
        # Simulate converting to speech
        audio_file = demo_audio_dir / phrase['filename']
        print(f"   音声ファイルをシミュレート中: {phrase['filename']}...")
        
        # Generate speech simulation
        speech_processor.text_to_speech(phrase['text'], str(audio_file))
        
        # Analyze the simulated audio
        audio_properties = speech_processor.analyze_audio(str(audio_file))
        print(f"   シミュレートされた音声ファイル分析:")
        print(f"     シミュレートされた長さ: {audio_properties.get('duration', 'N/A'):.2f} 秒")
        print(f"     テキスト長: {audio_properties.get('text_length', 'N/A')} 文字")
    
    # 2. Read from a text file and convert to speech
    print("\n\n2. テキストファイルからの音声合成シミュレーション")
    print("-" * 60)
    
    try:
        # Read the sample Japanese text file
        content = text_processor.read_text_file("sample_japanese.txt")
        print("サンプルテキスト（一部）:")
        print(content[:150] + "...")
        
        # Convert to speech
        sample_audio_file = demo_audio_dir / "sample_japanese.wav"
        print(f"\n音声ファイルをシミュレート中: {sample_audio_file}...")
        
        speech_processor.text_to_speech(content, str(sample_audio_file))
        print("シミュレートされた音声ファイルが作成されました。")
        print(f"テキストファイル: {sample_audio_file.with_suffix('.txt')}")
        print(f"プレースホルダーオーディオファイル: {sample_audio_file}")
        
        # Simulated speech to text
        print("\n音声からテキストへの変換をシミュレート中...")
        recovered_text = speech_processor.speech_to_text(str(sample_audio_file))
        print("復元されたテキスト（一部）:")
        print(recovered_text[:150] + "..." if len(recovered_text) > 150 else recovered_text)
        
    except Exception as e:
        print(f"サンプルテキストの処理中にエラーが発生しました: {e}")
    
    # Summary
    print("\n\nデモ完了（軽量版）")
    print("=" * 60)
    print("注意: これはライブラリをインストールせずに音声処理をシミュレートする軽量版です。")
    print("実際の音声処理機能を使用するには、必要なライブラリをインストールしてください。")
    print(f"テキストファイルの保存先: {demo_text_dir}")
    print(f"シミュレートされた音声ファイルの保存先: {demo_audio_dir}")
    print("=" * 60)

if __name__ == "__main__":
    main()
