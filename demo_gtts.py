#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Google TTS Demo for Japanese Text
--------------------------------
A demo script showcasing Google Text-to-Speech for Japanese.
"""

import os
import sys
from pathlib import Path
import time

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("gTTS not available. Please install with: pip install gtts")
    print("This demo requires an internet connection.")
    sys.exit(1)

from src.text_processor import JapaneseTextProcessor

def main():
    """Run a Google TTS demo for Japanese text."""
    print("日本語 Google Text-to-Speech デモ")
    print("=" * 60)
    print("注意: このデモにはインターネット接続が必要です。")
    
    # Create output directory
    output_dir = Path(__file__).parent / "data" / "demo" / "gtts"
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize text processor
    text_processor = JapaneseTextProcessor()
    
    # Demo phrases
    phrases = [
        {
            "text": "こんにちは、世界！",
            "description": "基本的な挨拶 (Basic greeting)",
            "filename": "hello_world.mp3"
        },
        {
            "text": "日本語のテキスト読み上げデモンストレーションです。",
            "description": "デモの説明 (Demo description)",
            "filename": "demo_description.mp3"
        },
        {
            "text": "桜の花が春風に舞い散る様子は、とても美しいです。",
            "description": "詩的な文 (Poetic sentence)",
            "filename": "poetic.mp3"
        },
        {
            "text": "AIを活用した音声合成技術は、日々進化しています。",
            "description": "技術的な文 (Technical sentence)",
            "filename": "technical.mp3"
        }
    ]
    
    # Process each phrase
    for i, phrase in enumerate(phrases):
        print(f"\n{i+1}. {phrase['description']}:")
        print(f"   テキスト: {phrase['text']}")
        
        # Convert to speech
        output_path = output_dir / phrase['filename']
        print(f"   MP3ファイルを生成中: {output_path}")
        
        try:
            # Create gTTS object with Japanese language
            tts = gTTS(text=phrase['text'], lang='ja', slow=False)
            
            # Save to file
            tts.save(str(output_path))
            print(f"   生成完了: {output_path}")
            
            # Save text file for reference
            text_path = output_path.with_suffix('.txt')
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(phrase['text'])
            
        except Exception as e:
            print(f"   エラーが発生しました: {e}")
    
    # Try with a sample file if available
    print("\nサンプルファイルからの変換:")
    print("-" * 60)
    
    try:
        sample_text = text_processor.read_text_file("sample_japanese.txt")
        # Limit the length for the demo
        if len(sample_text) > 500:
            demo_text = sample_text[:500] + "..."
        else:
            demo_text = sample_text
            
        print(f"サンプルテキスト（一部）: \n{demo_text[:200]}...")
        
        sample_output = output_dir / "sample_japanese.mp3"
        print(f"MP3ファイルを生成中: {sample_output}")
        
        tts = gTTS(text=demo_text, lang='ja', slow=False)
        tts.save(str(sample_output))
        
        print(f"生成完了: {sample_output}")
        
    except Exception as e:
        print(f"サンプルファイル処理中にエラーが発生しました: {e}")
    
    # Summary
    print("\nデモ完了！")
    print("=" * 60)
    print(f"生成されたファイルの保存先: {output_dir}")
    print("各MP3ファイルを再生して、音声合成の結果を確認してください。")

if __name__ == "__main__":
    main()
