# app/data/exports/moderation_exports.py

import csv
from datetime import datetime
from pathlib import Path
import os
from typing import List
from fastapi import HTTPException
from app.schemas.moderation import ModerationResult

class ModerationExporter:
    def __init__(self):
        self.export_dir = Path(__file__).parent.parent / "exports"
        print(f"Export directory resolved to: {self.export_dir.absolute()}")
        os.makedirs(self.export_dir, exist_ok=True)
        
    def _generate_filename(self, prefix: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.csv"
    
    def export_results(self, results: List[ModerationResult], filename_prefix: str = "moderation") -> str:
        """Export moderation results to CSV with specified columns"""
        try:
            filename = self._generate_filename(filename_prefix)
            filepath = self.export_dir / filename
            print(f"Attempting to write to: {filepath}")
            
            fieldnames = [
                "Text", 
                "Result", 
                "Action", 
                "Reason", 
                "Full_Reason", 
                "Snippet",
                "Timestamp"
            ]
            
            with open(filepath, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
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
            print(f"Successfully wrote to {filepath}") 
            return str(filepath)
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"CSV export failed: {str(e)}"
            )