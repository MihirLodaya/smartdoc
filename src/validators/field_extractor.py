import re

class FieldExtractor:
    def __init__(self):
        print("FieldExtractor initialized")
        self.patterns = {
            'pan': r'[A-Z]{5}[0-9]{4}[A-Z]{1}',
            'aadhar': r'\b\d{4}\s?\d{4}\s?\d{4}\b',
            'gstin': r'\b\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}\b',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'(\+91|91)?[\s-]?[6-9]\d{9}',
            'amount': r'[\$₹]?\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?',
            'date': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            'invoice_number': r'(?:invoice|inv|bill)[\s#-]*([A-Z0-9-]+)',
        }
    
    def extract_emails(self, text):
        """Extract email addresses"""
        matches = re.findall(self.patterns['email'], text, re.IGNORECASE)
        return list(set(matches))
    
    def extract_phone_numbers(self, text):
        """Extract phone numbers"""
        matches = re.findall(self.patterns['phone'], text)
        return [match[1] if match[0] else match for match in matches]
    
    def extract_amounts(self, text):
        """Extract monetary amounts"""
        matches = re.findall(self.patterns['amount'], text)
        return list(set(matches))
    
    def extract_dates(self, text):
        """Extract dates"""
        matches = re.findall(self.patterns['date'], text)
        return list(set(matches))
    
    def extract_invoice_numbers(self, text):
        """Extract invoice numbers"""
        matches = re.findall(self.patterns['invoice_number'], text, re.IGNORECASE)
        return list(set(matches))
    
    def extract_all_fields(self, text, document_type=None):
        """Extract all relevant fields based on document type"""
        if not text:
            return {}
            
        fields = {}
        
        # Common fields for all documents
        fields['emails'] = self.extract_emails(text)
        fields['phone_numbers'] = self.extract_phone_numbers(text)
        fields['dates'] = self.extract_dates(text)
        
        # Document-specific fields
        if document_type in ['invoice', 'bill']:
            fields['amounts'] = self.extract_amounts(text)
            fields['invoice_numbers'] = self.extract_invoice_numbers(text)
            fields['gstin'] = re.findall(self.patterns['gstin'], text.upper())
        
        elif document_type == 'pan':
            fields['pan_numbers'] = re.findall(self.patterns['pan'], text.upper())
        
        elif document_type == 'aadhar':
            fields['aadhar_numbers'] = re.findall(self.patterns['aadhar'], text)
        
        # Remove empty fields
        fields = {k: v for k, v in fields.items() if v}
        
        return fields
