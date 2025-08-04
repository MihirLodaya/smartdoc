import re

class DocumentClassifier:
    def __init__(self):
        print("DocumentClassifier initialized")
        self.document_keywords = {
            'invoice': ['invoice', 'bill', 'amount', 'total', 'gst', 'tax'],
            'resume': ['experience', 'education', 'skills', 'employment'],
            'aadhar': ['aadhaar', 'aadhar', 'uid', 'unique', 'identity'],
            'pan': ['pan', 'permanent', 'account', 'number'],
            'other': ['document', 'text']
        }
    
    def classify_document(self, text):
        """Simple keyword-based classification"""
        if not text:
            return {
                'document_type': 'other',
                'confidence': 0,
                'method': 'rule_based'
            }
            
        text_lower = text.lower()
        scores = {}
        
        for doc_type, keywords in self.document_keywords.items():
            score = 0
            for keyword in keywords:
                score += len(re.findall(r'\b' + keyword + r'\b', text_lower))
            scores[doc_type] = score
        
        predicted_type = max(scores, key=scores.get)
        confidence = scores[predicted_type] / (sum(scores.values()) + 1) * 100
        
        return {
            'document_type': predicted_type,
            'confidence': round(confidence, 2),
            'method': 'rule_based'
        }
