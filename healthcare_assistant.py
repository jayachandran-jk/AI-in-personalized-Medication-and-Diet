"""
AI-Powered Personalized Healthcare Assistant
Main class for generating personalized wellness recommendations
"""

from typing import Dict, List, Tuple, Any
import numpy as np
from datetime import datetime

from models import (
    Patient, ClusterProfile, PCAFeatures, WellnessPlan,
    NutritionRecommendation, LifestyleRecommendation, 
    SupplementRecommendation, SafetyAlert, RiskLevel
)
from ml_engine import HealthMLEngine
from config import Config

class PersonalizedHealthcareAssistant:
    """Main AI assistant for personalized healthcare recommendations"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.ml_engine = HealthMLEngine(self.config)
        
    def train_model(self, training_patients: List[Patient]) -> Dict[str, Any]:
        """Train the ML model with patient data"""
        return self.ml_engine.train_clustering_model(training_patients)
    
    def generate_wellness_plan(self, patient: Patient) -> WellnessPlan:
        """Generate complete personalized wellness plan for a patient"""
        
        # Get ML analysis
        cluster_profile, pca_features = self.ml_engine.analyze_patient(patient)
        
        # Generate recommendations
        nutrition = self._generate_nutrition_recommendations(patient, cluster_profile)
        lifestyle = self._generate_lifestyle_recommendations(patient, cluster_profile)
        supplements = self._generate_supplement_recommendations(patient, cluster_profile)
        safety_alerts = self._generate_safety_alerts(patient, cluster_profile)
        
        # Create wellness plan
        wellness_plan = WellnessPlan(
            patient=patient,
            cluster_profile=cluster_profile,
            pca_features=pca_features,
            nutrition=nutrition,
            lifestyle=lifestyle,
            supplements=supplements,
            safety_alerts=safety_alerts
        )
        
        return wellness_plan
    
    def _generate_nutrition_recommendations(self, patient: Patient, 
                                          cluster_profile: ClusterProfile) -> NutritionRecommendation:
        """Generate personalized nutrition recommendations"""
        
        foods_to_emphasize = []
        foods_to_avoid = []
        meal_planning_tips = []
        special_considerations = []
        
        # Base Indian dietary recommendations for all patients
        foods_to_emphasize.extend([
            "Green leafy vegetables (palak, methi, spinach)",
            "Lentils (moong dal, masoor dal, chana dal)",
            "Seasonal fruits (guava, papaya, apple)",
            "Whole grains (brown rice, bajra, jowar, ragi)",
            "Curd and buttermilk",
            "Turmeric, ginger, garlic"
        ])

        foods_to_avoid.extend([
            "Deep fried foods (samosa, pakora, puri)",
            "Sweets and mithai",
            "Refined flour products (maida)",
            "Excessive salt and pickles",
            "Processed and packaged foods"
        ])
        
        # Condition-specific recommendations
        conditions = [c.lower() for c in patient.medical_history.conditions]
        
        # Diabetes/Pre-diabetes recommendations
        if (patient.lab_results.hba1c and patient.lab_results.hba1c >= 5.7) or \
           (patient.lab_results.fasting_glucose and patient.lab_results.fasting_glucose >= 100) or \
           any('diabetes' in c for c in conditions):
            
            foods_to_emphasize.extend(self.config.NUTRITION_DATABASE['diabetes_risk']['recommended'])
            foods_to_avoid.extend(self.config.NUTRITION_DATABASE['diabetes_risk']['avoid'])
            meal_planning_tips.extend([
                "Eat 5-6 small meals throughout the day",
                "Include protein in every meal (dal, paneer, curd)",
                "Reduce rice quantity, prefer roti (whole wheat bread)",
                "Include bitter gourd, fenugreek leaves, and black plum in diet",
                "Walk for 10-15 minutes after meals"
            ])
            special_considerations.append("Monitor blood glucose levels as recommended by healthcare provider")
        
        # Cardiovascular risk recommendations
        if (patient.vitals.systolic_bp and patient.vitals.systolic_bp >= 130) or \
           (patient.lab_results.total_cholesterol and patient.lab_results.total_cholesterol >= 200) or \
           any('hypertension' in c or 'heart' in c for c in conditions):
            
            foods_to_emphasize.extend(self.config.NUTRITION_DATABASE['cardiovascular_risk']['recommended'])
            foods_to_avoid.extend(self.config.NUTRITION_DATABASE['cardiovascular_risk']['avoid'])
            meal_planning_tips.extend([
                "Drink arjuna bark decoction for heart health",
                "Reduce salt intake - avoid pickles and papad",
                "Include fish 2-3 times per week",
                "Include flaxseeds and walnuts in diet",
                "Drink coconut water regularly"
            ])
        
        # Hypertension-specific recommendations
        if patient.vitals.systolic_bp and patient.vitals.systolic_bp >= 130:
            foods_to_emphasize.extend(self.config.NUTRITION_DATABASE['hypertension']['recommended'])
            foods_to_avoid.extend(self.config.NUTRITION_DATABASE['hypertension']['avoid'])
            special_considerations.append("Monitor blood pressure regularly")
        
        # Weight management recommendations (Indian context)
        if patient.vitals.bmi and patient.vitals.bmi >= 25:
            meal_planning_tips.extend([
                "Fill half your plate with vegetables",
                "Eat slowly and chew properly",
                "Have salad before main meal",
                "Reduce sugar and ghee intake",
                "Have early dinner"
            ])
            special_considerations.append("Consult a dietitian for personalized meal planning")
        
        # Remove duplicates and format
        foods_to_emphasize = list(set(foods_to_emphasize))
        foods_to_avoid = list(set(foods_to_avoid))
        
        return NutritionRecommendation(
            foods_to_emphasize=foods_to_emphasize,
            foods_to_avoid=foods_to_avoid,
            meal_planning_tips=meal_planning_tips,
            hydration_guidelines="Drink 8-10 glasses of water daily, include coconut water and buttermilk in summer",
            special_considerations=special_considerations
        )
    
    def _generate_lifestyle_recommendations(self, patient: Patient, 
                                          cluster_profile: ClusterProfile) -> LifestyleRecommendation:
        """Generate personalized lifestyle and exercise recommendations"""
        
        # Determine fitness level based on age, conditions, and BMI
        fitness_level = "beginner"
        
        if patient.age < 40 and not patient.medical_history.conditions and \
           (not patient.vitals.bmi or patient.vitals.bmi < 30):
            fitness_level = "intermediate"
        
        if patient.age < 30 and not patient.medical_history.conditions and \
           (not patient.vitals.bmi or patient.vitals.bmi < 25):
            fitness_level = "advanced"
        
        # Get base exercise guidelines
        exercise_guidelines = self.config.EXERCISE_GUIDELINES[fitness_level]
        
        # Modify based on conditions
        activity_modifications = []
        conditions = [c.lower() for c in patient.medical_history.conditions]
        
        if any('heart' in c for c in conditions) or \
           (patient.vitals.systolic_bp and patient.vitals.systolic_bp >= 140):
            activity_modifications.append("Avoid high-intensity exercise without medical clearance")
            activity_modifications.append("Monitor heart rate during exercise")
        
        if any('diabetes' in c for c in conditions):
            activity_modifications.append("Monitor blood glucose before and after exercise")
            activity_modifications.append("Carry fast-acting carbohydrates during exercise")
        
        if patient.vitals.bmi and patient.vitals.bmi >= 35:
            activity_modifications.append("Start with low-impact activities (swimming, walking)")
            activity_modifications.append("Gradually increase intensity as fitness improves")
        
        # Sleep recommendations
        sleep_recommendations = [
            "Aim for 7-9 hours of quality sleep nightly",
            "Maintain consistent sleep and wake times",
            "Create a cool, dark, quiet sleeping environment",
            "Avoid screens 1 hour before bedtime"
        ]
        
        # Stress management
        stress_management = [
            "Practice deep breathing exercises (10 minutes daily)",
            "Consider meditation or mindfulness apps",
            "Engage in regular physical activity",
            "Maintain social connections and hobbies"
        ]
        
        # Add condition-specific stress management
        if patient.vitals.systolic_bp and patient.vitals.systolic_bp >= 130:
            stress_management.append("Practice stress-reduction techniques as stress can elevate blood pressure")
        
        return LifestyleRecommendation(
            exercise_type=exercise_guidelines['aerobic'],
            exercise_frequency="Most days of the week",
            exercise_duration="30-60 minutes",
            exercise_intensity=fitness_level.title(),
            sleep_recommendations=sleep_recommendations,
            stress_management=stress_management,
            activity_modifications=activity_modifications
        )
    
    def _generate_supplement_recommendations(self, patient: Patient, 
                                           cluster_profile: ClusterProfile) -> SupplementRecommendation:
        """Generate personalized supplement recommendations"""
        
        recommended_supplements = []
        contraindications = []
        interaction_warnings = []
        monitoring_suggestions = []
        
        # General wellness supplements
        recommended_supplements.extend(self.config.SUPPLEMENT_DATABASE['general_wellness'])
        
        # Condition-specific supplements
        conditions = [c.lower() for c in patient.medical_history.conditions]
        
        # Diabetes prevention/management
        if (patient.lab_results.hba1c and patient.lab_results.hba1c >= 5.7) or \
           any('diabetes' in c for c in conditions):
            recommended_supplements.extend(self.config.SUPPLEMENT_DATABASE['diabetes_prevention'])
            monitoring_suggestions.append("Monitor blood glucose levels when starting new supplements")
        
        # Cardiovascular health
        if (patient.vitals.systolic_bp and patient.vitals.systolic_bp >= 130) or \
           (patient.lab_results.total_cholesterol and patient.lab_results.total_cholesterol >= 200):
            recommended_supplements.extend(self.config.SUPPLEMENT_DATABASE['cardiovascular_health'])
            monitoring_suggestions.append("Monitor blood pressure regularly")
        
        # Add contraindications based on medications
        medications = [m.lower() for m in patient.medical_history.medications]
        
        if any('warfarin' in m or 'blood thinner' in m for m in medications):
            contraindications.append("Avoid high-dose omega-3 supplements without medical supervision")
            interaction_warnings.append("Omega-3 supplements may increase bleeding risk with blood thinners")
        
        if any('diabetes medication' in m or 'metformin' in m for m in medications):
            interaction_warnings.append("Monitor blood glucose when adding chromium or cinnamon supplements")
        
        return SupplementRecommendation(
            recommended_supplements=recommended_supplements,
            contraindications=contraindications,
            interaction_warnings=interaction_warnings,
            monitoring_suggestions=monitoring_suggestions
        )
    
    def _generate_safety_alerts(self, patient: Patient, 
                               cluster_profile: ClusterProfile) -> SafetyAlert:
        """Generate safety alerts and medical referral recommendations"""
        
        risk_level = RiskLevel.LOW
        warning_signs = []
        immediate_actions = []
        follow_up_timeline = "Annual routine check-up"
        specialist_referrals = []
        
        # Assess risk level based on vitals and lab results
        risk_factors = 0
        
        # Blood pressure assessment
        if patient.vitals.systolic_bp:
            if patient.vitals.systolic_bp >= 180:
                risk_level = RiskLevel.CRITICAL
                warning_signs.extend(self.config.WARNING_SIGNS['immediate_attention'])
                immediate_actions.append("Seek immediate medical attention for blood pressure crisis")
            elif patient.vitals.systolic_bp >= 140:
                risk_factors += 2
                specialist_referrals.append("Cardiologist for hypertension management")
            elif patient.vitals.systolic_bp >= 130:
                risk_factors += 1
        
        # Glucose assessment
        if patient.lab_results.fasting_glucose:
            if patient.lab_results.fasting_glucose >= 400:
                risk_level = RiskLevel.CRITICAL
                immediate_actions.append("Seek immediate medical attention for severe hyperglycemia")
            elif patient.lab_results.fasting_glucose >= 126:
                risk_factors += 2
                specialist_referrals.append("Endocrinologist for diabetes management")
            elif patient.lab_results.fasting_glucose >= 100:
                risk_factors += 1
        
        # HbA1c assessment
        if patient.lab_results.hba1c:
            if patient.lab_results.hba1c >= 6.5:
                risk_factors += 2
                if "Endocrinologist for diabetes management" not in specialist_referrals:
                    specialist_referrals.append("Endocrinologist for diabetes management")
            elif patient.lab_results.hba1c >= 5.7:
                risk_factors += 1
        
        # BMI assessment
        if patient.vitals.bmi:
            if patient.vitals.bmi >= 35:
                risk_factors += 2
                specialist_referrals.append("Registered dietitian for weight management")
            elif patient.vitals.bmi >= 30:
                risk_factors += 1
        
        # Determine overall risk level
        if risk_level != RiskLevel.CRITICAL:
            if risk_factors >= 4:
                risk_level = RiskLevel.HIGH
                follow_up_timeline = "Within 1-2 months"
            elif risk_factors >= 2:
                risk_level = RiskLevel.MODERATE
                follow_up_timeline = "Within 3-6 months"
        
        # Add general warning signs
        if risk_level in [RiskLevel.MODERATE, RiskLevel.HIGH]:
            warning_signs.extend(self.config.WARNING_SIGNS['urgent_consultation'])
        
        return SafetyAlert(
            risk_level=risk_level,
            warning_signs=warning_signs,
            immediate_actions=immediate_actions,
            follow_up_timeline=follow_up_timeline,
            specialist_referrals=specialist_referrals
        )
