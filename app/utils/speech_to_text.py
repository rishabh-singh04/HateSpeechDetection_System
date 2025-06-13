# app/utils/speech_to_text.py

import app.test.test_whisper as test_whisper
import os

class WhisperTranscriber:
    def __init__(self, model_name: str = "base"):
        self.model = test_whisper.load_model(model_name)

    def transcribe_audio(self, audio_path: str) -> str:
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        result = self.model.transcribe(audio_path)
        return result['text']
