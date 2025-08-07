# app/utils/feedback_handler.py
import json
from datetime import datetime
import os
from pathlib import Path
from typing import Dict, Union, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FEEDBACK_DIR = Path("logs")
FEEDBACK_FILE = FEEDBACK_DIR / "feedback.json"

def save_feedback(
    user_input: str, 
    page: str,
    metadata: Optional[Dict[str, Union[str, int]] = None
) -> bool:
    """
    Save user feedback to a JSON file with additional metadata.
    
    Args:
        user_input: The feedback text provided by the user
        page: The page where feedback was submitted
        metadata: Additional optional metadata to store with the feedback
        
    Returns:
        bool: True if feedback was saved successfully, False otherwise
    """
    # Create feedback directory if it doesn't exist
    FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
    
    # Prepare the feedback entry
    feedback_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "page": page,
        "feedback": user_input.strip(),
        **({"metadata": metadata} if metadata else {})
    }

    try:
        existing_data = []
        
        # Load existing data if file exists
        if FEEDBACK_FILE.exists():
            try:
                with open(FEEDBACK_FILE, "r", encoding="utf-8") as file:
                    existing_data = json.load(file)
                    if not isinstance(existing_data, list):
                        logger.warning("Feedback file corrupted, initializing new list")
                        existing_data = []
            except json.JSONDecodeError:
                logger.warning("Failed to decode feedback file, initializing new list")
                existing_data = []

        # Append new feedback
        existing_data.append(feedback_entry)

        # Save to file with atomic write operation
        temp_file = f"{FEEDBACK_FILE}.tmp"
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, indent=4, ensure_ascii=False)
        
        # Replace original file after successful write
        os.replace(temp_file, FEEDBACK_FILE)
        
        logger.info(f"Feedback successfully saved from page: {page}")
        return True

    except Exception as e:
        logger.error(f"Failed to save feedback: {str(e)}", exc_info=True)
        return False


def load_feedback() -> Optional[list]:
    """
    Load all feedback entries from the feedback file.
    
    Returns:
        Optional[list]: List of feedback entries or None if error occurs
    """
    try:
        if FEEDBACK_FILE.exists():
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        return []
    except Exception as e:
        logger.error(f"Failed to load feedback: {str(e)}", exc_info=True)
        return None