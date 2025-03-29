#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="japanese_text_speech_processor",
    version="0.1.0",
    description="A Python application for processing Japanese text and speech",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "pathlib",
        "typing",
    ],
    extras_require={
        "text": [
            "mecab-python3",
            "fugashi",
            "unidic",
            "janome",
        ],
        "speech": [
            "pyttsx3",
            "SpeechRecognition",
            "pyaudio",
            "librosa",
            "soundfile",
            "numpy",
        ],
        "dev": [
            "pytest",
            "black",
            "flake8",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Natural Language :: Japanese",
    ],
    python_requires=">=3.8",
)
