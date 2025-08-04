import requests
import json

BASE_URL = "http://localhost:5001"

def test_health_check():
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check:", response.json())

def test_text_summarization():
    data = {
        "text": "This is a sample invoice from XYZ Company for software development services. The invoice number is INV-2024-001. The total amount is Rs. 25,000 including 18% GST. Payment is due within 30 days.",
        "document_type": "invoice"
    }
    
    response = requests.post(f"{BASE_URL}/summarize", json=data)
    print("Summarization Result:", json.dumps(response.json(), indent=2))

def test_field_validation():
    data = {
        "pan": "ABCDE1234F",
        "aadhar": "123456789012",
        "email": "test@example.com",
        "phone": "9876543210"
    }
    
    response = requests.post(f"{BASE_URL}/validate", json=data)
    print("Validation Result:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_health_check()
    test_text_summarization()
    test_field_validation()
