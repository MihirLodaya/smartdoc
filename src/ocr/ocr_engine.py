import os

class OCREngine:
    def __init__(self):
        print("OCREngine initialized")
    
    def extract_text(self, file_path):
        """Basic text extraction - will be enhanced with real OCR later"""
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.txt':
                # Read text files directly
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                return {
                    'text': text,
                    'confidence': 100.0,
                    'status': 'success'
                }
            else:
                # For images and PDFs - placeholder for now
                return {
                    'text': f'OCR processing for {file_ext} files - coming soon!',
                    'confidence': 95.0,
                    'status': 'success'
                }
                
        except Exception as e:
            return {
                'text': '',
                'confidence': 0,
                'status': 'error',
                'error': str(e)
            }
