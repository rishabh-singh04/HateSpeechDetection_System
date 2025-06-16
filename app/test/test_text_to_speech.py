# app/tests/test_speech_to_text.py

import pytest
from unittest.mock import MagicMock, patch
import os
from app.utils.speech_to_text import WhisperTranscriber

@pytest.fixture
def mock_whisper():
    with patch('whisper.load_model') as mock_load:
        yield mock_load

def test_whisper_transcriber_initialization(mock_whisper):
    # Test initialization with default model
    transcriber = WhisperTranscriber()
    mock_whisper.assert_called_once_with("base")
    
    # Test initialization with custom model
    transcriber = WhisperTranscriber(model_name="large")
    mock_whisper.assert_called_with("large")

def test_transcribe_audio_success(mock_whisper):
    # Setup mock model and response
    mock_model = MagicMock()
    mock_model.transcribe.return_value = {'text': 'test transcription'}
    mock_whisper.return_value = mock_model
    
    # Test successful transcription
    with patch('os.path.exists', return_value=True):
        transcriber = WhisperTranscriber()
        result = transcriber.transcribe_audio("test_audio.mp3")
        
        mock_model.transcribe.assert_called_once_with("test_audio.mp3")
        assert result == 'test transcription'

def test_transcribe_audio_file_not_found(mock_whisper):
    # Test FileNotFoundError is raised when file doesn't exist
    with patch('os.path.exists', return_value=False):
        transcriber = WhisperTranscriber()
        with pytest.raises(FileNotFoundError) as excinfo:
            transcriber.transcribe_audio("nonexistent.mp3")
        
        assert "Audio file not found: nonexistent.mp3" in str(excinfo.value)