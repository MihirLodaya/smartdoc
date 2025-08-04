from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_restful import Api
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Import API resources
from api.resources import (
    FileUploadResource,
    ExtractTextResource,
    SummarizeResource,
    ValidateFieldsResource,
    HealthCheckResource
)

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)
api = Api(app)

# Configuration
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))  # 16MB
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Add API routes
api.add_resource(FileUploadResource, '/upload')
api.add_resource(ExtractTextResource, '/extract/<string:file_id>')
api.add_resource(SummarizeResource, '/summarize')
api.add_resource(ValidateFieldsResource, '/validate')
api.add_resource(HealthCheckResource, '/health')

# Static file serving routes
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('../static', filename)

@app.route('/demo')
def demo():
    return send_from_directory('../static', 'index.html')

# Updated home route with web interface link
@app.route('/')
def home():
    return '''
    <html>
    <head>
        <title>SmartDoc API</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: center;
                padding: 50px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                margin: 0;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: rgba(255,255,255,0.1);
                padding: 40px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            }
            h1 {
                font-size: 3rem;
                margin-bottom: 20px;
                background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .demo-btn {
                background: linear-gradient(45deg, #4ecdc4, #44a08d);
                color: white;
                padding: 20px 40px;
                text-decoration: none;
                border-radius: 50px;
                font-size: 1.2rem;
                font-weight: 600;
                display: inline-block;
                margin: 30px 0;
                transition: all 0.3s ease;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .demo-btn:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 40px rgba(0,0,0,0.3);
            }
            .endpoints {
                background: rgba(255,255,255,0.1);
                border-radius: 15px;
                padding: 30px;
                margin-top: 30px;
            }
            .endpoints ul {
                list-style: none;
                padding: 0;
            }
            .endpoints li {
                background: rgba(255,255,255,0.1);
                margin: 10px 0;
                padding: 15px;
                border-radius: 10px;
                border-left: 4px solid #4ecdc4;
            }
            .status {
                color: #4ecdc4;
                font-weight: 600;
                margin-bottom: 30px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 SmartDoc API</h1>
            <p class="status">✅ Your intelligent document processing API is running!</p>
            <p>Upload documents and get AI-powered analysis with text extraction, classification, and validation.</p>
            
            <a href="/demo" class="demo-btn">
                📱 Try the Web Interface
            </a>
            
            <div class="endpoints">
                <p><strong>Available API Endpoints:</strong></p>
                <ul>
                    <li>📤 <strong>POST /upload</strong> - Upload and process document</li>
                    <li>📄 <strong>POST /summarize</strong> - Summarize text with AI</li>
                    <li>✅ <strong>POST /validate</strong> - Validate extracted fields</li>
                    <li>🔍 <strong>GET /extract/&lt;file_id&gt;</strong> - Get extracted text</li>
                    <li>❤️ <strong>GET /health</strong> - API health check</li>
                </ul>
            </div>
            
            <div style="margin-top: 30px; opacity: 0.8;">
                <p><strong>Features:</strong></p>
                <p>🤖 AI Classification • 📝 Smart Summarization • 🔍 Field Extraction • ✅ Data Validation</p>
                <p><strong>Supports:</strong> PDF, JPG, PNG, TXT files (Max: 16MB)</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting SmartDoc API...")
    print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    print("Available endpoints:")
    print("  📱 Web Interface: http://127.0.0.1:5001/demo")
    print("  🏠 Home: http://127.0.0.1:5001/")
    print("  ❤️  Health: http://127.0.0.1:5001/health")
    print("  📤 Upload: POST http://127.0.0.1:5001/upload")
    app.run(debug=True, host='0.0.0.0', port=5001)
