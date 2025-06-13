
Hate Speech Detector with Realtime Audio Enabled Transcription Service

A Python service for real-time audio transcription using OpenAI's Whisper model. This service accepts base64-encoded audio and returns transcribed text with additional metadata.

## Features

- Real-time audio transcription
- Support for multiple languages
- Base64 audio input format
- Performance metrics (processing time, confidence score)
- Error handling and fallback responses

## Prerequisites

- Python 3.8+
- FFmpeg (must be installed and available in system PATH)
- [Optional] NVIDIA GPU with CUDA support for faster processing

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/whisper-realtime.git
   cd whisper-realtime
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   If you don't have a `requirements.txt` file, install the packages directly:
   ```bash
   pip install openai-whisper base64io tempfile pydub
   ```

3. Install FFmpeg:
   - **Windows**: Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)
   - **Mac**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

## Usage

### Basic Usage

```python
from whisper_service import WhisperRealtime

# Initialize the transcriber (default model size is "base")
transcriber = WhisperRealtime(model_size="base")

# Transcribe base64-encoded audio
result = transcriber.transcribe(audio_base64="your_base64_encoded_audio", language="en")

print(result)
```

### Available Model Sizes

Whisper provides several model sizes (larger models are more accurate but slower):
- "tiny"
- "base" (default)
- "small"
- "medium"
- "large"

### Response Format

Successful response:
```json
{
  "text": "transcribed text here",
  "language": "en",
  "processing_time_ms": 1200,
  "confidence": 85
}
```

Error response:
```json
{
  "text": "",
  "language": "en",
  "processing_time_ms": 0,
  "confidence": 0,
  "error": "error message here"
}
```

## API Reference

### `WhisperRealtime` Class

#### Constructor
```python
WhisperRealtime(model_size: str = "base")
```
- `model_size`: Whisper model size to use ("tiny", "base", "small", "medium", "large")

#### Methods
```python
transcribe(audio_base64: str, language: str = "en") -> Dict
```
- `audio_base64`: Base64 encoded audio data (WAV, MP3, or other supported formats)
- `language`: Expected language code (e.g., "en", "fr", "es"). Defaults to "en"

## Performance Considerations

1. **Hardware Acceleration**: For best performance, use a GPU with CUDA support
2. **Model Size**: Larger models are more accurate but require more memory and processing time
3. **Audio Quality**: Clear audio with minimal background noise yields best results

## Troubleshooting

### Common Issues

1. **FFmpeg Errors**:
   - Ensure FFmpeg is installed and in your PATH
   - Verify with `ffmpeg -version` in your terminal

2. **Permission Errors**:
   - On Windows, try running your script as Administrator
   - Or use the in-memory approach with `pydub` (see code comments)

3. **Memory Errors**:
   - Use a smaller model size if you encounter memory issues
   - Reduce audio length or quality if necessary

## Acknowledgments

- OpenAI for the Whisper model
- FFmpeg team for audio processing capabilities
```

This README includes:
1. Project description
2. Installation instructions
3. Usage examples
4. API documentation
5. Performance tips
6. Troubleshooting guide
