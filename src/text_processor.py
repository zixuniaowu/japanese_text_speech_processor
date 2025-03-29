#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Japanese Text Processor
-----------------------
This module provides functionality for processing Japanese text files.
"""

import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class JapaneseTextProcessor:
    """Class for processing Japanese text files."""
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize the Japanese text processor.
        
        Args:
            data_dir: Path to the data directory
        """
        if data_dir is None:
            # Default to the data directory in the project structure
            self.data_dir = Path(__file__).parent.parent / 'data' / 'text'
        else:
            self.data_dir = Path(data_dir)
        
        logger.info(f"Initialized text processor with data directory: {self.data_dir}")
    
    def read_text_file(self, filename: str) -> str:
        """
        Read a Japanese text file.
        
        Args:
            filename: Name of the file to read
            
        Returns:
            The content of the file as a string
        """
        # 正确处理文件路径
        if os.path.isabs(filename):
            # 如果是绝对路径，直接使用
            file_path = Path(filename)
        else:
            # 如果是相对路径，基于data_dir构建
            file_path = self.data_dir / filename
        
        logger.info(f"Reading text file: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise
    
    def read_markdown_file(self, filename: str) -> Dict[str, Union[str, List[str]]]:
        """
        Read a Japanese markdown file and extract structure.
        
        Args:
            filename: Name of the markdown file to read
            
        Returns:
            A dictionary with the structure of the markdown file
        """
        content = self.read_text_file(filename)
        
        # Extract headers
        headers = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
        
        # Extract lists
        bullet_lists = re.findall(r'^\s*[-*+]\s+(.+)$', content, re.MULTILINE)
        numbered_lists = re.findall(r'^\s*\d+\.\s+(.+)$', content, re.MULTILINE)
        
        # Extract code blocks
        code_blocks = re.findall(r'```(?:\w+)?\n([\s\S]*?)```', content)
        
        structure = {
            "raw_content": content,
            "headers": [(len(h[0]), h[1]) for h in headers],
            "bullet_lists": bullet_lists,
            "numbered_lists": numbered_lists,
            "code_blocks": code_blocks
        }
        
        return structure
    
    def write_text_file(self, filename: str, content: str) -> None:
        """
        Write content to a Japanese text file.
        
        Args:
            filename: Name of the file to write
            content: Content to write to the file
        """
        # 正确处理文件路径
        if os.path.isabs(filename):
            # 如果是绝对路径，直接使用
            file_path = Path(filename)
        else:
            # 如果是相对路径，基于data_dir构建
            file_path = self.data_dir / filename
        
        logger.info(f"Writing text file: {file_path}")
        
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Successfully wrote content to {file_path}")
        except Exception as e:
            logger.error(f"Error writing to file {file_path}: {e}")
            raise

    def export_to_json(self, text_data: Dict, output_file: str) -> None:
        """
        Export text data to JSON format.
        
        Args:
            text_data: Dictionary of text data to export
            output_file: Name of the output JSON file
        """
        # 正确处理文件路径
        if os.path.isabs(output_file):
            file_path = Path(output_file)
        else:
            # 使用项目的processed目录
            file_path = Path(self.data_dir).parent / 'processed' / output_file
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(text_data, f, ensure_ascii=False, indent=2)
            logger.info(f"Successfully exported data to {file_path}")
        except Exception as e:
            logger.error(f"Error exporting to JSON {file_path}: {e}")
            raise

# Example usage
if __name__ == "__main__":
    processor = JapaneseTextProcessor()
    
    # Read and print a sample text file
    try:
        content = processor.read_text_file("sample_japanese.txt")
        print("Sample Text Content:")
        print(content)
        print("-" * 40)
        
        # Read and extract structure from a markdown file
        md_structure = processor.read_markdown_file("sample_japanese.md")
        print("Markdown Structure:")
        print(json.dumps(md_structure, ensure_ascii=False, indent=2))
    except Exception as e:
        logger.error(f"Error in example: {e}")
