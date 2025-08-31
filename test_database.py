#!/usr/bin/env python3
"""
Test script for the patient database functionality
"""

from database import PatientDatabase
from sample_data import create_sample_patients

def main():
    print("🗄️ Testing Patient Database Functionality")
    print("=" * 50)
    
    # Initialize database
    print("📊 Initializing database...")
    db = PatientDatabase("test_patients.db")
    
    # Populate with sample data
    print("📋 Adding sample patients...")
    sample_patients = create_sample_patients()
    
    for patient in sample_patients:
        success = db.add_patient(patient)
        if success:
            print(f"✅ Added: {patient.name} ({patient.patient_id})")
        else:
            print(f"❌ Failed to add: {patient.name}")
    
    print(f"\n📊 Total patients in database: {db.get_patient_count()}")
    
    # Test patient retrieval by ID
    print("\n🔍 Testing patient retrieval by ID...")
    test_id = "PT-2024-0002"
    patient = db.get_patient_by_id(test_id)
    
    if patient:
        print(f"✅ Found patient by ID: {patient.name}")
        print(f"   Age: {patient.age}, Gender: {patient.gender.value}")
        print(f"   BMI: {patient.vitals.bmi}")
        print(f"   Conditions: {', '.join(patient.medical_history.conditions)}")
    else:
        print(f"❌ Patient not found: {test_id}")
    
    # Test patient retrieval by name
    print("\n🔍 Testing patient retrieval by name...")
    test_name = "Sarah Johnson"
    patient = db.get_patient_by_name(test_name)
    
    if patient:
        print(f"✅ Found patient by name: {patient.name} ({patient.patient_id})")
        print(f"   BP: {patient.vitals.systolic_bp}/{patient.vitals.diastolic_bp} mmHg")
        print(f"   HbA1c: {patient.lab_results.hba1c}%")
    else:
        print(f"❌ Patient not found: {test_name}")
    
    # Test patient search
    print("\n🔍 Testing patient search...")
    search_results = db.search_patients("Johnson")
    print(f"Search results for 'Johnson': {len(search_results)} patients")
    
    for result in search_results:
        print(f"   - {result['name']} ({result['patient_id']}) - {result['age']} years")
    
    # Test getting all patients
    print("\n📋 All patients in database:")
    all_patients = db.get_all_patients()
    
    for patient_info in all_patients:
        print(f"   - {patient_info['name']} ({patient_info['patient_id']}) - {patient_info['age']}y, {patient_info['gender']}")
    
    print("\n✅ Database testing completed successfully!")
    print(f"Database file: test_patients.db")

if __name__ == "__main__":
    main()
