from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/pricing')
def pricing():
    return render_template('pricing.html')

@bp.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')

from .services.parser import parse_resume
from .services.market_scanner import scan_market
from .services.diagnoser import diagnose

@bp.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        flash('No file part')
        return redirect(url_for('main.index'))
    file = request.files['resume']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('main.index'))
    
    job_title = request.form.get('job_title')
    company = request.form.get('company')

    # Initialize variables to defaults
    diagnosis_html = ""
    scores = {}
    drift = {}
    personas = []
    career_pivot = {}
    target_companies = {}
    blind_spots = []
    
    # 1. Parse Resume
    # Save temporarily to parse
    upload_folder = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, secure_filename(file.filename))
    file.save(filepath)
    
    try:
        resume_text = parse_resume(filepath)
        if not resume_text:
            flash('Could not extract text from resume.')
            return redirect(url_for('main.index'))

        job_description = request.form.get('job_description')
        
        if job_description and job_description.strip():
             # Use provided JD
             market_signals = f"USER PROVIDED JOB DESCRIPTION:\n{job_description}"
        else:
             # 2. Key Market Signals via Search
             market_signals = scan_market(job_title, company)
        
        # 3. Diagnosis (Returns JSON string now)
        diagnosis_response = diagnose(resume_text, market_signals)
        
        import json
        try:
            data = json.loads(diagnosis_response)
            diagnosis_html = data.get('diagnosis_html', 'Error parsing diagnosis.')
            scores = data.get('scores', {})
            drift = data.get('market_drift', {})
            personas = data.get('personas', [])
            career_pivot = data.get('career_pivot', {})
            target_companies = data.get('target_companies', {})
            blind_spots = data.get('blind_spots', [])
        except json.JSONDecodeError:
            diagnosis_html = diagnosis_response # Fallback if raw text
            scores = {}
            drift = {}
            personas = []
            career_pivot = {}
            target_companies = {}
            blind_spots = []
        
    finally:
        # Cleanup
        if os.path.exists(filepath):
            os.remove(filepath)
    
    return render_template('results.html', 
                          diagnosis=diagnosis_html, 
                          scores=scores, 
                          drift=drift, 
                          personas=personas, 
                          career_pivot=career_pivot,
                          target_companies=target_companies,
                          blind_spots=blind_spots,
                          job_title=job_title)
