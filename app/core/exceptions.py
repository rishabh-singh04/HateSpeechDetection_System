# app/core/exceptions.py

class ClassificationError(Exception):
    pass

class RetrievalError(Exception):
    pass

class ReasoningError(Exception):
    pass

class ActionRecommendationError(Exception):
    pass

class ExternalAPIError(Exception):
    pass