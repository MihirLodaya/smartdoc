import re

class FieldValidator:
    def __init__(self):
        print("FieldValidator initialized")
    
    def validate_pan(self, pan):
        """Validate PAN format"""
        if not pan or len(pan) != 10:
            return False, "Invalid PAN length"
        pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
        if not re.match(pattern, pan.upper()):
            return False, "Invalid PAN format"
        return True, "Valid PAN format"
    
    def validate_aadhar(self, aadhar):
        """Validate Aadhar format"""
        if not aadhar:
            return False, "Empty Aadhar number"
        clean_aadhar = re.sub(r'\s', '', aadhar)
        if len(clean_aadhar) != 12:
            return False, "Invalid Aadhar length"
        if not clean_aadhar.isdigit():
            return False, "Aadhar should contain only digits"
        return True, "Valid Aadhar format"
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        if re.match(pattern, email):
            return True, "Valid email format"
        return False, "Invalid email format"
    
    def validate_phone(self, phone):
        """Validate Indian phone number"""
        clean_phone = re.sub(r'[\s\-\+]', '', phone)
        if clean_phone.startswith('91') and len(clean_phone) == 12:
            clean_phone = clean_phone[2:]
        if len(clean_phone) == 10 and clean_phone[0] in '6789':
            return True, "Valid phone number"
        return False, "Invalid phone number format"
    
    def validate_extracted_fields(self, fields, document_type):
        """Validate all extracted fields"""
        validation_results = {}
        
        if 'emails' in fields and fields['emails']:
            validation_results['emails'] = []
            for email in fields['emails']:
                is_valid, message = self.validate_email(email)
                validation_results['emails'].append({
                    'value': email,
                    'is_valid': is_valid,
                    'message': message
                })
        
        if 'phone_numbers' in fields and fields['phone_numbers']:
            validation_results['phone_numbers'] = []
            for phone in fields['phone_numbers']:
                is_valid, message = self.validate_phone(phone)
                validation_results['phone_numbers'].append({
                    'value': phone,
                    'is_valid': is_valid,
                    'message': message
                })
        
        if document_type == 'pan' and 'pan_numbers' in fields and fields['pan_numbers']:
            validation_results['pan'] = []
            for pan in fields['pan_numbers']:
                is_valid, message = self.validate_pan(pan)
                validation_results['pan'].append({
                    'value': pan,
                    'is_valid': is_valid,
                    'message': message
                })
        
        return validation_results
