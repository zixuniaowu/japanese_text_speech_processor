.PHONY: setup test run clean

# Project paths
PYTHON = python
VENV = venv
BIN = $(VENV)/Scripts
SRC_DIR = src
DATA_DIR = data
TEST_DIR = tests
EXAMPLES_DIR = examples

# Default target
all: setup

# Setup virtual environment and install dependencies
setup:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install -e .

# Install with text processing dependencies
setup-text: setup
	$(BIN)/pip install -e ".[text]"

# Install with speech processing dependencies
setup-speech: setup
	$(BIN)/pip install -e ".[speech]"

# Install all dependencies including development ones
setup-dev: setup
	$(BIN)/pip install -e ".[text,speech,dev]"

# Run tests
test:
	$(BIN)/pytest $(TEST_DIR)

# Run the text processing example
run-text:
	$(BIN)/python $(EXAMPLES_DIR)/process_japanese_text.py

# Run the speech processing example
run-speech:
	$(BIN)/python $(EXAMPLES_DIR)/process_japanese_speech.py

# Run the main application (text processing)
run-text-main:
	$(BIN)/python main.py text --read data/text/sample_japanese.txt

# Run the main application (speech processing)
run-speech-main:
	$(BIN)/python main.py speech --text-to-speech data/text/sample_japanese.txt --output data/audio/output.wav

# Clean up generated files and directories
clean:
	rm -rf $(VENV)
	rm -rf *.egg-info
	rm -rf __pycache__
	rm -rf $(SRC_DIR)/__pycache__
	rm -rf $(TEST_DIR)/__pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Create data directory structure
data-dirs:
	mkdir -p $(DATA_DIR)/text
	mkdir -p $(DATA_DIR)/audio
	mkdir -p $(DATA_DIR)/processed
