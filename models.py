"""
Data models for the AI-Powered Personalized Healthcare Assistant
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class RiskLevel(Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class VitalSigns:
    """Patient vital signs data"""
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None
    heart_rate: Optional[int] = None
    temperature: Optional[float] = None
    respiratory_rate: Optional[int] = None
    oxygen_saturation: Optional[float] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    
    @property
    def bmi(self) -> Optional[float]:
        """Calculate BMI if height and weight are available"""
        if self.height and self.weight and self.height > 0:
            height_m = self.height / 100  # Convert cm to meters
            return round(self.weight / (height_m ** 2), 1)
        return None

@dataclass
class LabResults:
    """Laboratory test results"""
    fasting_glucose: Optional[float] = None
    hba1c: Optional[float] = None
    total_cholesterol: Optional[float] = None
    ldl_cholesterol: Optional[float] = None
    hdl_cholesterol: Optional[float] = None
    triglycerides: Optional[float] = None
    creatinine: Optional[float] = None
    bun: Optional[float] = None
    test_date: Optional[datetime] = None

@dataclass
class MedicalHistory:
    """Patient medical history"""
    conditions: List[str] = field(default_factory=list)
    medications: List[str] = field(default_factory=list)
    allergies: List[str] = field(default_factory=list)
    family_history: List[str] = field(default_factory=list)
    surgeries: List[str] = field(default_factory=list)
    lifestyle_factors: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Patient:
    """Complete patient profile"""
    patient_id: str
    name: str
    age: int
    gender: Gender
    vitals: VitalSigns
    lab_results: LabResults
    medical_history: MedicalHistory
    symptoms: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert patient data to dictionary for ML processing"""
        return {
            'patient_id': self.patient_id,
            'age': self.age,
            'gender': self.gender.value,
            'bmi': self.vitals.bmi or 0,
            'systolic_bp': self.vitals.systolic_bp or 0,
            'diastolic_bp': self.vitals.diastolic_bp or 0,
            'heart_rate': self.vitals.heart_rate or 0,
            'fasting_glucose': self.lab_results.fasting_glucose or 0,
            'hba1c': self.lab_results.hba1c or 0,
            'total_cholesterol': self.lab_results.total_cholesterol or 0,
            'ldl_cholesterol': self.lab_results.ldl_cholesterol or 0,
            'hdl_cholesterol': self.lab_results.hdl_cholesterol or 0,
            'triglycerides': self.lab_results.triglycerides or 0,
            'num_conditions': len(self.medical_history.conditions),
            'num_medications': len(self.medical_history.medications),
            'family_diabetes': 'diabetes' in ' '.join(self.medical_history.family_history).lower(),
            'family_heart_disease': 'heart' in ' '.join(self.medical_history.family_history).lower(),
        }

@dataclass
class ClusterProfile:
    """ML cluster analysis results"""
    cluster_id: int
    cluster_name: str
    characteristics: List[str]
    typical_conditions: List[str]
    risk_factors: List[str]
    similarity_score: float
    confidence_level: float

@dataclass
class PCAFeatures:
    """Principal Component Analysis results"""
    component_1: float  # Primary health pattern
    component_2: float  # Secondary health pattern
    component_3: float  # Tertiary health pattern
    explained_variance: List[float]
    feature_importance: Dict[str, float]

@dataclass
class NutritionRecommendation:
    """Nutritional guidance"""
    foods_to_emphasize: List[str]
    foods_to_avoid: List[str]
    meal_planning_tips: List[str]
    hydration_guidelines: str
    special_considerations: List[str]

@dataclass
class LifestyleRecommendation:
    """Lifestyle and exercise guidance"""
    exercise_type: str
    exercise_frequency: str
    exercise_duration: str
    exercise_intensity: str
    sleep_recommendations: List[str]
    stress_management: List[str]
    activity_modifications: List[str]

@dataclass
class SupplementRecommendation:
    """Supplement and wellness guidance"""
    recommended_supplements: List[Dict[str, str]]
    contraindications: List[str]
    interaction_warnings: List[str]
    monitoring_suggestions: List[str]

@dataclass
class SafetyAlert:
    """Safety warnings and medical referrals"""
    risk_level: RiskLevel
    warning_signs: List[str]
    immediate_actions: List[str]
    follow_up_timeline: str
    specialist_referrals: List[str]

@dataclass
class WellnessPlan:
    """Complete personalized wellness plan"""
    patient: Patient
    cluster_profile: ClusterProfile
    pca_features: PCAFeatures
    nutrition: NutritionRecommendation
    lifestyle: LifestyleRecommendation
    supplements: SupplementRecommendation
    safety_alerts: SafetyAlert
    generated_at: datetime = field(default_factory=datetime.now)
    
    def to_formatted_report(self) -> str:
        """Generate formatted wellness plan report"""
        report = f"""
**Personalized Wellness Plan for {self.patient.name} (ID: {self.patient.patient_id})**

**Cluster Analysis Summary:**
- Cluster ID: {self.cluster_profile.cluster_id} ({self.cluster_profile.cluster_name})
- Similarity Score: {self.cluster_profile.similarity_score:.2%}
- Confidence Level: {self.cluster_profile.confidence_level:.2%}
- Key Characteristics: {', '.join(self.cluster_profile.characteristics)}

**Current Health Assessment:**
- Age: {self.patient.age}, Gender: {self.patient.gender.value.title()}
- BMI: {self.patient.vitals.bmi or 'N/A'}
- Blood Pressure: {self.patient.vitals.systolic_bp or 'N/A'}/{self.patient.vitals.diastolic_bp or 'N/A'} mmHg
- HbA1c: {self.patient.lab_results.hba1c or 'N/A'}%
- Primary Conditions: {', '.join(self.patient.medical_history.conditions) or 'None reported'}

**Nutritional Recommendations:**
Foods to Emphasize:
{chr(10).join(f'- {food}' for food in self.nutrition.foods_to_emphasize)}

Foods to Limit/Avoid:
{chr(10).join(f'- {food}' for food in self.nutrition.foods_to_avoid)}

Meal Planning: {', '.join(self.nutrition.meal_planning_tips)}
Hydration: {self.nutrition.hydration_guidelines}

**Lifestyle & Activity Guidelines:**
- Exercise: {self.lifestyle.exercise_type}, {self.lifestyle.exercise_frequency}
- Duration: {self.lifestyle.exercise_duration}
- Intensity: {self.lifestyle.exercise_intensity}
- Sleep: {', '.join(self.lifestyle.sleep_recommendations)}
- Stress Management: {', '.join(self.lifestyle.stress_management)}

**Supplement Considerations:**
Recommended Supplements:
{chr(10).join(f"- {supp['name']}: {supp['dosage']} ({supp['timing']})" for supp in self.supplements.recommended_supplements)}

Contraindications: {', '.join(self.supplements.contraindications) or 'None identified'}

**Important Safety Notes:**
- Risk Level: {self.safety_alerts.risk_level.value.title()}
- Warning Signs: {', '.join(self.safety_alerts.warning_signs)}
- Follow-up: {self.safety_alerts.follow_up_timeline}
- Specialist Referrals: {', '.join(self.safety_alerts.specialist_referrals) or 'None at this time'}

**Disclaimer:** This guidance is for informational purposes only and does not replace professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers for medical decisions.

Generated on: {self.generated_at.strftime('%Y-%m-%d %H:%M:%S')}
        """
        return report.strip()
