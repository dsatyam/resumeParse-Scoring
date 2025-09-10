import os
import re

class Guardrails:
    ALLOWED_FILE_TYPES = ['.pdf','.docx']
    MAX_FILE_SIZE_MB = 5
    PROHIBITED_WORDS = ['Satyam', 'Dixit']

    @staticmethod
    def validate_file_type(file_path: str):
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in Guardrails.ALLOWED_FILE_TYPES:
            raise ValueError(f"Invalid file type {ext}. Only"+Guardrails.ALLOWED_FILE_TYPES+" files are allowed.")

    @staticmethod
    def validate_file_size(file_path: str):
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if file_size_mb > Guardrails.MAX_FILE_SIZE_MB:
            raise ValueError(f"File size exceeds {Guardrails.MAX_FILE_SIZE_MB} MB limit.")

    @staticmethod
    def validate_prohibited_content(text_content: str):
        words = []
        for word in Guardrails.PROHIBITED_WORDS:
            if re.search(r'\b' + re.escape(word) + r'\b', text_content, re.IGNORECASE):
                words.append(word)
        if len(words)>0:
            raise ValueError(f"Prohibited content detected: {words}")
