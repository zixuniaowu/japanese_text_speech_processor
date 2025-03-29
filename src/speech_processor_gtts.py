#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Japanese Speech Processor using Google Text-to-Speech
----------------------------------------------------
This module provides functionality for processing Japanese speech using Google TTS.
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, List, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    logger.warning("gTTS not available. Please install with: pip install gtts")

class JapaneseSpeechProcessor:
    """Class for processing Japanese speech using Google TTS."""
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize the Japanese speech processor.
        
        Args:
            data_dir: Path to the audio data directory
        """
        if data_dir is None:
            # Default to the audio directory in the project structure
            self.data_dir = Path(__file__).parent.parent / 'data' / 'audio'
        else:
            self.data_dir = Path(data_dir)
        
        logger.info(f"Initialized speech processor with data directory: {self.data_dir}")
        
        if not GTTS_AVAILABLE:
            logger.warning("Google TTS not available. Some functionality will be limited.")
            logger.warning("Install with: pip install gtts")
    
    def text_to_speech(self, text: str, output_file: str) -> None:
        """
        Convert Japanese text to speech using Google TTS.
        
        Args:
            text: Japanese text to convert to speech
            output_file: Path to save the audio file
        """
        logger.info(f"Converting text to speech: {text[:50]}...")
        
        # Check if it's already an absolute path
        if os.path.isabs(output_file):
            file_path = Path(output_file)
        else:
            file_path = self.data_dir / output_file
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        if GTTS_AVAILABLE:
            try:
                # Create gTTS object with Japanese language
                tts = gTTS(text=text, lang='ja', slow=False)
                
                # Determine output format (defaults to mp3 for gTTS)
                # If wav is requested, we'll still save as mp3 but with a note
                output_is_wav = file_path.suffix.lower() == '.wav'
                
                if output_is_wav:
                    # User wants WAV but gTTS creates MP3, so adjust the path
                    actual_path = file_path.with_suffix('.mp3')
                    logger.info(f"Note: gTTS can only create MP3 files. Saving to {actual_path} instead of {file_path}")
                else:
                    actual_path = file_path
                
                # Save the file
                tts.save(str(actual_path))
                logger.info(f"Successfully saved speech to {actual_path}")
                
                # Create a text file with the original content for reference
                text_file_path = file_path.with_suffix('.txt')
                with open(text_file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                logger.info(f"Saved original text to {text_file_path}")
                
                if output_is_wav:
                    # Create a note about the format conversion
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(f"Note: The audio for this text was saved as {actual_path}\n")
                        f.write("gTTS can only generate MP3 files, not WAV files.\n")
                        f.write(f"Original text: {text}\n")
                
            except Exception as e:
                logger.error(f"Error in text to speech conversion: {e}")
                self._create_placeholder(text, file_path)
        else:
            logger.warning("gTTS not available. Creating placeholder files.")
            self._create_placeholder(text, file_path)
    
    def _create_placeholder(self, text: str, file_path: Path) -> None:
        """
        Create placeholder files when gTTS is not available.
        
        Args:
            text: Text that would have been converted
            file_path: Path to save the placeholder
        """
        try:
            # Create a text file with the content
            text_file_path = file_path.with_suffix('.txt')
            with open(text_file_path, 'w', encoding='utf-8') as f:
                f.write(text)
                f.write("\n\n")
                f.write("--- This is a placeholder for text-to-speech output ---\n")
                f.write("--- To enable actual TTS, please install gTTS: ---\n")
                f.write("--- pip install gtts ---\n")
            
            # Create an empty file as a placeholder
            with open(file_path, 'w') as f:
                f.write("PLACEHOLDER AUDIO FILE\n")
                f.write("This file would contain audio in a real implementation.\n")
                f.write("Please install gTTS to generate actual audio: pip install gtts\n")
            
            logger.info(f"Created placeholder files at {text_file_path} and {file_path}")
        except Exception as e:
            logger.error(f"Error creating placeholder files: {e}")
    
    def speech_to_text(self, audio_file: str) -> str:
        """
        Placeholder for speech-to-text functionality.
        
        Note: Actual implementation would require additional libraries.
        
        Args:
            audio_file: Path to the audio file
            
        Returns:
            Placeholder message
        """
        # Check if it's already an absolute path
        if os.path.isabs(audio_file):
            file_path = Path(audio_file)
        else:
            file_path = self.data_dir / audio_file
            
        logger.info(f"Speech-to-text functionality is not implemented: {file_path}")
        
        # Try to find a text file with the same name
        text_file_path = file_path.with_suffix('.txt')
        if text_file_path.exists():
            try:
                with open(text_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract only the original text, not the placeholder message
                    if "---" in content:
                        content = content.split("---")[0].strip()
                    return content
            except Exception as e:
                logger.error(f"Error reading text file: {e}")
        
        return "音声認識機能は実装されていません。Speech-to-Text機能を使用するには、追加のライブラリが必要です。"
    
    def analyze_audio(self, audio_file: str) -> Dict[str, Union[float, List[float]]]:
        """
        Provide basic information about an audio file.
        
        Args:
            audio_file: Path to the audio file
            
        Returns:
            Dictionary of file properties
        """
        # Check if it's already an absolute path
        if os.path.isabs(audio_file):
            file_path = Path(audio_file)
        else:
            file_path = self.data_dir / audio_file
            
        logger.info(f"Analyzing audio file: {file_path}")
        
        # Check if file exists
        if not file_path.exists():
            mp3_path = file_path.with_suffix('.mp3')
            if mp3_path.exists():
                file_path = mp3_path
                logger.info(f"Found MP3 version instead: {file_path}")
            else:
                return {
                    "error": f"File not found: {file_path}",
                    "exists": False
                }
        
        # Get basic file information
        file_size = file_path.stat().st_size
        file_extension = file_path.suffix.lower()
        
        result = {
            "exists": True,
            "file_size_bytes": file_size,
            "file_extension": file_extension,
            "file_path": str(file_path)
        }
        
        # If it's a text placeholder, indicate that
        if file_extension == '.txt' or file_size < 1000:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    if "PLACEHOLDER" in content:
                        result["is_placeholder"] = True
                        result["note"] = "This is a placeholder file, not actual audio"
            except:
                pass
        
        # Check if there's a corresponding text file
        text_file_path = file_path.with_suffix('.txt')
        if text_file_path.exists():
            result["has_text_file"] = True
            try:
                with open(text_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Count lines and characters
                    result["text_lines"] = len(content.split('\n'))
                    result["text_length"] = len(content)
            except:
                pass
        
        # For MP3 files, try to get duration if mutagen is available
        if file_extension == '.mp3':
            try:
                from mutagen.mp3 import MP3
                audio = MP3(file_path)
                result["duration_seconds"] = audio.info.length
                result["bitrate"] = audio.info.bitrate
                result["sample_rate"] = audio.info.sample_rate
            except ImportError:
                result["note"] = "Install mutagen for MP3 file analysis: pip install mutagen"
            except Exception as e:
                result["error"] = f"Error analyzing MP3: {str(e)}"
        
        return result

# Example usage
if __name__ == "__main__":
    processor = JapaneseSpeechProcessor()
    
    # Example TTS conversion
    sample_text = "こんにちは、これは日本語のテキスト読み上げテストです。"
    processor.text_to_speech(sample_text, "gtts_example.mp3")
    
    # Analyze the generated file
    audio_properties = processor.analyze_audio("gtts_example.mp3")
    print("Audio Properties:")
    for key, value in audio_properties.items():
        print(f"  {key}: {value}")
