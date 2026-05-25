# app/services/query_logger.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy.orm import Session
from sqlalchemy import Integer
from sqlalchemy import Column, DateTime, Text
from app.db.base import Base
from datetime import datetime

class QueryLog(Base):
    __tablename__ = "query_logs"
    id = Column(Integer, primary_key=True)
    query = Column(Text)
    results_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class QueryLogger:
    def __init__(self, db: Session):
        self.db = db

    def log_query(self, query: str, results_count: int):
        record = QueryLog(
            query=query,
            results_count=results_count
        )
        self.db.add(record)
        self.db.commit()