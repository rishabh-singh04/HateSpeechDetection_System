# app/data/exports/moderation_exports.py

import csv
from datetime import datetime
from pathlib import Path
import os
from typing import List
from fastapi import HTTPException
from app.schemas.moderation import ModerationResult
import logging

# logger = logging.getLogger(__name__)

class ModerationExporter:
    def __init__(self):
        self.export_dir = Path(__file__).parent.parent / "exports"
        self.single_file = self.export_dir / "moderation_results.csv"
        os.makedirs(self.export_dir, exist_ok=True)
        
        # Initialize file with headers if it doesn't exist
        if not self.single_file.exists():
            with open(self.single_file, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self._get_fieldnames())
                writer.writeheader()
        
        # logger.info(f"Export directory: {self.export_dir.absolute()}")

    def _get_fieldnames(self) -> List[str]:
        return [
            "Text", 
            "Result", 
            "Action", 
            "Reason", 
            "Full_Reason", 
            "Snippet",
            "Timestamp"
        ]

    def export_results(self, results: List[ModerationResult]) -> str:
        """Append moderation results to single CSV file"""
        try:
            # Open in append mode
            with open(self.single_file, mode='a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self._get_fieldnames())
                
                for result in results:
                    writer.writerow({
                        "Text": result.text,
                        "Result": result.result,
                        "Action": result.action,
                        "Reason": result.reason,
                        "Full_Reason": result.full_reason,
                        "Snippet": result.snippet,
                        "Timestamp": datetime.now().isoformat()
                    })
            
            # logger.info(f"Appended {len(results)} records to {self.single_file}")
            return str(self.single_file)
            
        except Exception as e:
            error_msg = f"CSV export failed: {str(e)}"
            # logger.error(error_msg, exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=error_msg
            )

    def _generate_filename(self, prefix: str) -> str:
        """Legacy method kept for compatibility"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.csv"