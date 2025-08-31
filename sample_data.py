"""
Sample patient data for testing the AI Healthcare Assistant
"""

from datetime import datetime, timedelta
from models import Patient, VitalSigns, LabResults, MedicalHistory, Gender

def create_sample_patients():
    """Create a diverse set of sample patients for testing"""
    
    patients = []
    
    # Patient 1: Healthy young adult
    patients.append(Patient(
        patient_id="PT-2024-0001",
        name="Alex Johnson",
        age=28,
        gender=Gender.MALE,
        vitals=VitalSigns(
            systolic_bp=118,
            diastolic_bp=75,
            heart_rate=68,
            temperature=98.6,
            weight=75,
            height=180
        ),
        lab_results=LabResults(
            fasting_glucose=88,
            hba1c=5.2,
            total_cholesterol=180,
            ldl_cholesterol=110,
            hdl_cholesterol=55,
            triglycerides=95,
            test_date=datetime.now() - timedelta(days=30)
        ),
        medical_history=MedicalHistory(
            conditions=[],
            medications=[],
            allergies=["Penicillin"],
            family_history=["Hypertension (father)"],
            lifestyle_factors={"exercise": "regular", "smoking": "never", "alcohol": "occasional"}
        ),
        symptoms=[]
    ))
    
    # Patient 2: Pre-diabetic with hypertension (Indian context)
    patients.append(Patient(
        patient_id="PT-2024-0002",
        name="Priya Sharma",
        age=52,
        gender=Gender.FEMALE,
        vitals=VitalSigns(
            systolic_bp=142,
            diastolic_bp=88,
            heart_rate=78,
            weight=82,
            height=165
        ),
        lab_results=LabResults(
            fasting_glucose=118,
            hba1c=6.1,
            total_cholesterol=245,
            ldl_cholesterol=165,
            hdl_cholesterol=38,
            triglycerides=220,
            test_date=datetime.now() - timedelta(days=15)
        ),
        medical_history=MedicalHistory(
            conditions=["Pre-diabetes", "Stage 1 Hypertension"],
            medications=["Telmisartan 40mg", "Metformin 500mg"],
            allergies=[],
            family_history=["Type 2 Diabetes (both parents)", "Heart disease (father)"],
            lifestyle_factors={"exercise": "sedentary", "smoking": "never", "alcohol": "occasional", "diet": "high carb Indian diet"}
        ),
        symptoms=["Fatigue", "Occasional headaches", "Frequent urination"]
    ))
    
    # Patient 3: Type 2 Diabetes with complications (Indian context)
    patients.append(Patient(
        patient_id="PT-2024-0003",
        name="Rajesh Kumar",
        age=64,
        gender=Gender.MALE,
        vitals=VitalSigns(
            systolic_bp=155,
            diastolic_bp=95,
            heart_rate=82,
            weight=95,
            height=175
        ),
        lab_results=LabResults(
            fasting_glucose=165,
            hba1c=8.2,
            total_cholesterol=280,
            ldl_cholesterol=190,
            hdl_cholesterol=32,
            triglycerides=350,
            creatinine=1.4,
            test_date=datetime.now() - timedelta(days=7)
        ),
        medical_history=MedicalHistory(
            conditions=["Type 2 Diabetes", "Hypertension", "Diabetic nephropathy"],
            medications=["Metformin 1000mg", "Glimepiride 2mg", "Amlodipine 5mg", "Atorvastatin 20mg"],
            allergies=["Sulfa drugs"],
            family_history=["Type 2 Diabetes (mother)", "Stroke (father)"],
            lifestyle_factors={"exercise": "limited", "smoking": "former", "alcohol": "none", "diet": "traditional Indian high carb"}
        ),
        symptoms=["Frequent urination", "Blurred vision", "Foot numbness", "Excessive thirst"]
    ))
    
    # Patient 4: Young adult with metabolic syndrome
    patients.append(Patient(
        patient_id="PT-2024-0004",
        name="Maria Rodriguez",
        age=35,
        gender=Gender.FEMALE,
        vitals=VitalSigns(
            systolic_bp=135,
            diastolic_bp=85,
            heart_rate=75,
            weight=88,
            height=160
        ),
        lab_results=LabResults(
            fasting_glucose=105,
            hba1c=5.9,
            total_cholesterol=220,
            ldl_cholesterol=145,
            hdl_cholesterol=35,
            triglycerides=180,
            test_date=datetime.now() - timedelta(days=20)
        ),
        medical_history=MedicalHistory(
            conditions=["Metabolic syndrome", "PCOS"],
            medications=["Metformin 500mg"],
            allergies=[],
            family_history=["Type 2 Diabetes (grandmother)", "Obesity (mother)"],
            lifestyle_factors={"exercise": "irregular", "smoking": "never", "alcohol": "social"}
        ),
        symptoms=["Weight gain", "Irregular periods", "Fatigue"]
    ))
    
    # Patient 5: Elderly with multiple comorbidities
    patients.append(Patient(
        patient_id="PT-2024-0005",
        name="Eleanor Thompson",
        age=78,
        gender=Gender.FEMALE,
        vitals=VitalSigns(
            systolic_bp=160,
            diastolic_bp=90,
            heart_rate=68,
            weight=68,
            height=158
        ),
        lab_results=LabResults(
            fasting_glucose=140,
            hba1c=7.1,
            total_cholesterol=200,
            ldl_cholesterol=120,
            hdl_cholesterol=45,
            triglycerides=150,
            creatinine=1.2,
            test_date=datetime.now() - timedelta(days=10)
        ),
        medical_history=MedicalHistory(
            conditions=["Type 2 Diabetes", "Hypertension", "Osteoporosis", "Mild cognitive impairment"],
            medications=["Insulin glargine", "Amlodipine 5mg", "Alendronate 70mg", "Vitamin D3"],
            allergies=["Aspirin"],
            family_history=["Alzheimer's disease (mother)", "Heart disease (father)"],
            lifestyle_factors={"exercise": "light walking", "smoking": "never", "alcohol": "none"}
        ),
        symptoms=["Memory issues", "Joint pain", "Dizziness"]
    ))
    
    # Patient 6: Athletic young adult
    patients.append(Patient(
        patient_id="PT-2024-0006",
        name="David Kim",
        age=24,
        gender=Gender.MALE,
        vitals=VitalSigns(
            systolic_bp=110,
            diastolic_bp=70,
            heart_rate=55,
            weight=70,
            height=178
        ),
        lab_results=LabResults(
            fasting_glucose=82,
            hba1c=4.8,
            total_cholesterol=160,
            ldl_cholesterol=95,
            hdl_cholesterol=65,
            triglycerides=75,
            test_date=datetime.now() - timedelta(days=45)
        ),
        medical_history=MedicalHistory(
            conditions=[],
            medications=[],
            allergies=[],
            family_history=["Hypertension (grandfather)"],
            lifestyle_factors={"exercise": "intense daily", "smoking": "never", "alcohol": "rare"}
        ),
        symptoms=[]
    ))
    
    # Patient 7: Middle-aged with cardiovascular risk
    patients.append(Patient(
        patient_id="PT-2024-0007",
        name="Jennifer Wilson",
        age=48,
        gender=Gender.FEMALE,
        vitals=VitalSigns(
            systolic_bp=148,
            diastolic_bp=92,
            heart_rate=80,
            weight=78,
            height=168
        ),
        lab_results=LabResults(
            fasting_glucose=95,
            hba1c=5.4,
            total_cholesterol=260,
            ldl_cholesterol=175,
            hdl_cholesterol=42,
            triglycerides=195,
            test_date=datetime.now() - timedelta(days=25)
        ),
        medical_history=MedicalHistory(
            conditions=["Hypertension", "Hyperlipidemia"],
            medications=["Losartan 50mg", "Simvastatin 20mg"],
            allergies=[],
            family_history=["Heart attack (father at 55)", "Stroke (mother at 68)"],
            lifestyle_factors={"exercise": "weekend only", "smoking": "former", "alcohol": "moderate"}
        ),
        symptoms=["Chest tightness with exertion", "Shortness of breath"]
    ))
    
    # Patient 8: Young adult with family history
    patients.append(Patient(
        patient_id="PT-2024-0008",
        name="Michael Brown",
        age=32,
        gender=Gender.MALE,
        vitals=VitalSigns(
            systolic_bp=125,
            diastolic_bp=80,
            heart_rate=72,
            weight=85,
            height=183
        ),
        lab_results=LabResults(
            fasting_glucose=98,
            hba1c=5.5,
            total_cholesterol=195,
            ldl_cholesterol=125,
            hdl_cholesterol=48,
            triglycerides=110,
            test_date=datetime.now() - timedelta(days=35)
        ),
        medical_history=MedicalHistory(
            conditions=[],
            medications=[],
            allergies=["Shellfish"],
            family_history=["Type 2 Diabetes (father, uncle)", "Heart disease (grandfather)"],
            lifestyle_factors={"exercise": "moderate", "smoking": "never", "alcohol": "social"}
        ),
        symptoms=[]
    ))
    
    return patients

def get_test_patient():
    """Get a specific test patient for demonstrations"""
    return Patient(
        patient_id="PT-2024-7891",
        name="Priya Sharma",
        age=52,
        gender=Gender.FEMALE,
        vitals=VitalSigns(
            systolic_bp=142,
            diastolic_bp=88,
            heart_rate=78,
            weight=82,
            height=165
        ),
        lab_results=LabResults(
            fasting_glucose=118,
            hba1c=6.1,
            total_cholesterol=245,
            ldl_cholesterol=165,
            hdl_cholesterol=38,
            triglycerides=220,
            test_date=datetime.now() - timedelta(days=15)
        ),
        medical_history=MedicalHistory(
            conditions=["Pre-diabetes", "Stage 1 Hypertension"],
            medications=["Telmisartan 40mg", "Metformin 500mg"],
            allergies=[],
            family_history=["Type 2 Diabetes (both parents)", "Heart disease (father)"],
            lifestyle_factors={"exercise": "sedentary", "smoking": "never", "alcohol": "occasional", "diet": "high carb Indian diet"}
        ),
        symptoms=["Fatigue", "Occasional headaches", "Frequent urination"]
    )
