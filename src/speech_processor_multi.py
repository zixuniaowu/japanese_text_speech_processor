#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Japanese Speech Processor with Multiple TTS Engines
--------------------------------------------------
This module provides functionality for processing Japanese speech using multiple TTS engines.
"""

import os
import logging
import time
from pathlib import Path
from typing import Optional, Dict, List, Union, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to import different TTS engines
PYTTSX3_AVAILABLE = False
GTTS_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
    logger.info("pyttsx3 is available")
except ImportError:
    logger.warning("pyttsx3 not available")

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
    logger.info("gTTS is available")
except ImportError:
    logger.warning("gTTS not available (requires internet connection)")

class JapaneseSpeechProcessorMulti:
    """Class for processing Japanese speech using multiple TTS engines."""
    
    def __init__(self, data_dir: Optional[str] = None, engine: str = 'auto'):
        """
        Initialize the Japanese speech processor.
        
        Args:
            data_dir: Path to the audio data directory
            engine: TTS engine to use ('pyttsx3', 'gtts', 'auto')
        """
        if data_dir is None:
            # Default to the audio directory in the project structure
            self.data_dir = Path(__file__).parent.parent / 'data' / 'audio'
        else:
            self.data_dir = Path(data_dir)
        
        logger.info(f"Initialized speech processor with data directory: {self.data_dir}")
        
        # Initialize TTS engines
        self.pyttsx3_engine = None
        self.engine_type = engine
        
        # Try to initialize pyttsx3 if available
        if PYTTSX3_AVAILABLE:
            try:
                self.pyttsx3_engine = pyttsx3.init()
                self.pyttsx3_engine.setProperty('rate', 150)  # Speed of speech
                self.pyttsx3_engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
                
                # Try to find a Japanese voice if available
                voices = self.pyttsx3_engine.getProperty('voices')
                japanese_voice = None
                
                for voice in voices:
                    # Some voice systems show language in id, name or languages attribute
                    voice_info = str(voice.id) + str(voice.name).lower()
                    if 'japanese' in voice_info or 'ja' in voice_info or 'japan' in voice_info:
                        japanese_voice = voice.id
                        break
                    
                if japanese_voice:
                    self.pyttsx3_engine.setProperty('voice', japanese_voice)
                    logger.info(f"Using Japanese voice: {japanese_voice}")
                else:
                    logger.warning("No specific Japanese voice found, using default voice")
                    
                logger.info("pyttsx3 engine initialized successfully")
            except Exception as e:
                logger.error(f"Error initializing pyttsx3 engine: {e}")
                self.pyttsx3_engine = None
    
    def text_to_speech(self, text: str, output_file: str) -> Tuple[bool, str]:
        """
        Convert Japanese text to speech using the best available engine.
        
        Args:
            text: Japanese text to convert to speech
            output_file: Path to save the audio file
            
        Returns:
            Tuple of (success flag, message)
        """
        logger.info(f"Converting text to speech: {text[:50]}...")
        
        # Check if it's already an absolute path
        if os.path.isabs(output_file):
            file_path = Path(output_file)
        else:
            file_path = self.data_dir / output_file
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Determine which engine to use based on preference and availability
        if self.engine_type == 'pyttsx3' and PYTTSX3_AVAILABLE and self.pyttsx3_engine:
            return self._use_pyttsx3(text, file_path)
        elif self.engine_type == 'gtts' and GTTS_AVAILABLE:
            return self._use_gtts(text, file_path)
        elif self.engine_type == 'auto':
            # Try engines in order of preference
            if GTTS_AVAILABLE:
                success, message = self._use_gtts(text, file_path)
                if success:
                    return success, message
            
            if PYTTSX3_AVAILABLE and self.pyttsx3_engine:
                return self._use_pyttsx3(text, file_path)
            
            # If no engines available, create a placeholder
            return self._create_placeholder(text, file_path)
        else:
            # No suitable engine found, create a placeholder
            return self._create_placeholder(text, file_path)
    
    def _use_pyttsx3(self, text: str, file_path: Path) -> Tuple[bool, str]:
        """Use pyttsx3 for TTS conversion."""
        try:
            # Save to file
            self.pyttsx3_engine.save_to_file(text, str(file_path))
            self.pyttsx3_engine.runAndWait()
            
            # Check if file exists and has content
            if file_path.exists() and file_path.stat().st_size > 0:
                logger.info(f"Successfully saved speech to {file_path} using pyttsx3")
                return True, f"Successfully generated audio using pyttsx3: {file_path}"
            else:
                logger.warning(f"pyttsx3 didn't create a valid audio file at {file_path}")
                return False, "pyttsx3 failed to create a valid audio file"
        except Exception as e:
            logger.error(f"Error in pyttsx3 text to speech conversion: {e}")
            return False, f"Error using pyttsx3: {str(e)}"
    
    def _use_gtts(self, text: str, file_path: Path) -> Tuple[bool, str]:
        """Use Google TTS for conversion."""
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang='ja', slow=False)
            
            # Default output is MP3, modify path if needed
            mp3_path = file_path.with_suffix('.mp3')
            tts.save(str(mp3_path))
            
            logger.info(f"Successfully saved speech to {mp3_path} using gTTS")
            return True, f"Successfully generated audio using Google TTS: {mp3_path}"
        except Exception as e:
            logger.error(f"Error in gTTS text to speech conversion: {e}")
            return False, f"Error using Google TTS (requires internet): {str(e)}"
    
    def _create_placeholder(self, text: str, file_path: Path) -> Tuple[bool, str]:
        """Create a placeholder when no TTS engine is available."""
        try:
            # Create a text file with the content
            text_file_path = file_path.with_suffix('.txt')
            with open(text_file_path, 'w', encoding='utf-8') as f:
                f.write(text)
                f.write("\n\n")
                f.write("--- This is a placeholder for text-to-speech output ---\n")
                f.write("--- To enable actual TTS, install one of these packages: ---\n")
                f.write("--- pip install pyttsx3 ---\n")
                f.write("--- pip install gtts ---\n")
            
            # Create an empty WAV file as a placeholder
            with open(file_path, 'w') as f:
                f.write("PLACEHOLDER AUDIO FILE\n")
                f.write("This file would contain audio in a real implementation.\n")
            
            logger.info(f"Created placeholder files at {text_file_path} and {file_path}")
            return True, f"Created placeholder (no TTS engines available)"
        except Exception as e:
            logger.error(f"Error creating placeholder files: {e}")
            return False, f"Error creating placeholder files: {str(e)}"
    
    def speech_to_text(self, audio_file: str) -> str:
        """
        Convert Japanese speech to text.
        
        This is a placeholder function since speech recognition requires
        additional libraries and potentially API credentials.
        
        Args:
            audio_file: Path to the audio file
            
        Returns:
            Transcribed text or error message
        """
        # Check if it's already an absolute path
        if os.path.isabs(audio_file):
            file_path = Path(audio_file)
        else:
            file_path = self.data_dir / audio_file
            
        logger.info(f"Speech-to-text functionality is not implemented: {file_path}")
        
        # Check if a corresponding text file exists (from TTS operation)
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
        
        return "音声認識機能は実装されていません。Speech-to-Text機能を使用するには、追加のライブラリとAPIキーが必要です。"
    
    def analyze_audio(self, audio_file: str) -> Dict[str, Union[float, List[float]]]:
        """
        Analyze properties of a Japanese speech audio file.
        
        This is a simplified implementation that checks if the file exists
        and provides basic information.
        
        Args:
            audio_file: Path to the audio file
            
        Returns:
            Dictionary of audio properties
        """
        # Check if it's already an absolute path
        if os.path.isabs(audio_file):
            file_path = Path(audio_file)
        else:
            file_path = self.data_dir / audio_file
            
        logger.info(f"Analyzing audio file: {file_path}")
        
        # Check if file exists
        if not file_path.exists():
            return {
                "error": f"File not found: {file_path}",
                "exists": False
            }
        
        # Get basic file information
        file_size = file_path.stat().st_size
        file_extension = file_path.suffix.lower()
        
        # Check if there's a corresponding text file (from TTS)
        text_file_path = file_path.with_suffix('.txt')
        text_content = ""
        if text_file_path.exists():
            try:
                with open(text_file_path, 'r', encoding='utf-8') as f:
                    text_content = f.read()
                    if "---" in text_content:
                        text_content = text_content.split("---")[0].strip()
            except:
                pass
        
        # Return basic information
        result = {
            "exists": True,
            "file_size_bytes": file_size,
            "file_extension": file_extension,
            "file_path": str(file_path),
            "has_text_file": text_file_path.exists(),
            "text_length": len(text_content)
        }
        
        # If it's a placeholder file, indicate that
        if file_extension == '.txt' or (file_size < 1000 and "PLACEHOLDER" in open(file_path, 'r').read()):
            result["is_placeholder"] = True
            result["note"] = "This is a placeholder file, not actual audio"
        
        # Try to get more detailed audio info if possible
        try:
            import wave
            if file_extension == '.wav':
                with wave.open(str(file_path), 'r') as wav_file:
                    # Extract WAV file properties
                    channels = wav_file.getnchannels()
                    sample_width = wav_file.getsampwidth()
                    frame_rate = wav_file.getframerate()
                    n_frames = wav_file.getnframes()
                    duration = n_frames / frame_rate if frame_rate > 0 else 0
                    
                    result.update({
                        "channels": channels,
                        "sample_width_bytes": sample_width,
                        "frame_rate_hz": frame_rate,
                        "n_frames": n_frames,
                        "duration_seconds": duration
                    })
        except Exception as e:
            result["wave_analysis_error"] = str(e)
        
        return result

# Example usage
if __name__ == "__main__":
    processor = JapaneseSpeechProcessorMulti()
    
    # Example TTS conversion
    sample_text = "こんにちは、これは日本語のテキスト読み上げテストです。"
    success, message = processor.text_to_speech(sample_text, "multi_sample_output.wav")
    print(f"TTS result: {message}")
    
    # Analyze the generated file
    audio_properties = processor.analyze_audio("multi_sample_output.wav")
    print("Audio Properties:")
    for key, value in audio_properties.items():
        print(f"  {key}: {value}")
