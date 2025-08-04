from flask import request, current_app
from flask_restful import Resource
import os
import uuid
import sys
from werkzeug.utils import secure_filename
import json

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import modules
from ocr.ocr_engine import OCREngine
from ml.document_classifier import DocumentClassifier
from ml.summarizer import TextSummarizer
from validators.field_extractor import FieldExtractor
from validators.field_validator import FieldValidator
from utils.text_cleaner import TextCleaner

class FileUploadResource(Resource):
    def __init__(self):
        self.ocr_engine = OCREngine()
        self.classifier = DocumentClassifier()
        self.summarizer = TextSummarizer()
        self.field_extractor = FieldExtractor()
        self.field_validator = FieldValidator()
        self.text_cleaner = TextCleaner()
        self.allowed_extensions = {'png', 'jpg', 'jpeg', 'pdf', 'bmp', 'tiff', 'txt'}
    
    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def post(self):
        """Upload and process document"""
        try:
            # Check if file is present
            if 'file' not in request.files:
                return {'error': 'No file provided'}, 400
            
            file = request.files['file']
            
            if file.filename == '':
                return {'error': 'No file selected'}, 400
            
            if not self.allowed_file(file.filename):
                return {
                    'error': 'File type not supported', 
                    'supported_types': list(self.allowed_extensions)
                }, 400
            
            # Generate unique filename
            original_filename = secure_filename(file.filename)
            file_extension = original_filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            
            # Save file
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(upload_path)
            
            # Process the document
            result = self.process_document(upload_path, original_filename)
            result['file_id'] = unique_filename.split('.')[0]
            
            return result, 200
            
        except Exception as e:
            return {'error': f'Processing failed: {str(e)}'}, 500
    
    def process_document(self, file_path, original_filename):
        """Process uploaded document through the entire pipeline"""
        result = {
            'filename': original_filename,
            'status': 'processing'
        }
        
        try:
            # Step 1: OCR Extraction
            ocr_result = self.ocr_engine.extract_text(file_path)
            if ocr_result['status'] != 'success':
                result['status'] = 'failed'
                result['error'] = ocr_result.get('error', 'OCR failed')
                return result
            
            raw_text = ocr_result['text']
            cleaned_text = self.text_cleaner.clean_text(raw_text)
            
            result['ocr'] = {
                'confidence': ocr_result['confidence'],
                'text_length': len(cleaned_text)
            }
            
            # Step 2: Document Classification
            classification = self.classifier.classify_document(cleaned_text)
            result['classification'] = classification
            
            document_type = classification['document_type']
            
            # Step 3: Field Extraction
            extracted_fields = self.field_extractor.extract_all_fields(
                cleaned_text, document_type
            )
            result['extracted_fields'] = extracted_fields
            
            # Step 4: Field Validation
            validation_results = self.field_validator.validate_extracted_fields(
                extracted_fields, document_type
            )
            result['validation'] = validation_results
            
            # Step 5: Text Summarization
            summary = self.summarizer.summarize_text(cleaned_text, document_type)
            result['summary'] = summary
            
            # Optional: Include original text for debugging
            if request.args.get('include_text') == 'true':
                result['extracted_text'] = cleaned_text
            
            result['status'] = 'completed'
            
            return result
            
        except Exception as e:
            result['status'] = 'failed'
            result['error'] = str(e)
            return result

class ExtractTextResource(Resource):
    def __init__(self):
        self.ocr_engine = OCREngine()
        self.text_cleaner = TextCleaner()
    
    def get(self, file_id):
        """Get extracted text for a specific file"""
        try:
            # Find the file
            upload_folder = current_app.config['UPLOAD_FOLDER']
            file_path = None
            
            for filename in os.listdir(upload_folder):
                if filename.startswith(file_id):
                    file_path = os.path.join(upload_folder, filename)
                    break
            
            if not file_path or not os.path.exists(file_path):
                return {'error': 'File not found'}, 404
            
            # Extract text
            ocr_result = self.ocr_engine.extract_text(file_path)
            
            if ocr_result['status'] != 'success':
                return {'error': ocr_result.get('error', 'OCR failed')}, 500
            
            cleaned_text = self.text_cleaner.clean_text(ocr_result['text'])
            
            return {
                'file_id': file_id,
                'text': cleaned_text,
                'confidence': ocr_result['confidence'],
                'status': 'success'
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

class SummarizeResource(Resource):
    def __init__(self):
        self.summarizer = TextSummarizer()
    
    def post(self):
        """Summarize provided text"""
        try:
            data = request.get_json()
            
            if not data or 'text' not in data:
                return {'error': 'No text provided'}, 400
            
            text = data['text']
            document_type = data.get('document_type', 'other')
            max_length = data.get('max_length', 150)
            
            summary = self.summarizer.summarize_text(text, document_type, max_length)
            
            return {
                'summary': summary,
                'original_length': len(text),
                'summary_length': len(summary),
                'compression_ratio': round(len(summary) / len(text), 2) if len(text) > 0 else 0,
                'status': 'success'
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

class ValidateFieldsResource(Resource):
    def __init__(self):
        self.field_validator = FieldValidator()
    
    def post(self):
        """Validate specific fields"""
        try:
            data = request.get_json()
            
            if not data:
                return {'error': 'No data provided'}, 400
            
            validation_results = {}
            
            # Validate individual fields
            if 'pan' in data:
                is_valid, message = self.field_validator.validate_pan(data['pan'])
                validation_results['pan'] = {
                    'value': data['pan'],
                    'is_valid': is_valid,
                    'message': message
                }
            
            if 'email' in data:
                is_valid, message = self.field_validator.validate_email(data['email'])
                validation_results['email'] = {
                    'value': data['email'],
                    'is_valid': is_valid,
                    'message': message
                }
            
            return {
                'validation_results': validation_results,
                'status': 'success'
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

class HealthCheckResource(Resource):
    def get(self):
        """Health check endpoint"""
        return {
            'status': 'healthy',
            'service': 'SmartDoc API',
            'version': '1.0.0',
            'components': {
                'ocr': 'active',
                'classifier': 'active',
                'summarizer': 'active',
                'validator': 'active'
            }
        }, 200
