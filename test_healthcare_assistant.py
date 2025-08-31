"""
Test suite for the AI-Powered Personalized Healthcare Assistant
"""

import pytest
import numpy as np
from datetime import datetime

from healthcare_assistant import PersonalizedHealthcareAssistant
from sample_data import create_sample_patients, get_test_patient
from models import Patient, VitalSigns, LabResults, MedicalHistory, Gender, RiskLevel
from config import Config

class TestHealthcareAssistant:
    """Test cases for the healthcare assistant"""
    
    @pytest.fixture
    def assistant(self):
        """Create a healthcare assistant instance for testing"""
        config = Config()
        assistant = PersonalizedHealthcareAssistant(config)
        
        # Train with sample data
        training_patients = create_sample_patients()
        assistant.train_model(training_patients)
        
        return assistant
    
    @pytest.fixture
    def test_patient(self):
        """Create a test patient"""
        return get_test_patient()
    
    def test_model_training(self):
        """Test ML model training"""
        assistant = PersonalizedHealthcareAssistant()
        training_patients = create_sample_patients()
        
        results = assistant.train_model(training_patients)
        
        assert 'silhouette_score' in results
        assert results['silhouette_score'] > -1 and results['silhouette_score'] <= 1
        assert results['n_samples'] == len(training_patients)
        assert assistant.ml_engine.is_trained
    
    def test_wellness_plan_generation(self, assistant, test_patient):
        """Test wellness plan generation"""
        wellness_plan = assistant.generate_wellness_plan(test_patient)
        
        # Check that all components are present
        assert wellness_plan.patient == test_patient
        assert wellness_plan.cluster_profile is not None
        assert wellness_plan.pca_features is not None
        assert wellness_plan.nutrition is not None
        assert wellness_plan.lifestyle is not None
        assert wellness_plan.supplements is not None
        assert wellness_plan.safety_alerts is not None
        
        # Check cluster profile
        assert 0 <= wellness_plan.cluster_profile.cluster_id < 5
        assert 0 <= wellness_plan.cluster_profile.similarity_score <= 1
        assert 0 <= wellness_plan.cluster_profile.confidence_level <= 1
        
        # Check PCA features
        assert len(wellness_plan.pca_features.explained_variance) == 3
        assert wellness_plan.pca_features.feature_importance is not None
    
    def test_nutrition_recommendations(self, assistant, test_patient):
        """Test nutrition recommendation generation"""
        wellness_plan = assistant.generate_wellness_plan(test_patient)
        nutrition = wellness_plan.nutrition
        
        # Check that recommendations are provided
        assert len(nutrition.foods_to_emphasize) > 0
        assert len(nutrition.foods_to_avoid) > 0
        assert nutrition.hydration_guidelines is not None
        
        # Check for diabetes-specific recommendations (test patient is pre-diabetic)
        foods_str = ' '.join(nutrition.foods_to_emphasize).lower()
        assert any(food in foods_str for food in ['vegetable', 'protein', 'whole grain'])
        
        avoid_str = ' '.join(nutrition.foods_to_avoid).lower()
        assert any(food in avoid_str for food in ['sugar', 'processed', 'refined'])
    
    def test_lifestyle_recommendations(self, assistant, test_patient):
        """Test lifestyle recommendation generation"""
        wellness_plan = assistant.generate_wellness_plan(test_patient)
        lifestyle = wellness_plan.lifestyle
        
        # Check that all fields are populated
        assert lifestyle.exercise_type is not None
        assert lifestyle.exercise_frequency is not None
        assert lifestyle.exercise_duration is not None
        assert lifestyle.exercise_intensity is not None
        assert len(lifestyle.sleep_recommendations) > 0
        assert len(lifestyle.stress_management) > 0
    
    def test_supplement_recommendations(self, assistant, test_patient):
        """Test supplement recommendation generation"""
        wellness_plan = assistant.generate_wellness_plan(test_patient)
        supplements = wellness_plan.supplements
        
        # Check that recommendations are provided
        assert len(supplements.recommended_supplements) > 0
        
        # Check supplement structure
        for supplement in supplements.recommended_supplements:
            assert 'name' in supplement
            assert 'dosage' in supplement
            assert 'timing' in supplement
    
    def test_safety_alerts(self, assistant, test_patient):
        """Test safety alert generation"""
        wellness_plan = assistant.generate_wellness_plan(test_patient)
        safety = wellness_plan.safety_alerts
        
        # Check risk level assignment
        assert safety.risk_level in [RiskLevel.LOW, RiskLevel.MODERATE, RiskLevel.HIGH, RiskLevel.CRITICAL]
        assert safety.follow_up_timeline is not None
        
        # For pre-diabetic patient, should have moderate risk
        assert safety.risk_level in [RiskLevel.MODERATE, RiskLevel.HIGH]
    
    def test_high_risk_patient(self, assistant):
        """Test analysis of high-risk patient"""
        # Create high-risk patient
        high_risk_patient = Patient(
            patient_id="PT-HIGH-RISK",
            name="High Risk Patient",
            age=65,
            gender=Gender.MALE,
            vitals=VitalSigns(
                systolic_bp=185,  # Very high BP
                diastolic_bp=110,
                weight=100,
                height=170
            ),
            lab_results=LabResults(
                fasting_glucose=200,  # Diabetic range
                hba1c=9.5,  # Poor control
                total_cholesterol=300,
                test_date=datetime.now()
            ),
            medical_history=MedicalHistory(
                conditions=["Type 2 Diabetes", "Hypertension", "Heart disease"],
                medications=["Insulin", "Multiple BP medications"],
                family_history=["Heart attack", "Stroke"]
            )
        )
        
        wellness_plan = assistant.generate_wellness_plan(high_risk_patient)
        
        # Should be high or critical risk
        assert wellness_plan.safety_alerts.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]
        
        # Should have specialist referrals
        assert len(wellness_plan.safety_alerts.specialist_referrals) > 0
        
        # Should have activity modifications
        assert len(wellness_plan.lifestyle.activity_modifications) > 0
    
    def test_healthy_patient(self, assistant):
        """Test analysis of healthy patient"""
        # Create healthy patient
        healthy_patient = Patient(
            patient_id="PT-HEALTHY",
            name="Healthy Patient",
            age=25,
            gender=Gender.FEMALE,
            vitals=VitalSigns(
                systolic_bp=110,
                diastolic_bp=70,
                weight=60,
                height=165
            ),
            lab_results=LabResults(
                fasting_glucose=85,
                hba1c=5.0,
                total_cholesterol=160,
                hdl_cholesterol=60,
                test_date=datetime.now()
            ),
            medical_history=MedicalHistory(
                conditions=[],
                medications=[],
                family_history=[]
            )
        )
        
        wellness_plan = assistant.generate_wellness_plan(healthy_patient)
        
        # Should be low risk
        assert wellness_plan.safety_alerts.risk_level == RiskLevel.LOW
        
        # Should have general wellness recommendations
        assert len(wellness_plan.nutrition.foods_to_emphasize) > 0
        assert len(wellness_plan.supplements.recommended_supplements) > 0
    
    def test_formatted_report(self, assistant, test_patient):
        """Test formatted report generation"""
        wellness_plan = assistant.generate_wellness_plan(test_patient)
        report = wellness_plan.to_formatted_report()
        
        # Check that report contains key sections
        assert "Personalized Wellness Plan" in report
        assert "Cluster Analysis Summary" in report
        assert "Current Health Assessment" in report
        assert "Nutritional Recommendations" in report
        assert "Lifestyle & Activity Guidelines" in report
        assert "Supplement Considerations" in report
        assert "Important Safety Notes" in report
        assert "Disclaimer" in report
        
        # Check patient information is included
        assert test_patient.name in report
        assert test_patient.patient_id in report

def run_tests():
    """Run all tests"""
    print("🧪 Running Healthcare Assistant Tests")
    print("=" * 40)
    
    # Run pytest
    pytest.main([__file__, "-v"])

if __name__ == "__main__":
    run_tests()
