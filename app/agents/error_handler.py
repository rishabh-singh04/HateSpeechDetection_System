# app/agents/error_handler.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import traceback
import logging
from app.core.exceptions import *

logger = logging.getLogger("error_handler")
logging.basicConfig(level=logging.INFO)

class ErrorHandlerAgent:
    def handle(self, err: Exception, context: str = "unknown") -> dict:
        logger.error(f"Error in context '{context}': {str(err)}")
        logger.debug(traceback.format_exc())

        if isinstance(err, ClassificationError):
            return {"error": "Failed to classify content. Please try again."}
        elif isinstance(err, RetrievalError):
            return {"error": "Unable to retrieve relevant policy documents."}
        elif isinstance(err, ReasoningError):
            return {"error": "Could not generate policy reasoning."}
        elif isinstance(err, ActionRecommendationError):
            return {"error": "Action recommendation failed."}
        elif isinstance(err, ExternalAPIError):
            return {"error": "External API service is currently unavailable."}
        else:
            return {"error": "An unexpected error occurred. Please contact support."}
