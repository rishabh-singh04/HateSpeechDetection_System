# app/utils/decorators.py

import functools
import logging
from functools import wraps
from typing import Callable, Any
from app.data.exports.moderation_exports import ModerationExporter
from app.schemas.moderation import ModerationResult
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AgentLogger")

def handle_errors(default_return=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"Error in {func.__name__}: {e}")
                return default_return
        return wrapper
    return decorator



# def export_moderation_results(func):
#     @wraps(func)
#     def wrapper(text: str, db):
#         # Call the original function
#         result = func(text, db)
        
#         # Handle both dict and string reasoning
#         if isinstance(result.reasoning, dict):
#             reason = result.reasoning.get("summary", "")
#             full_reason = str(result.reasoning)
#         else:
#             reason = str(result.reasoning)[:100]  # First 100 chars for summary
#             full_reason = str(result.reasoning)
        
#         export_data = ModerationResult(
#             text=text,
#             result=result.classification,
#             action=result.action,
#             reason=reason,
#             full_reason=full_reason,
#             snippet=text[:100] + "..." if len(text) > 100 else text,
#             timestamp=datetime.fromisoformat(result.timestamp)
#         )
        
#         # Export to CSV
#         exporter = ModerationExporter()
#         exporter.export_results([export_data])
        
#         return result
#     return wrapper
def export_moderation_results(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(text: str, db: Any) -> Any:
        try:
            result = func(text, db)
            
            # Convert response to export format
            export_data = ModerationResult.from_response(text, result)
            
            # Export with error handling
            try:
                exporter = ModerationExporter()
                exporter.export_results([export_data])
            except Exception as e:
                logger.error(f"Export failed: {str(e)}", exc_info=True)
                # Continue even if export fails
                
            return result
            
        except Exception as e:
            logger.error(f"Moderation failed: {str(e)}", exc_info=True)
            raise

    return wrapper