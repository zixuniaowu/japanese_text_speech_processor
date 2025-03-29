#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Japanese Text and Speech Processor
---------------------------------
Main application entry point using Google TTS as the primary speech engine.
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add the src directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

from src.text_processor import JapaneseTextProcessor
from src.speech_processor_gtts import JapaneseSpeechProcessor

# Try to import phonetics module, handle gracefully if missing
try:
    from src.japanese_phonetics import JapanesePhoneticConverter
    PHONETICS_AVAILABLE = True
except ImportError:
    PHONETICS_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_text(args):
    """Process Japanese text files."""
    # 使用绝对路径
    data_dir = None
    if args.data_dir:
        data_dir = args.data_dir
    else:
        # 默认使用项目根目录下的data/text目录
        data_dir = str(Path(__file__).parent / "data" / "text")
    
    processor = JapaneseTextProcessor(data_dir)
    
    if args.read:
        try:
            # 直接传递文件名或路径，JapaneseTextProcessor会处理路径逻辑
            content = processor.read_text_file(args.read)
            print(f"\n{'=' * 40}\n{content}\n{'=' * 40}\n")
        except Exception as e:
            logger.error(f"Error reading text file: {e}")
    
    if args.read_markdown:
        try:
            # 直接传递文件名或路径，JapaneseTextProcessor会处理路径逻辑
            structure = processor.read_markdown_file(args.read_markdown)
            print(f"\nMarkdown Structure:\n{'-' * 40}")
            print(f"Headers: {len(structure['headers'])}")
            for level, text in structure['headers']:
                print(f"{'#' * level} {text}")
            
            print(f"\nLists:")
            if structure['bullet_lists']:
                print("Bullet Lists:")
                for item in structure['bullet_lists']:
                    print(f"- {item}")
            
            if structure['numbered_lists']:
                print("\nNumbered Lists:")
                for i, item in enumerate(structure['numbered_lists']):
                    print(f"{i+1}. {item}")
                
            if structure['code_blocks']:
                print(f"\nCode Blocks: {len(structure['code_blocks'])}")
                for i, block in enumerate(structure['code_blocks']):
                    print(f"\nBlock {i+1}:")
                    print(f"```\n{block}\n```")
        except Exception as e:
            logger.error(f"Error processing markdown: {e}")
    
    if args.convert:
        if not PHONETICS_AVAILABLE:
            print("警告: 日本語音声変換モジュールがインストールされていません。")
            print("テキスト変換機能を使用するには、以下のパッケージをインストールしてください:")
            print("pip install janome pykakasi")
            return
            
        try:
            # Initialize the phonetic converter
            converter = JapanesePhoneticConverter()
            
            # Read the input text
            if os.path.exists(args.convert):
                text = processor.read_text_file(args.convert)
            else:
                text = args.convert  # Assume it's direct text input
            
            print(f"\nOriginal text: {text}")
            
            # Perform conversions
            if args.to_hiragana:
                try:
                    hiragana = converter.to_hiragana(text)
                    print(f"\nHiragana: {hiragana}")
                except Exception as e:
                    print(f"Error converting to hiragana: {e}")
            
            if args.to_romaji:
                try:
                    romaji = converter.to_romaji(text)
                    print(f"\nRomaji: {romaji}")
                except Exception as e:
                    print(f"Error converting to romaji: {e}")
            
            if args.to_katakana:
                try:
                    katakana = converter.to_katakana(text)
                    print(f"\nKatakana: {katakana}")
                except Exception as e:
                    print(f"Error converting to katakana: {e}")
            
            if args.tokenize:
                try:
                    tokens = converter.tokenize(text)
                    print("\nTokenization:")
                    for i, token in enumerate(tokens):
                        print(f"{i+1}. {token['surface']} ({token.get('part_of_speech', 'unknown')})")
                        if 'reading' in token:
                            print(f"   Reading: {token['reading']}")
                        if 'base_form' in token:
                            print(f"   Base form: {token['base_form']}")
                except Exception as e:
                    print(f"Error tokenizing text: {e}")
        except Exception as e:
            logger.error(f"Error converting text: {e}")

def process_speech(args):
    """Process Japanese speech files."""
    # 使用绝对路径
    data_dir = None
    if args.data_dir:
        data_dir = args.data_dir
    else:
        # 默认使用项目根目录下的data/audio目录
        data_dir = str(Path(__file__).parent / "data" / "audio")
    
    processor = JapaneseSpeechProcessor(data_dir)
    
    if args.text_to_speech:
        try:
            input_path = args.text_to_speech
            
            # Check if it's a file or direct text
            if os.path.exists(input_path):
                # It's a file
                with open(input_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                logger.info(f"Read text from file: {input_path}")
            else:
                # It's direct text
                text = input_path
                logger.info("Using direct text input")
            
            # 生成默认输出文件名（如果未提供）
            if args.output:
                output_file = args.output
            else:
                if os.path.exists(input_path):
                    # Default to using MP3 extension for gTTS
                    output_file = f"{Path(input_path).stem}.mp3"
                else:
                    output_file = "output.mp3"
            
            # 转换为语音
            processor.text_to_speech(text, output_file)
            print(f"Text-to-speech conversion completed using Google TTS.")
            print(f"Output saved to: {output_file}")
            
        except Exception as e:
            logger.error(f"Error in text-to-speech conversion: {e}")
    
    if args.analyze_audio:
        try:
            properties = processor.analyze_audio(args.analyze_audio)
            print(f"\nAudio Properties:")
            for key, value in properties.items():
                print(f"  {key}: {value}")
        except Exception as e:
            logger.error(f"Error analyzing audio: {e}")
    
    if args.speech_to_text:
        try:
            text = processor.speech_to_text(args.speech_to_text)
            print(f"\nTranscribed Text:")
            print(text)
            print("\nNote: This is not actual speech recognition.")
            print("The text is retrieved from the corresponding .txt file if available.")
        except Exception as e:
            logger.error(f"Error in speech-to-text conversion: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Process Japanese text and speech files using Google TTS",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Global options
    parser.add_argument("--data-dir", help="Path to data directory")
    
    # Create subparsers for text and speech
    subparsers = parser.add_subparsers(title="commands", dest="command")
    
    # Text processing
    text_parser = subparsers.add_parser("text", help="Process Japanese text")
    text_parser.add_argument("--read", help="Read and display a text file")
    text_parser.add_argument("--read-markdown", help="Read and analyze a markdown file")
    text_parser.add_argument("--convert", help="Convert text (file path or direct text)")
    text_parser.add_argument("--to-hiragana", action="store_true", help="Convert to hiragana")
    text_parser.add_argument("--to-romaji", action="store_true", help="Convert to romaji")
    text_parser.add_argument("--to-katakana", action="store_true", help="Convert to katakana")
    text_parser.add_argument("--tokenize", action="store_true", help="Tokenize the text")
    
    # Speech processing
    speech_parser = subparsers.add_parser("speech", help="Process Japanese speech")
    speech_parser.add_argument("--text-to-speech", help="Convert text or text file to speech")
    speech_parser.add_argument("--analyze-audio", help="Analyze an audio file")
    speech_parser.add_argument("--speech-to-text", help="Convert speech to text")
    speech_parser.add_argument("--output", help="Output file for text-to-speech")
    
    # Demo command
    demo_parser = subparsers.add_parser("demo", help="Run demonstration")
    demo_parser.add_argument("--speech", action="store_true", help="Run speech processing demo")
    demo_parser.add_argument("--text", action="store_true", help="Run text processing demo")
    
    args = parser.parse_args()
    
    if args.command == "text":
        process_text(args)
    elif args.command == "speech":
        process_speech(args)
    elif args.command == "demo":
        # Choose appropriate demo script
        if args.speech:
            try:
                # Create a simple speech demo directly here
                processor = JapaneseSpeechProcessor()
                text_processor = JapaneseTextProcessor()
                
                print("\n日本語音声処理デモ (Google TTS使用)")
                print("=" * 60)
                
                # Sample text
                sample_text = "こんにちは、これは日本語のテキスト読み上げデモです。Google TTSを使用しています。"
                print(f"サンプルテキスト: {sample_text}")
                
                # Convert to speech
                output_file = "demo_output.mp3"
                print(f"音声ファイルを生成中: {output_file}")
                processor.text_to_speech(sample_text, output_file)
                
                # Also try with a longer sample text
                try:
                    long_text = text_processor.read_text_file("sample_japanese.txt")
                    long_output = "demo_long.mp3"
                    print(f"サンプルファイルから音声を生成中: {long_output}")
                    processor.text_to_speech(long_text[:500], long_output)  # First 500 chars for demo
                except Exception as e:
                    print(f"サンプルファイル処理中にエラーが発生しました: {e}")
                
                print("\nデモ完了！生成されたMP3ファイルを再生してください。")
                print("=" * 60)
                
            except Exception as e:
                logger.error(f"Error running speech demo: {e}")
        elif args.text:
            try:
                demo_path = Path(__file__).parent / "examples" / "process_japanese_text.py"
                os.system(f"{sys.executable} {demo_path}")
            except Exception as e:
                logger.error(f"Error running text demo: {e}")
        else:
            print("Please specify --speech or --text for the demo command")
            demo_parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
