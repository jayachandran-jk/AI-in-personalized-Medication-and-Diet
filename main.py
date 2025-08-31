"""
Main application for the AI-Powered Personalized Healthcare Assistant
"""

import os
import sys
from typing import List
import pandas as pd

from healthcare_assistant import PersonalizedHealthcareAssistant
from sample_data import create_sample_patients, get_test_patient
from models import Patient
from config import get_config

def main():
    """Main application entry point"""
    print("🏥 AI-Powered Personalized Healthcare Assistant")
    print("=" * 50)
    
    # Initialize configuration and assistant
    config = get_config()
    assistant = PersonalizedHealthcareAssistant(config)
    
    # Create sample patients for training
    print("📊 Creating sample patient data...")
    training_patients = create_sample_patients()
    print(f"✅ Created {len(training_patients)} sample patients")
    
    # Train the ML model
    print("\n🤖 Training machine learning model...")
    try:
        training_results = assistant.train_model(training_patients)
        print(f"✅ Model trained successfully!")
        print(f"   - Silhouette Score: {training_results['silhouette_score']:.3f}")
        print(f"   - Number of Clusters: {config.ML_CONFIG['n_clusters']}")
        print(f"   - PCA Components: {config.ML_CONFIG['pca_components']}")
        print(f"   - Training Samples: {training_results['n_samples']}")
    except Exception as e:
        print(f"❌ Error training model: {e}")
        return
    
    # Demonstrate with test patient
    print("\n👤 Analyzing test patient...")
    test_patient = get_test_patient()
    
    try:
        # Generate wellness plan
        wellness_plan = assistant.generate_wellness_plan(test_patient)
        
        # Display results
        print("\n📋 PERSONALIZED WELLNESS PLAN")
        print("=" * 50)
        print(wellness_plan.to_formatted_report())
        
        # Save results to file
        output_file = "wellness_plan_output.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(wellness_plan.to_formatted_report())
        print(f"\n💾 Wellness plan saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error generating wellness plan: {e}")
        return
    
    # Interactive mode
    print("\n🔄 Interactive Mode")
    print("=" * 30)
    
    while True:
        print("\nOptions:")
        print("1. Analyze another patient")
        print("2. View cluster information")
        print("3. Export training data")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            analyze_custom_patient(assistant)
        elif choice == "2":
            display_cluster_info(assistant)
        elif choice == "3":
            export_training_data(training_patients)
        elif choice == "4":
            print("👋 Thank you for using the AI Healthcare Assistant!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

def analyze_custom_patient(assistant: PersonalizedHealthcareAssistant):
    """Interactive patient analysis"""
    print("\n📝 Enter Patient Information")
    print("-" * 30)
    
    try:
        # Get basic patient info
        patient_id = input("Patient ID: ").strip() or f"PT-{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"
        name = input("Patient Name: ").strip() or "Test Patient"
        age = int(input("Age: ").strip() or "50")
        gender_input = input("Gender (male/female/other): ").strip().lower() or "female"
        
        from models import Gender
        gender = Gender.MALE if gender_input == "male" else Gender.FEMALE if gender_input == "female" else Gender.OTHER
        
        # Get vitals
        print("\n🩺 Vital Signs:")
        systolic_bp = int(input("Systolic BP (mmHg): ").strip() or "120")
        diastolic_bp = int(input("Diastolic BP (mmHg): ").strip() or "80")
        weight = float(input("Weight (kg): ").strip() or "70")
        height = float(input("Height (cm): ").strip() or "170")
        
        # Get lab results
        print("\n🧪 Lab Results:")
        fasting_glucose = float(input("Fasting Glucose (mg/dL): ").strip() or "100")
        hba1c = float(input("HbA1c (%): ").strip() or "5.5")
        total_cholesterol = float(input("Total Cholesterol (mg/dL): ").strip() or "200")
        
        # Create patient object
        from models import VitalSigns, LabResults, MedicalHistory
        from datetime import datetime
        
        patient = Patient(
            patient_id=patient_id,
            name=name,
            age=age,
            gender=gender,
            vitals=VitalSigns(
                systolic_bp=systolic_bp,
                diastolic_bp=diastolic_bp,
                weight=weight,
                height=height
            ),
            lab_results=LabResults(
                fasting_glucose=fasting_glucose,
                hba1c=hba1c,
                total_cholesterol=total_cholesterol,
                test_date=datetime.now()
            ),
            medical_history=MedicalHistory()
        )
        
        # Generate wellness plan
        print("\n🔄 Generating wellness plan...")
        wellness_plan = assistant.generate_wellness_plan(patient)
        
        print("\n📋 WELLNESS PLAN RESULTS")
        print("=" * 40)
        print(wellness_plan.to_formatted_report())
        
    except ValueError as e:
        print(f"❌ Invalid input: {e}")
    except Exception as e:
        print(f"❌ Error analyzing patient: {e}")

def display_cluster_info(assistant: PersonalizedHealthcareAssistant):
    """Display information about ML clusters"""
    print("\n🎯 Cluster Information")
    print("=" * 30)
    
    if not assistant.ml_engine.is_trained:
        print("❌ Model not trained yet.")
        return
    
    for cluster_id, profile in assistant.ml_engine.cluster_profiles.items():
        print(f"\n📊 Cluster {cluster_id}: {profile.cluster_name}")
        print(f"   Characteristics: {', '.join(profile.characteristics[:3])}...")
        print(f"   Typical Conditions: {', '.join(profile.typical_conditions) or 'None'}")
        print(f"   Risk Factors: {', '.join(profile.risk_factors) or 'None'}")

def export_training_data(patients: List[Patient]):
    """Export training data to CSV"""
    print("\n💾 Exporting Training Data")
    print("-" * 30)
    
    try:
        # Convert patients to DataFrame
        patient_data = []
        for patient in patients:
            data = patient.to_dict()
            data['name'] = patient.name
            data['conditions'] = '; '.join(patient.medical_history.conditions)
            data['medications'] = '; '.join(patient.medical_history.medications)
            data['family_history'] = '; '.join(patient.medical_history.family_history)
            patient_data.append(data)
        
        df = pd.DataFrame(patient_data)
        
        # Save to CSV
        filename = "training_data_export.csv"
        df.to_csv(filename, index=False)
        print(f"✅ Training data exported to: {filename}")
        print(f"   Records: {len(df)}")
        print(f"   Columns: {len(df.columns)}")
        
    except Exception as e:
        print(f"❌ Error exporting data: {e}")

if __name__ == "__main__":
    main()
