# # app/db/models/policy.py

# from sqlalchemy import Column, Integer, String, Text
# from app.db.base import Base

# class PolicyDocument(Base):
#     __tablename__ = "policy_documents"
#     id = Column(Integer, primary_key=True)
#     name = Column(String(255))  # e.g., "reddit_policy.txt"
#     content = Column(Text)      # Full text of the policy

from sqlalchemy import Column, Integer, String, Text
from app.db.base import Base

class PolicyDocument(Base):
    __tablename__ = "policy_documents"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    content = Column(Text)
    
    # Proper dynamic attribute handling
    _score = None
    
    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, value):
        self._score = value