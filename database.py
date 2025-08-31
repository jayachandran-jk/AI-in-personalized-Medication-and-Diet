"""
Database module for storing and retrieving patient information
"""

import sqlite3
import json
from typing import List, Optional, Dict, Any
from datetime import datetime
import os

from models import Patient, VitalSigns, LabResults, MedicalHistory, Gender

class PatientDatabase:
    """SQLite database for patient management"""
    
    def __init__(self, db_path: str = "patients.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create patients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create vitals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vitals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL,
                systolic_bp INTEGER,
                diastolic_bp INTEGER,
                heart_rate INTEGER,
                temperature REAL,
                respiratory_rate INTEGER,
                oxygen_saturation REAL,
                weight REAL,
                height REAL,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
            )
        ''')
        
        # Create lab_results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lab_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL,
                fasting_glucose REAL,
                hba1c REAL,
                total_cholesterol REAL,
                ldl_cholesterol REAL,
                hdl_cholesterol REAL,
                triglycerides REAL,
                creatinine REAL,
                bun REAL,
                test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
            )
        ''')
        
        # Create medical_history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medical_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL,
                conditions TEXT,
                medications TEXT,
                allergies TEXT,
                family_history TEXT,
                surgeries TEXT,
                lifestyle_factors TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
            )
        ''')
        
        # Create symptoms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS symptoms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL,
                symptoms TEXT,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_patient(self, patient: Patient) -> bool:
        """Add a new patient to the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Insert patient basic info
            cursor.execute('''
                INSERT OR REPLACE INTO patients (patient_id, name, age, gender)
                VALUES (?, ?, ?, ?)
            ''', (patient.patient_id, patient.name, patient.age, patient.gender.value))
            
            # Insert vitals
            if patient.vitals:
                cursor.execute('''
                    INSERT OR REPLACE INTO vitals 
                    (patient_id, systolic_bp, diastolic_bp, heart_rate, temperature, 
                     respiratory_rate, oxygen_saturation, weight, height)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    patient.patient_id,
                    patient.vitals.systolic_bp,
                    patient.vitals.diastolic_bp,
                    patient.vitals.heart_rate,
                    patient.vitals.temperature,
                    patient.vitals.respiratory_rate,
                    patient.vitals.oxygen_saturation,
                    patient.vitals.weight,
                    patient.vitals.height
                ))
            
            # Insert lab results
            if patient.lab_results:
                cursor.execute('''
                    INSERT OR REPLACE INTO lab_results 
                    (patient_id, fasting_glucose, hba1c, total_cholesterol, 
                     ldl_cholesterol, hdl_cholesterol, triglycerides, creatinine, bun, test_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    patient.patient_id,
                    patient.lab_results.fasting_glucose,
                    patient.lab_results.hba1c,
                    patient.lab_results.total_cholesterol,
                    patient.lab_results.ldl_cholesterol,
                    patient.lab_results.hdl_cholesterol,
                    patient.lab_results.triglycerides,
                    patient.lab_results.creatinine,
                    patient.lab_results.bun,
                    patient.lab_results.test_date
                ))
            
            # Insert medical history
            if patient.medical_history:
                cursor.execute('''
                    INSERT OR REPLACE INTO medical_history 
                    (patient_id, conditions, medications, allergies, family_history, surgeries, lifestyle_factors)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    patient.patient_id,
                    json.dumps(patient.medical_history.conditions),
                    json.dumps(patient.medical_history.medications),
                    json.dumps(patient.medical_history.allergies),
                    json.dumps(patient.medical_history.family_history),
                    json.dumps(patient.medical_history.surgeries),
                    json.dumps(patient.medical_history.lifestyle_factors)
                ))
            
            # Insert symptoms
            if patient.symptoms:
                cursor.execute('''
                    INSERT OR REPLACE INTO symptoms (patient_id, symptoms)
                    VALUES (?, ?)
                ''', (patient.patient_id, json.dumps(patient.symptoms)))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error adding patient: {e}")
            return False
    
    def get_patient_by_id(self, patient_id: str) -> Optional[Patient]:
        """Retrieve a patient by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get patient basic info
            cursor.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,))
            patient_row = cursor.fetchone()
            
            if not patient_row:
                conn.close()
                return None
            
            # Get vitals
            cursor.execute('SELECT * FROM vitals WHERE patient_id = ? ORDER BY recorded_at DESC LIMIT 1', (patient_id,))
            vitals_row = cursor.fetchone()
            
            # Get lab results
            cursor.execute('SELECT * FROM lab_results WHERE patient_id = ? ORDER BY test_date DESC LIMIT 1', (patient_id,))
            lab_row = cursor.fetchone()
            
            # Get medical history
            cursor.execute('SELECT * FROM medical_history WHERE patient_id = ? ORDER BY updated_at DESC LIMIT 1', (patient_id,))
            history_row = cursor.fetchone()
            
            # Get symptoms
            cursor.execute('SELECT * FROM symptoms WHERE patient_id = ? ORDER BY recorded_at DESC LIMIT 1', (patient_id,))
            symptoms_row = cursor.fetchone()
            
            conn.close()
            
            # Construct Patient object
            return self._construct_patient(patient_row, vitals_row, lab_row, history_row, symptoms_row)
            
        except Exception as e:
            print(f"Error retrieving patient: {e}")
            return None
    
    def get_patient_by_name(self, name: str) -> Optional[Patient]:
        """Retrieve a patient by name (case-insensitive)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get patient basic info
            cursor.execute('SELECT * FROM patients WHERE LOWER(name) = LOWER(?)', (name,))
            patient_row = cursor.fetchone()
            
            if not patient_row:
                conn.close()
                return None
            
            patient_id = patient_row[0]  # patient_id is the first column
            conn.close()
            
            # Use get_patient_by_id to get complete patient data
            return self.get_patient_by_id(patient_id)
            
        except Exception as e:
            print(f"Error retrieving patient by name: {e}")
            return None
    
    def search_patients(self, query: str) -> List[Dict[str, Any]]:
        """Search patients by ID or name"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT patient_id, name, age, gender 
                FROM patients 
                WHERE LOWER(patient_id) LIKE LOWER(?) OR LOWER(name) LIKE LOWER(?)
                ORDER BY name
            ''', (f'%{query}%', f'%{query}%'))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    'patient_id': row[0],
                    'name': row[1],
                    'age': row[2],
                    'gender': row[3]
                })
            
            conn.close()
            return results
            
        except Exception as e:
            print(f"Error searching patients: {e}")
            return []
    
    def get_all_patients(self) -> List[Dict[str, Any]]:
        """Get list of all patients (basic info only)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT patient_id, name, age, gender FROM patients ORDER BY name')
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    'patient_id': row[0],
                    'name': row[1],
                    'age': row[2],
                    'gender': row[3]
                })
            
            conn.close()
            return results
            
        except Exception as e:
            print(f"Error getting all patients: {e}")
            return []
    
    def _construct_patient(self, patient_row, vitals_row, lab_row, history_row, symptoms_row) -> Patient:
        """Construct a Patient object from database rows"""
        
        # Basic patient info
        patient_id, name, age, gender_str, created_at, updated_at = patient_row
        gender = Gender(gender_str)
        
        # Vitals
        vitals = VitalSigns()
        if vitals_row:
            vitals = VitalSigns(
                systolic_bp=vitals_row[2],
                diastolic_bp=vitals_row[3],
                heart_rate=vitals_row[4],
                temperature=vitals_row[5],
                respiratory_rate=vitals_row[6],
                oxygen_saturation=vitals_row[7],
                weight=vitals_row[8],
                height=vitals_row[9]
            )
        
        # Lab results
        lab_results = LabResults()
        if lab_row:
            lab_results = LabResults(
                fasting_glucose=lab_row[2],
                hba1c=lab_row[3],
                total_cholesterol=lab_row[4],
                ldl_cholesterol=lab_row[5],
                hdl_cholesterol=lab_row[6],
                triglycerides=lab_row[7],
                creatinine=lab_row[8],
                bun=lab_row[9],
                test_date=datetime.fromisoformat(lab_row[10]) if lab_row[10] else None
            )
        
        # Medical history
        medical_history = MedicalHistory()
        if history_row:
            medical_history = MedicalHistory(
                conditions=json.loads(history_row[2]) if history_row[2] else [],
                medications=json.loads(history_row[3]) if history_row[3] else [],
                allergies=json.loads(history_row[4]) if history_row[4] else [],
                family_history=json.loads(history_row[5]) if history_row[5] else [],
                surgeries=json.loads(history_row[6]) if history_row[6] else [],
                lifestyle_factors=json.loads(history_row[7]) if history_row[7] else {}
            )
        
        # Symptoms
        symptoms = []
        if symptoms_row:
            symptoms = json.loads(symptoms_row[2]) if symptoms_row[2] else []
        
        return Patient(
            patient_id=patient_id,
            name=name,
            age=age,
            gender=gender,
            vitals=vitals,
            lab_results=lab_results,
            medical_history=medical_history,
            symptoms=symptoms,
            created_at=datetime.fromisoformat(created_at) if created_at else datetime.now()
        )
    
    def populate_sample_data(self):
        """Populate database with sample patients"""
        from sample_data import create_sample_patients
        
        sample_patients = create_sample_patients()
        
        for patient in sample_patients:
            self.add_patient(patient)
        
        print(f"✅ Added {len(sample_patients)} sample patients to database")
    
    def get_patient_count(self) -> int:
        """Get total number of patients in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM patients')
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception as e:
            print(f"Error getting patient count: {e}")
            return 0
