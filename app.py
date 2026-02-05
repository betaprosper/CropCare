from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Dummy disease database
DISEASE_INFO = {
    'black_pod': {
        'name': 'Black Pod Disease',
        'scientific_name': 'Phytophthora megakarya',
        'confidence': 92.5,
        'severity': 'High',
        'description': 'Black pod disease is the most damaging disease of cocoa worldwide, causing losses of 20-30% annually and up to 100% in severe cases.',
        'symptoms': [
            'Dark brown to black lesions on pods',
            'Rapid spread during wet seasons',
            'Premature pod drop',
            'White fungal growth on infected areas',
            'Internal bean rot'
        ],
        'treatment': [
            'Apply fungicides: Ridomil, Kocide, or copper-based fungicides',
            'Remove and destroy infected pods immediately',
            'Improve farm sanitation and drainage',
            'Prune trees to improve air circulation',
            'Harvest ripe pods frequently (weekly during wet season)'
        ],
        'prevention': [
            'Plant resistant cocoa varieties',
            'Maintain proper spacing between trees',
            'Regular farm sanitation',
            'Apply fungicides preventively during rainy season',
            'Ensure good drainage in cocoa farms'
        ],
        'chemicals': [
            {
                'name': 'Ridomil Gold',
                'dosage': '2.5kg per hectare',
                'application': 'Spray every 2-3 weeks during rainy season'
            },
            {
                'name': 'Kocide 2000',
                'dosage': '3kg per hectare',
                'application': 'Apply as protective spray'
            },
            {
                'name': 'Nordox 75 WG',
                'dosage': '2kg per hectare',
                'application': 'Preventive application'
            }
        ]
    },
    'healthy': {
        'name': 'Healthy Cocoa',
        'confidence': 95.0,
        'severity': 'None',
        'description': 'Your cocoa plant appears healthy with no visible signs of disease.',
        'symptoms': [],
        'treatment': [],
        'prevention': [
            'Continue regular farm maintenance',
            'Monitor plants weekly for early disease detection',
            'Maintain proper nutrition and watering',
            'Keep farm clean and well-drained'
        ],
        'chemicals': []
    }
}

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/upload')
def upload_page():
    """Upload page"""
    return render_template('upload.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Handle image upload and analysis"""
    if 'crop_image' not in request.files:
        flash('No file uploaded', 'danger')
        return redirect(url_for('upload_page'))
    
    file = request.files['crop_image']
    
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(url_for('upload_page'))
    
    if file and allowed_file(file.filename):
        # Save the file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # TODO: Add actual AI model prediction here
        # For now, randomly select a disease for demonstration
        import random
        disease_key = random.choice(['black_pod', 'healthy'])
        
        return redirect(url_for('result', filename=filename, disease=disease_key))
    
    flash('Invalid file type. Please upload an image (PNG, JPG, JPEG, GIF)', 'danger')
    return redirect(url_for('upload_page'))

@app.route('/result/<filename>/<disease>')
def result(filename, disease):
    """Display analysis results"""
    disease_info = DISEASE_INFO.get(disease, DISEASE_INFO['healthy'])
    
    result_data = {
        'image_path': f'uploads/{filename}',
        'disease': disease_info['name'],
        'scientific_name': disease_info.get('scientific_name', ''),
        'confidence': disease_info['confidence'],
        'severity': disease_info['severity'],
        'description': disease_info['description'],
        'symptoms': disease_info['symptoms'],
        'treatment': disease_info['treatment'],
        'prevention': disease_info['prevention'],
        'chemicals': disease_info.get('chemicals', []),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return render_template('result.html', result=result_data)

@app.route('/community')
def community():
    """Community page"""
    return render_template('community.html')

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)