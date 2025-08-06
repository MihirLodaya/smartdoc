#  SmartDoc AI - Intelligent Document Processing Platform

 [ Documentation](#-features) -  [ Installation](#-installation) -  [ Usage](#-usage) 

##  **Table of Contents**

- [Overview](#-overview)
- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Configuration](#-configuration
- [License](#-license)

##  **Overview**

SmartDoc AI is an advanced document processing platform that combines **OCR technology**, **machine learning**, and **artificial intelligence** to extract, classify, and analyze documents automatically. Upload any document and get instant insights with field extraction, data validation, and AI-powered summaries.

### ** Key Capabilities**

- ** AI-Powered Classification** - Automatically detect document types (invoices, resumes, ID cards, contracts)
- ** Intelligent Summarization** - Generate concise summaries using Facebook's BART model
- ** Smart Field Extraction** - Extract emails, phone numbers, amounts, dates, and document-specific fields
- ** Data Validation** - Validate PAN numbers, Aadhar cards, email formats, and more
- ** Beautiful Web Interface** - Modern, responsive UI with drag-and-drop functionality
- ** RESTful API** - Clean, documented API endpoints for integration

##  **Features**

### ** AI & Machine Learning**
- **Document Classification** using rule-based and ML approaches
- **Text Summarization** powered by Hugging Face BART model
- **Field Extraction** with regex patterns and ML validation
- **Confidence Scoring** for all AI predictions

### ** OCR & Text Processing**
- **Multi-format Support** - PDF, JPG, PNG, TXT, BMP, TIFF
- **Advanced OCR** using Tesseract with image preprocessing
- **Text Cleaning** and normalization
- **Multi-language Support** (extensible)

### ** Data Processing**
- **Smart Field Detection** - Emails, phones, amounts, dates, IDs
- **Format Validation** - PAN, Aadhar, GSTIN, email validation
- **Document-Specific Logic** - Tailored processing for different document types
- **Structured Output** - Clean JSON responses

### ** Web Interface**
- **Drag & Drop Upload** with visual feedback
- **Real-time Processing** status updates
- **Interactive Results** with expandable sections
- **Download Functionality** - Export results as JSON
- **Responsive Design** - Works on desktop and mobile

### ** Developer Features**
- **RESTful API** with comprehensive endpoints
- **CORS Support** for cross-origin requests
- **Error Handling** with detailed error messages
- **Logging** and debugging capabilities
- **Docker Support** for easy deployment

### ** Prerequisites**
- **Python 3.9+** 
- **Tesseract OCR** 
- **Poppler** (for PDF processing)

### **System Dependencies**

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr poppler-utils
```

**macOS:**
```bash
brew install tesseract poppler
```

**Windows:**
- Download [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
- Download [Poppler](https://github.com/oschwartz10612/poppler-windows)

### **Python Setup**

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/smartdoc-ai.git
cd smartdoc-ai
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

## ⚡ **Quick Start**

### **1. Start the API Server**
```bash
python src/app.py
```

### **2. Access the Web Interface**
Open your browser and navigate to:
```
http://127.0.0.1:5001/demo
```

### **3. Upload and Process Documents**
- Drag & drop any supported file (PDF, JPG, PNG, TXT)
- Click "Analyze with AI" 
- View comprehensive results with AI insights

### **4. API Usage Example**
```bash
# Upload and process a document
curl -X POST -F "file=@invoice.pdf" http://127.0.0.1:5001/upload

# Get AI summary
curl -X POST -H "Content-Type: application/json" \
  -d '{"text":"Your document text here","document_type":"invoice"}' \
  http://127.0.0.1:5001/summarize

# Validate fields
curl -X POST -H "Content-Type: application/json" \
  -d '{"pan":"ABCDE1234F","email":"test@example.com"}' \
  http://127.0.0.1:5001/validate
```

## 📚 **Usage**

### **Supported Document Types**
- **📄 Invoices** - Extract amounts, GST numbers, dates, vendor details
- **👤 Resumes** - Summarize experience, extract contact information
- **🆔 ID Cards** - Validate PAN, Aadhar numbers and formats
- **📋 Contracts** - Summarize key clauses and extract parties
- **📝 General Documents** - Text extraction and AI summarization

### **Web Interface Features**

1. **Upload Methods:**
   - Click to browse files
   - Drag and drop onto upload area
   - Paste files (if browser supports)

2. **Processing Feedback:**
   - Real-time status updates
   - Progress animations
   - Error handling with user-friendly messages

3. **Results Display:**
   - Overview cards with key metrics
   - AI-generated summaries
   - Extracted fields with validation
   - Raw JSON data for developers

4. **Export Options:**
   - Download results as JSON
   - Copy specific field values
   - Print-friendly format

## **API Documentation**

### **Base URL**
```
http://127.0.0.1:5001
```

### **Endpoints**

#### ** Upload and Process Document**
```http
POST /upload
Content-Type: multipart/form-data

Parameters:
- file: Document file (PDF, JPG, PNG, TXT, BMP, TIFF)
- include_text: Optional, set to 'true' to include extracted text

Response: Comprehensive analysis results
```

#### ** Text Summarization**
```http
POST /summarize
Content-Type: application/json

Body:
{
  "text": "Document text to summarize",
  "document_type": "invoice|resume|contract|other",
  "max_length": 150
}

Response: AI-generated summary with statistics
```

#### ** Field Validation**
```http
POST /validate
Content-Type: application/json

Body:
{
  "pan": "ABCDE1234F",
  "email": "test@example.com",
  "phone": "9876543210",
  "aadhar": "123456789012"
}

Response: Validation results for each field
```

#### **🔍 Extract Text Only**
```http
GET /extract/{file_id}

Response: Extracted text with confidence scores
```

#### **❤ Health Check**
```http
GET /health

Response: API status and component health
```

### **Response Format**
```json
{
  "filename": "document.pdf",
  "status": "completed",
  "classification": {
    "document_type": "invoice",
    "confidence": 85.5,
    "method": "rule_based"
  },
  "extracted_fields": {
    "emails": ["contact@company.com"],
    "amounts": ["$1,500.00"],
    "dates": ["2024-01-15"]
  },
  "validation": {
    "emails": [
      {
        "value": "contact@company.com",
        "is_valid": true,
        "message": "Valid email format"
      }
    ]
  },
  "summary": "AI-generated document summary...",
  "ocr": {
    "confidence": 98.2,
    "text_length": 1247
  }
}
```

##  **Deployment**

### **Docker Deployment**

1. **Build and run with Docker Compose:**
```bash
docker-compose up -d
```

2. **Custom Docker build:**
```bash
docker build -t smartdoc-ai .
docker run -p 5001:5001 -v $(pwd)/uploads:/app/uploads smartdoc-ai
```

### **Cloud Deployment**

#### **Heroku**
```bash
heroku create your-smartdoc-app
heroku buildpacks:add --index 1 heroku-community/apt
echo "tesseract-ocr poppler-utils" > Aptfile
git add . && git commit -m "Deploy to Heroku"
git push heroku main
```

#### **Railway**
```bash
railway login
railway init
railway add
railway deploy
```

#### **Render**
- Connect your GitHub repository
- Set build command: `pip install -r requirements.txt`
- Set start command: `python src/app.py`
- Add environment variables

##  **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 SmartDoc AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

##  **Acknowledgments**

- **Hugging Face** for the BART summarization model
- **Tesseract OCR** team for excellent OCR capabilities
- **Flask** community for the robust web framework
- **OpenCV** contributors for image processing tools

##  **Support**

- **🐛 Issues:** [GitHub Issues](https://github.com/yourusername/smartdoc-ai/issues)
- **💬 Discussions:** [GitHub Discussions](https://github.com/yourusername/smartdoc-ai/discussions)
- **📖 Documentation:** [Full Documentation](https://smartdoc-ai.readthedocs.io)



[](https://github.com/yourusername/smartrtrt
