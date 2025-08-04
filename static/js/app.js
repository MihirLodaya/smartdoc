class SmartDocApp {
    constructor() {
        this.apiBaseUrl = 'http://127.0.0.1:5001';
        this.selectedFile = null;
        this.processingData = null;
        
        this.initializeElements();
        this.attachEventListeners();
    }
    
    initializeElements() {
        // Upload elements
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.uploadBtn = document.getElementById('uploadBtn');
        this.selectedFileDiv = document.getElementById('selectedFile');
        this.fileName = document.getElementById('fileName');
        this.fileSize = document.getElementById('fileSize');
        this.processBtn = document.getElementById('processBtn');
        
        // Status elements
        this.statusSection = document.getElementById('statusSection');
        this.statusText = document.getElementById('statusText');
        
        // Results elements
        this.resultsSection = document.getElementById('resultsSection');
        this.downloadBtn = document.getElementById('downloadBtn');
    }
    
    attachEventListeners() {
        // File upload events
        this.uploadArea.addEventListener('click', () => this.fileInput.click());
        this.uploadBtn.addEventListener('click', () => this.fileInput.click());
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        this.processBtn.addEventListener('click', () => this.processDocument());
        this.downloadBtn.addEventListener('click', () => this.downloadResults());
        
        // Drag and drop events
        this.uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.uploadArea.addEventListener('drop', (e) => this.handleDrop(e));
    }
    
    handleDragOver(e) {
        e.preventDefault();
        this.uploadArea.classList.add('dragover');
    }
    
    handleDragLeave(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
    }
    
    handleDrop(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.selectFile(files[0]);
        }
    }
    
    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.selectFile(file);
        }
    }
    
    selectFile(file) {
        // Validate file type
        const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png', 'text/plain', 'image/bmp', 'image/tiff'];
        if (!allowedTypes.includes(file.type)) {
            alert('Please select a valid file type (PDF, JPG, PNG, TXT, BMP, TIFF)');
            return;
        }
        
        // Validate file size (16MB max)
        const maxSize = 16 * 1024 * 1024;
        if (file.size > maxSize) {
            alert('File size must be less than 16MB');
            return;
        }
        
        this.selectedFile = file;
        this.fileName.textContent = file.name;
        this.fileSize.textContent = this.formatFileSize(file.size);
        
        this.selectedFileDiv.style.display = 'flex';
        this.uploadArea.style.display = 'none';
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    async processDocument() {
        if (!this.selectedFile) {
            alert('Please select a file first');
            return;
        }
        
        // Show processing status
        this.showProcessingStatus();
        
        try {
            const formData = new FormData();
            formData.append('file', this.selectedFile);
            
            // Update status messages
            this.updateStatus('Uploading document...');
            
            const response = await fetch(`${this.apiBaseUrl}/upload`, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            this.updateStatus('Processing document...');
            const data = await response.json();
            
            this.processingData = data;
            this.displayResults(data);
            
        } catch (error) {
            console.error('Error processing document:', error);
            alert(`Error processing document: ${error.message}`);
            this.hideProcessingStatus();
        }
    }
    
    showProcessingStatus() {
        this.statusSection.style.display = 'block';
        this.resultsSection.style.display = 'none';
    }
    
    hideProcessingStatus() {
        this.statusSection.style.display = 'none';
    }
    
    updateStatus(message) {
        this.statusText.textContent = message;
    }
    
    displayResults(data) {
        this.hideProcessingStatus();
        this.resultsSection.style.display = 'block';
        
        // Update overview cards
        this.updateOverviewCards(data);
        
        // Update detailed results
        this.updateSummary(data.summary);
        this.updateExtractedFields(data.extracted_fields);
        this.updateValidationResults(data.validation);
        this.updateRawData(data);
        
        // Scroll to results
        this.resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    updateOverviewCards(data) {
        // Document type and confidence
        document.getElementById('docType').textContent = 
            data.classification?.document_type?.toUpperCase() || 'UNKNOWN';
        document.getElementById('docConfidence').textContent = 
            `${data.classification?.confidence || 0}% confidence`;
        
        // OCR quality
        document.getElementById('ocrConfidence').textContent = 
            `${data.ocr?.confidence || 0}% quality`;
        document.getElementById('textLength').textContent = 
            `${data.ocr?.text_length || 0} characters`;
        
        // Fields count
        const fieldsCount = Object.keys(data.extracted_fields || {}).length;
        const validFieldsCount = this.countValidFields(data.validation || {});
        
        document.getElementById('fieldsCount').textContent = `${fieldsCount} fields`;
        document.getElementById('validFields').textContent = `${validFieldsCount} valid`;
    }
    
    countValidFields(validation) {
        let count = 0;
        Object.values(validation).forEach(fieldArray => {
            if (Array.isArray(fieldArray)) {
                count += fieldArray.filter(field => field.is_valid).length;
            }
        });
        return count;
    }
    
    updateSummary(summary) {
        const summaryContent = document.getElementById('summaryContent');
        summaryContent.innerHTML = `<p>${summary || 'No summary available'}</p>`;
    }
    
    updateExtractedFields(fields) {
        const fieldsContent = document.getElementById('fieldsContent');
        
        if (!fields || Object.keys(fields).length === 0) {
            fieldsContent.innerHTML = '<p>No fields extracted</p>';
            return;
        }
        
        let html = '';
        Object.entries(fields).forEach(([fieldType, values]) => {
            if (values && values.length > 0) {
                html += `
                    <div class="field-item">
                        <span class="field-label">${fieldType.replace('_', ' ')}</span>
                        <div class="field-values">
                            ${values.map(value => `<span class="field-value">${value}</span>`).join('')}
                        </div>
                    </div>
                `;
            }
        });
        
        fieldsContent.innerHTML = html || '<p>No fields extracted</p>';
    }
    
    updateValidationResults(validation) {
        const validationContent = document.getElementById('validationContent');
        
        if (!validation || Object.keys(validation).length === 0) {
            validationContent.innerHTML = '<p>No validation results</p>';
            return;
        }
        
        let html = '';
        Object.entries(validation).forEach(([fieldType, results]) => {
            if (Array.isArray(results)) {
                results.forEach(result => {
                    const isValid = result.is_valid;
                    html += `
                        <div class="validation-item ${isValid ? 'valid' : 'invalid'}">
                            <i class="fas fa-${isValid ? 'check-circle' : 'times-circle'} validation-icon ${isValid ? 'valid' : 'invalid'}"></i>
                            <div>
                                <strong>${result.value}</strong>
                                <br>
                                <small>${result.message}</small>
                            </div>
                        </div>
                    `;
                });
            }
        });
        
        validationContent.innerHTML = html || '<p>No validation results</p>';
    }
    
    updateRawData(data) {
        const rawData = document.getElementById('rawData');
        rawData.textContent = JSON.stringify(data, null, 2);
    }
    
    downloadResults() {
        if (!this.processingData) {
            alert('No data to download');
            return;
        }
        
        const dataStr = JSON.stringify(this.processingData, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        const url = URL.createObjectURL(dataBlob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `smartdoc-results-${new Date().toISOString().slice(0,10)}.json`;
        link.click();
        
        URL.revokeObjectURL(url);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SmartDocApp();
});
