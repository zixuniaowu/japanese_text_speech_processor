#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the Japanese Text Processor.
"""

import os
import sys
import unittest
from pathlib import Path

# Add the parent directory to the path so we can import the src modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.text_processor import JapaneseTextProcessor

class TestJapaneseTextProcessor(unittest.TestCase):
    """Test cases for the JapaneseTextProcessor class."""
    
    def setUp(self):
        """Set up the test environment."""
        # Create a test data directory in the tests folder
        self.test_data_dir = Path(__file__).parent / 'test_data'
        os.makedirs(self.test_data_dir, exist_ok=True)
        
        # Create a test text file
        self.test_file = self.test_data_dir / 'test_japanese.txt'
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write("これはテストです。\n日本語の処理をテストします。")
        
        # Create a test markdown file
        self.test_md_file = self.test_data_dir / 'test_japanese.md'
        with open(self.test_md_file, 'w', encoding='utf-8') as f:
            f.write("# テスト見出し\n\n- リスト項目1\n- リスト項目2\n\n```\nコードブロック\n```")
        
        # Initialize the processor with the test data directory
        self.processor = JapaneseTextProcessor(str(self.test_data_dir))
    
    def tearDown(self):
        """Clean up after the tests."""
        # Option to remove test files if needed
        # import shutil
        # shutil.rmtree(self.test_data_dir)
        pass
    
    def test_read_text_file(self):
        """Test reading a Japanese text file."""
        content = self.processor.read_text_file('test_japanese.txt')
        self.assertEqual(content, "これはテストです。\n日本語の処理をテストします。")
    
    def test_read_markdown_file(self):
        """Test reading a Japanese markdown file."""
        structure = self.processor.read_markdown_file('test_japanese.md')
        
        # Check headers
        self.assertEqual(len(structure['headers']), 1)
        self.assertEqual(structure['headers'][0], (1, "テスト見出し"))
        
        # Check lists
        self.assertEqual(len(structure['bullet_lists']), 2)
        self.assertIn("リスト項目1", structure['bullet_lists'])
        self.assertIn("リスト項目2", structure['bullet_lists'])
        
        # Check code blocks
        self.assertEqual(len(structure['code_blocks']), 1)
        self.assertEqual(structure['code_blocks'][0], "コードブロック")
    
    def test_write_text_file(self):
        """Test writing Japanese text to a file."""
        test_content = "これは書き込みテストです。"
        output_file = "test_output.txt"
        
        self.processor.write_text_file(output_file, test_content)
        
        # Verify the file was written correctly
        file_path = self.test_data_dir / output_file
        self.assertTrue(file_path.exists())
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertEqual(content, test_content)
    
    def test_export_to_json(self):
        """Test exporting Japanese text data to JSON."""
        # Create the required directory
        export_dir = self.test_data_dir.parent / 'processed'
        os.makedirs(export_dir, exist_ok=True)
        
        test_data = {
            "title": "テストデータ",
            "content": ["項目1", "項目2"],
            "metadata": {
                "author": "テスト作者",
                "date": "2025-03-29"
            }
        }
        
        output_file = "test_export.json"
        
        # Override the default export directory for testing
        self.processor.data_dir = Path(self.test_data_dir).parent
        
        # Export the data
        self.processor.export_to_json(test_data, output_file)
        
        # Verify the file was written correctly
        file_path = export_dir / output_file
        self.assertTrue(file_path.exists())
        
        # Check JSON content
        import json
        with open(file_path, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        self.assertEqual(loaded_data, test_data)


if __name__ == "__main__":
    unittest.main()
