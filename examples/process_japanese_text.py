#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example script demonstrating Japanese text processing.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the src modules
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from src.text_processor import JapaneseTextProcessor

def main():
    """Demonstrate Japanese text processing capabilities."""
    print("日本語テキスト処理の例")
    print("=" * 50)
    
    # 使用项目根目录下的data/text目录
    data_dir = parent_dir / "data" / "text"
    
    # Initialize the text processor
    processor = JapaneseTextProcessor(str(data_dir))
    
    # Path to sample files
    sample_text_file = "sample_japanese.txt"
    sample_md_file = "sample_japanese.md"
    
    # Process text file
    print("\n1. テキストファイルの読み込み:")
    print("-" * 50)
    try:
        content = processor.read_text_file(sample_text_file)
        print(content)
    except Exception as e:
        print(f"Error reading text file: {e}")
    
    # Process markdown file
    print("\n2. Markdownファイルの解析:")
    print("-" * 50)
    try:
        structure = processor.read_markdown_file(sample_md_file)
        
        print("見出し:")
        for level, text in structure['headers']:
            print(f"{'#' * level} {text}")
        
        print("\n箇条書きリスト:")
        for item in structure['bullet_lists']:
            print(f"- {item}")
        
        print("\n番号付きリスト:")
        for item in structure['numbered_lists']:
            print(f"- {item}")
        
        print(f"\nコードブロック数: {len(structure['code_blocks'])}")
        for i, block in enumerate(structure['code_blocks']):
            print(f"\nコードブロック {i+1}:")
            print(f"```\n{block}\n```")
        
    except Exception as e:
        print(f"Error processing markdown: {e}")
    
    # Create a new Japanese text file
    print("\n3. 新しい日本語テキストファイルの作成:")
    print("-" * 50)
    try:
        new_content = """
新しく作成した日本語のテキストファイルです。
これは例として作成されました。

日本語のテキスト処理には以下のような機能があります：
- テキストファイルの読み込み
- テキストファイルの書き込み
- Markdownファイルの構造解析
- JSONへのエクスポート

よろしくお願いします！
"""
        
        output_file = "example_output.txt"
        processor.write_text_file(output_file, new_content.strip())
        print(f"ファイル '{output_file}' を作成しました。")
        
        # Read back the file to verify
        content = processor.read_text_file(output_file)
        print("\n作成したファイルの内容:")
        print(content)
        
    except Exception as e:
        print(f"Error creating new text file: {e}")
    
    # Export data to JSON
    print("\n4. JSONへのエクスポート:")
    print("-" * 50)
    try:
        # Create the processed directory if it doesn't exist
        processed_dir = parent_dir / "data" / "processed"
        os.makedirs(processed_dir, exist_ok=True)
        
        # Sample data
        japanese_data = {
            "タイトル": "日本語サンプルデータ",
            "作成日": "2025年3月29日",
            "項目": ["テキスト処理", "音声処理", "言語分析"],
            "メタデータ": {
                "著者": "サンプル作成者",
                "バージョン": "1.0.0"
            }
        }
        
        # Export to JSON
        processor.export_to_json(japanese_data, "example_export.json")
        print(f"データをJSONにエクスポートしました。")
        
        # Print some sample data
        print("\nエクスポートされたデータのサンプル:")
        print(f"タイトル: {japanese_data['タイトル']}")
        print(f"作成日: {japanese_data['作成日']}")
        print(f"項目: {', '.join(japanese_data['項目'])}")
        
    except Exception as e:
        print(f"Error exporting to JSON: {e}")

if __name__ == "__main__":
    main()
