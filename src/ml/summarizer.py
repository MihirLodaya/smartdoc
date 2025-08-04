import re

class TextSummarizer:
    def __init__(self):
        print("TextSummarizer initialized")
        self.summarizer = None
        self.model_loaded = False
        
        try:
            from transformers import pipeline
            print("Loading BART model for summarization...")
            self.summarizer = pipeline(
                "summarization", 
                model="facebook/bart-large-cnn",
                device=-1  # Use CPU
            )
            self.model_loaded = True
            print("BART model loaded successfully!")
        except Exception as e:
            print(f"Could not load BART model: {e}")
            print("Falling back to rule-based summarization")
    
    def summarize_text(self, text, document_type='other', max_length=150):
        """Main summarization method with improved fallback"""
        if not text or len(text.strip()) < 50:
            return "Document too short to generate a meaningful summary."
        
        # Clean the text first
        clean_text = self.clean_text_for_summary(text)
        
        # Try ML-based summarization first
        if self.model_loaded and self.summarizer:
            try:
                print("Using BART model for summarization...")
                
                # Adjust max_length based on input length
                input_length = len(clean_text.split())
                adjusted_max_length = min(max_length, max(30, input_length // 3))
                min_length = max(20, adjusted_max_length // 3)
                
                # Truncate if too long for the model
                if len(clean_text) > 1024:
                    clean_text = clean_text[:1024]
                
                summary = self.summarizer(
                    clean_text,
                    max_length=adjusted_max_length,
                    min_length=min_length,
                    do_sample=False,
                    truncation=True
                )
                
                result = summary[0]['summary_text']
                print(f"BART summary generated: {len(result)} characters")
                return result
                
            except Exception as e:
                print(f"BART summarization failed: {e}")
                print("Falling back to rule-based summarization")
        
        # Fallback to enhanced rule-based summarization
        return self.enhanced_rule_based_summary(clean_text, document_type)
    
    def clean_text_for_summary(self, text):
        """Clean text specifically for summarization"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove very short lines (likely OCR artifacts)
        lines = text.split('\n')
        meaningful_lines = [line.strip() for line in lines if len(line.strip()) > 10]
        
        return ' '.join(meaningful_lines).strip()
    
    def enhanced_rule_based_summary(self, text, document_type):
        """Enhanced rule-based summarization with document-specific logic"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 15]
        
        if len(sentences) == 0:
            return "Unable to generate summary from the provided text."
        
        # Document-specific summarization
        if document_type == 'invoice':
            return self.summarize_invoice(sentences, text)
        elif document_type == 'resume':
            return self.summarize_resume(sentences, text)
        elif document_type in ['pan', 'aadhar']:
            return self.summarize_id_document(sentences, text, document_type)
        else:
            return self.generic_summary(sentences)
    
    def summarize_invoice(self, sentences, full_text):
        """Invoice-specific summarization"""
        key_info = []
        
        # Look for company name
        company_match = re.search(r'(Company|From|Invoice from):?\s*([A-Za-z\s&.,]+)', full_text, re.IGNORECASE)
        if company_match:
            key_info.append(f"Invoice from {company_match.group(2).strip()}")
        
        # Look for amounts
        amounts = re.findall(r'[\$₹]\s*[\d,]+\.?\d*', full_text)
        if amounts:
            total_amount = amounts[-1]  # Usually the last amount is total
            key_info.append(f"total amount {total_amount}")
        
        # Look for services/items
        for sentence in sentences[:5]:
            if any(word in sentence.lower() for word in ['service', 'product', 'item', 'development', 'design']):
                key_info.append(f"for {sentence.lower()}")
                break
        
        if key_info:
            return '. '.join(key_info).capitalize() + '.'
        else:
            return f"Invoice document with {len(sentences)} line items processed."
    
    def summarize_resume(self, sentences, full_text):
        """Resume-specific summarization"""
        key_points = []
        
        # Look for experience
        for sentence in sentences:
            if any(word in sentence.lower() for word in ['experience', 'worked', 'years', 'developer', 'engineer']):
                key_points.append(sentence)
                if len(key_points) >= 2:
                    break
        
        if key_points:
            return '. '.join(key_points[:2]) + '.'
        else:
            return f"Resume document containing professional background and qualifications."
    
    def summarize_id_document(self, sentences, full_text, doc_type):
        """ID document summarization"""
        doc_name = "PAN Card" if doc_type == 'pan' else "Aadhar Card"
        
        # Look for name
        name_patterns = [
            r'Name:?\s*([A-Za-z\s]+)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, full_text)
            if match:
                name = match.group(1).strip()
                return f"{doc_name} belonging to {name}."
        
        return f"Official {doc_name} identity document."
    
    def generic_summary(self, sentences):
        """Generic summarization for unknown document types"""
        if len(sentences) >= 3:
            return '. '.join(sentences[:3]) + '.'
        elif len(sentences) >= 1:
            return sentences[0] + '.'
        else:
            return "Document processed successfully."
