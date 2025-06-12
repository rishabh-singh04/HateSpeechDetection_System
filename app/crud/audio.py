# app/crud/audio.py
from sqlalchemy.orm import Session
from app.models.audio import AudioTranscription
from app.schemas.audio import AudioTranscriptionCreate

def create_audio_transcription(db: Session, transcription: AudioTranscriptionCreate):
    db_transcription = AudioTranscription(**transcription.dict())
    db.add(db_transcription)
    db.commit()
    db.refresh(db_transcription)
    return db_transcription

def get_audio_transcription(db: Session, transcription_id: int):
    return db.query(AudioTranscription).filter(AudioTranscription.id == transcription_id).first()

def get_user_audio_transcriptions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(AudioTranscription).filter(AudioTranscription.user_id == user_id).offset(skip).limit(limit).all()

