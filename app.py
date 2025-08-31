"""
Flask web application for the AI-Powered Personalized Healthcare Assistant
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_cors import CORS
import traceback
from datetime import datetime

from healthcare_assistant import PersonalizedHealthcareAssistant
from sample_data import create_sample_patients
from models import Patient, VitalSigns, LabResults, MedicalHistory, Gender
from config import get_config
from database import PatientDatabase

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'healthcare_assistant_secret_key_2024'
CORS(app)

# Global assistant and database instances
assistant = None
db = None

def initialize_assistant():
    """Initialize and train the healthcare assistant"""
    global assistant, db
    try:
        config = get_config()
        assistant = PersonalizedHealthcareAssistant(config)

        # Initialize database
        db = PatientDatabase()

        # Check if database has patients, if not populate with sample data
        if db.get_patient_count() == 0:
            print("📊 Populating database with sample patients...")
            db.populate_sample_data()

        # Train with sample data from database
        all_patients_data = db.get_all_patients()
        training_patients = []
        for patient_data in all_patients_data:
            patient = db.get_patient_by_id(patient_data['patient_id'])
            if patient:
                training_patients.append(patient)

        training_results = assistant.train_model(training_patients)

        print(f"✅ Assistant initialized successfully!")
        print(f"   - Silhouette Score: {training_results['silhouette_score']:.3f}")
        print(f"   - Training Samples: {training_results['n_samples']}")
        print(f"   - Database Patients: {db.get_patient_count()}")

        return True
    except Exception as e:
        print(f"❌ Error initializing assistant: {e}")
        return False

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    """Patient analysis page"""
    if request.method == 'GET':
        return render_template('analyze.html')
    
    try:
        # Get form data
        data = request.get_json() if request.is_json else request.form
        
        # Create patient from form data
        patient = create_patient_from_form(data)
        
        # Generate wellness plan
        if assistant is None:
            return jsonify({'error': 'Assistant not initialized'}), 500
        
        wellness_plan = assistant.generate_wellness_plan(patient)
        
        # Convert to JSON-serializable format
        result = {
            'patient_info': {
                'name': patient.name,
                'patient_id': patient.patient_id,
                'age': patient.age,
                'gender': patient.gender.value,
                'bmi': patient.vitals.bmi
            },
            'cluster_analysis': {
                'cluster_id': wellness_plan.cluster_profile.cluster_id,
                'cluster_name': wellness_plan.cluster_profile.cluster_name,
                'similarity_score': round(wellness_plan.cluster_profile.similarity_score * 100, 1),
                'confidence_level': round(wellness_plan.cluster_profile.confidence_level * 100, 1),
                'characteristics': wellness_plan.cluster_profile.characteristics[:3]
            },
            'nutrition': {
                'foods_to_emphasize': wellness_plan.nutrition.foods_to_emphasize[:5],
                'foods_to_avoid': wellness_plan.nutrition.foods_to_avoid[:5],
                'meal_planning_tips': wellness_plan.nutrition.meal_planning_tips,
                'hydration_guidelines': wellness_plan.nutrition.hydration_guidelines
            },
            'lifestyle': {
                'exercise_type': wellness_plan.lifestyle.exercise_type,
                'exercise_frequency': wellness_plan.lifestyle.exercise_frequency,
                'sleep_recommendations': wellness_plan.lifestyle.sleep_recommendations[:3],
                'stress_management': wellness_plan.lifestyle.stress_management[:3]
            },
            'supplements': {
                'recommended_supplements': wellness_plan.supplements.recommended_supplements[:3],
                'contraindications': wellness_plan.supplements.contraindications
            },
            'safety_alerts': {
                'risk_level': wellness_plan.safety_alerts.risk_level.value,
                'follow_up_timeline': wellness_plan.safety_alerts.follow_up_timeline,
                'specialist_referrals': wellness_plan.safety_alerts.specialist_referrals,
                'warning_signs': wellness_plan.safety_alerts.warning_signs[:3]
            },
            'full_report': wellness_plan.to_formatted_report()
        }
        
        if request.is_json:
            return jsonify(result)
        else:
            return render_template('results.html', result=result)
            
    except Exception as e:
        error_msg = f"Error analyzing patient: {str(e)}"
        print(f"❌ {error_msg}")
        print(traceback.format_exc())
        
        if request.is_json:
            return jsonify({'error': error_msg}), 500
        else:
            flash(error_msg, 'error')
            return redirect(url_for('analyze'))

@app.route('/api/clusters')
def get_clusters():
    """API endpoint to get cluster information"""
    if assistant is None or not assistant.ml_engine.is_trained:
        return jsonify({'error': 'Assistant not initialized'}), 500
    
    clusters = []
    for cluster_id, profile in assistant.ml_engine.cluster_profiles.items():
        clusters.append({
            'cluster_id': cluster_id,
            'cluster_name': profile.cluster_name,
            'characteristics': profile.characteristics,
            'typical_conditions': profile.typical_conditions,
            'risk_factors': profile.risk_factors
        })
    
    return jsonify({'clusters': clusters})

@app.route('/demo')
def demo():
    """Demo page with pre-filled patient data"""
    return render_template('demo.html')

@app.route('/pharmacy')
def pharmacy():
    """Pharmacy interface for patient lookup"""
    return render_template('pharmacy.html')

@app.route('/api/search_patients')
def search_patients():
    """API endpoint to search patients by ID or name"""
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify({'patients': []})

    if db is None:
        return jsonify({'error': 'Database not initialized'}), 500

    try:
        patients = db.search_patients(query)
        return jsonify({'patients': patients})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patient/<patient_id>')
def get_patient_details(patient_id):
    """API endpoint to get patient details by ID"""
    if db is None:
        return jsonify({'error': 'Database not initialized'}), 500

    try:
        patient = db.get_patient_by_id(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404

        # Convert patient to JSON-serializable format
        patient_data = {
            'patient_id': patient.patient_id,
            'name': patient.name,
            'age': patient.age,
            'gender': patient.gender.value,
            'vitals': {
                'systolic_bp': patient.vitals.systolic_bp,
                'diastolic_bp': patient.vitals.diastolic_bp,
                'heart_rate': patient.vitals.heart_rate,
                'weight': patient.vitals.weight,
                'height': patient.vitals.height,
                'bmi': patient.vitals.bmi
            },
            'lab_results': {
                'fasting_glucose': patient.lab_results.fasting_glucose,
                'hba1c': patient.lab_results.hba1c,
                'total_cholesterol': patient.lab_results.total_cholesterol,
                'ldl_cholesterol': patient.lab_results.ldl_cholesterol,
                'hdl_cholesterol': patient.lab_results.hdl_cholesterol,
                'triglycerides': patient.lab_results.triglycerides
            },
            'medical_history': {
                'conditions': patient.medical_history.conditions,
                'medications': patient.medical_history.medications,
                'family_history': patient.medical_history.family_history
            },
            'symptoms': patient.symptoms
        }

        return jsonify({'patient': patient_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/pharmacy/analyze', methods=['POST'])
def pharmacy_analyze():
    """Analyze patient from pharmacy interface"""
    try:
        data = request.get_json()
        patient_identifier = data.get('patient_identifier', '').strip()

        if not patient_identifier:
            return jsonify({'error': 'Patient ID or name is required'}), 400

        if db is None:
            return jsonify({'error': 'Database not initialized'}), 500

        # Try to find patient by ID first, then by name
        patient = db.get_patient_by_id(patient_identifier)
        if not patient:
            patient = db.get_patient_by_name(patient_identifier)

        if not patient:
            return jsonify({'error': f'Patient not found: {patient_identifier}'}), 404

        # Generate wellness plan
        if assistant is None:
            return jsonify({'error': 'Assistant not initialized'}), 500

        wellness_plan = assistant.generate_wellness_plan(patient)

        # Convert to JSON-serializable format (same as analyze route)
        result = {
            'patient_info': {
                'name': patient.name,
                'patient_id': patient.patient_id,
                'age': patient.age,
                'gender': patient.gender.value,
                'bmi': patient.vitals.bmi
            },
            'cluster_analysis': {
                'cluster_id': wellness_plan.cluster_profile.cluster_id,
                'cluster_name': wellness_plan.cluster_profile.cluster_name,
                'similarity_score': round(wellness_plan.cluster_profile.similarity_score * 100, 1),
                'confidence_level': round(wellness_plan.cluster_profile.confidence_level * 100, 1),
                'characteristics': wellness_plan.cluster_profile.characteristics[:3]
            },
            'nutrition': {
                'foods_to_emphasize': wellness_plan.nutrition.foods_to_emphasize[:5],
                'foods_to_avoid': wellness_plan.nutrition.foods_to_avoid[:5],
                'meal_planning_tips': wellness_plan.nutrition.meal_planning_tips,
                'hydration_guidelines': wellness_plan.nutrition.hydration_guidelines
            },
            'lifestyle': {
                'exercise_type': wellness_plan.lifestyle.exercise_type,
                'exercise_frequency': wellness_plan.lifestyle.exercise_frequency,
                'sleep_recommendations': wellness_plan.lifestyle.sleep_recommendations[:3],
                'stress_management': wellness_plan.lifestyle.stress_management[:3]
            },
            'supplements': {
                'recommended_supplements': wellness_plan.supplements.recommended_supplements[:3],
                'contraindications': wellness_plan.supplements.contraindications
            },
            'safety_alerts': {
                'risk_level': wellness_plan.safety_alerts.risk_level.value,
                'follow_up_timeline': wellness_plan.safety_alerts.follow_up_timeline,
                'specialist_referrals': wellness_plan.safety_alerts.specialist_referrals,
                'warning_signs': wellness_plan.safety_alerts.warning_signs[:3]
            },
            'full_report': wellness_plan.to_formatted_report()
        }

        return jsonify(result)

    except Exception as e:
        error_msg = f"Error analyzing patient: {str(e)}"
        print(f"❌ {error_msg}")
        return jsonify({'error': error_msg}), 500

def create_patient_from_form(data):
    """Create a Patient object from form data"""
    # Basic info
    patient_id = data.get('patient_id', f"PT-{datetime.now().strftime('%Y%m%d%H%M%S')}")
    name = data.get('name', 'Anonymous Patient')
    age = int(data.get('age', 50))
    gender_str = data.get('gender', 'female').lower()
    
    gender = Gender.MALE if gender_str == 'male' else Gender.FEMALE if gender_str == 'female' else Gender.OTHER
    
    # Vitals
    vitals = VitalSigns(
        systolic_bp=int(data.get('systolic_bp', 120)) if data.get('systolic_bp') else None,
        diastolic_bp=int(data.get('diastolic_bp', 80)) if data.get('diastolic_bp') else None,
        heart_rate=int(data.get('heart_rate', 70)) if data.get('heart_rate') else None,
        weight=float(data.get('weight', 70)) if data.get('weight') else None,
        height=float(data.get('height', 170)) if data.get('height') else None
    )
    
    # Lab results
    lab_results = LabResults(
        fasting_glucose=float(data.get('fasting_glucose', 100)) if data.get('fasting_glucose') else None,
        hba1c=float(data.get('hba1c', 5.5)) if data.get('hba1c') else None,
        total_cholesterol=float(data.get('total_cholesterol', 200)) if data.get('total_cholesterol') else None,
        ldl_cholesterol=float(data.get('ldl_cholesterol', 130)) if data.get('ldl_cholesterol') else None,
        hdl_cholesterol=float(data.get('hdl_cholesterol', 50)) if data.get('hdl_cholesterol') else None,
        triglycerides=float(data.get('triglycerides', 150)) if data.get('triglycerides') else None,
        test_date=datetime.now()
    )
    
    # Medical history
    conditions = [c.strip() for c in data.get('conditions', '').split(',') if c.strip()]
    medications = [m.strip() for m in data.get('medications', '').split(',') if m.strip()]
    family_history = [f.strip() for f in data.get('family_history', '').split(',') if f.strip()]
    
    medical_history = MedicalHistory(
        conditions=conditions,
        medications=medications,
        family_history=family_history
    )
    
    return Patient(
        patient_id=patient_id,
        name=name,
        age=age,
        gender=gender,
        vitals=vitals,
        lab_results=lab_results,
        medical_history=medical_history
    )

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error="Internal server error"), 500

if __name__ == '__main__':
    print("🏥 Starting AI-Powered Personalized Healthcare Assistant Web App")
    print("=" * 60)
    
    # Initialize assistant
    if initialize_assistant():
        print("🚀 Starting Flask server...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to initialize assistant. Exiting.")
        exit(1)
