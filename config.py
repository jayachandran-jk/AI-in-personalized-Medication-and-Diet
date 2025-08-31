"""
Configuration settings for the AI-Powered Personalized Healthcare Assistant
"""

import os
from typing import Dict, Any

class Config:
    """Main configuration class for the healthcare assistant"""
    
    # Application Settings
    APP_NAME = "AI-Powered Personalized Healthcare Assistant"
    VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Machine Learning Settings
    ML_CONFIG = {
        "n_clusters": 5,  # Number of clusters for K-Means
        "pca_components": 3,  # Number of PCA components
        "random_state": 42,  # For reproducible results
        "cluster_confidence_threshold": 0.7,  # Minimum confidence for cluster assignment
    }
    
    # Health Risk Thresholds
    HEALTH_THRESHOLDS = {
        "blood_pressure": {
            "normal": {"systolic": (90, 120), "diastolic": (60, 80)},
            "elevated": {"systolic": (120, 129), "diastolic": (60, 80)},
            "stage1": {"systolic": (130, 139), "diastolic": (80, 89)},
            "stage2": {"systolic": (140, 180), "diastolic": (90, 120)},
            "crisis": {"systolic": (180, float('inf')), "diastolic": (120, float('inf'))}
        },
        "glucose": {
            "normal": (70, 99),
            "prediabetic": (100, 125),
            "diabetic": (126, float('inf'))
        },
        "hba1c": {
            "normal": (0, 5.6),
            "prediabetic": (5.7, 6.4),
            "diabetic": (6.5, float('inf'))
        },
        "bmi": {
            "underweight": (0, 18.5),
            "normal": (18.5, 24.9),
            "overweight": (25, 29.9),
            "obese": (30, float('inf'))
        },
        "cholesterol": {
            "total": {"desirable": (0, 200), "borderline": (200, 239), "high": (240, float('inf'))},
            "ldl": {"optimal": (0, 100), "near_optimal": (100, 129), "borderline": (130, 159), "high": (160, 189), "very_high": (190, float('inf'))},
            "hdl": {"low": (0, 40), "normal": (40, 60), "high": (60, float('inf'))}
        }
    }
    
    # Indian Dietary Recommendations Database
    NUTRITION_DATABASE = {
        "diabetes_risk": {
            "recommended": [
                "bitter gourd", "fenugreek leaves", "spinach",
                "okra", "bottle gourd", "ridge gourd",
                "moong dal", "chana dal", "masoor dal", "brown rice",
                "pearl millet", "sorghum", "finger millet",
                "Indian gooseberry", "black plum", "neem leaves",
                "turmeric", "cinnamon", "cumin", "carom seeds"
            ],
            "avoid": [
                "white rice", "refined flour", "jaggery in excess",
                "sweets and mithai", "fried snacks", "samosa", "pakora",
                "sugary lassi", "mango in excess", "ripe banana", "potato"
            ]
        },
        "cardiovascular_risk": {
            "recommended": [
                "arjuna bark tea", "garlic", "ginger", "turmeric",
                "flaxseeds", "walnuts", "almonds", "fish",
                "mustard oil in moderation", "coconut water", "green tea",
                "pomegranate", "grapes", "oats", "barley", "moong dal"
            ],
            "avoid": [
                "ghee in excess", "coconut oil in excess", "fried foods",
                "red meat", "organ meats", "egg yolk", "full-fat dairy",
                "salty snacks", "pickles", "papad", "processed foods"
            ]
        },
        "hypertension": {
            "recommended": [
                "bottle gourd", "cucumber", "watermelon", "coconut water",
                "banana", "pomegranate", "garlic", "ginger", "holy basil",
                "coriander seeds water", "fennel seeds", "cardamom",
                "low-salt dal", "steamed vegetables", "buttermilk"
            ],
            "avoid": [
                "excess salt", "pickles", "papad", "salty snacks",
                "processed foods", "canned foods", "soy sauce",
                "cheese", "salted nuts", "fried foods", "alcohol"
            ]
        },
        "general_wellness": {
            "recommended": [
                "seasonal fruits", "green leafy vegetables", "whole grains",
                "dal (lentils)", "curd", "buttermilk", "coconut water",
                "ginger-lemon tea", "turmeric milk", "tulsi tea",
                "almonds", "walnuts", "dates", "figs"
            ],
            "avoid": [
                "excessive oil", "deep fried foods", "processed snacks",
                "aerated drinks", "excessive sugar", "refined flour products"
            ]
        }
    }
    
    # Exercise Recommendations
    EXERCISE_GUIDELINES = {
        "beginner": {
            "aerobic": "20-30 minutes, 3-4 times per week, low to moderate intensity",
            "strength": "2 times per week, bodyweight exercises",
            "flexibility": "10-15 minutes daily stretching"
        },
        "intermediate": {
            "aerobic": "30-45 minutes, 4-5 times per week, moderate intensity",
            "strength": "2-3 times per week, resistance training",
            "flexibility": "15-20 minutes daily stretching and mobility"
        },
        "advanced": {
            "aerobic": "45-60 minutes, 5-6 times per week, moderate to high intensity",
            "strength": "3-4 times per week, progressive resistance training",
            "flexibility": "20-30 minutes daily comprehensive mobility work"
        }
    }
    
    # Supplement Guidelines (English Medicine/Allopathic)
    SUPPLEMENT_DATABASE = {
        "diabetes_prevention": [
            {"name": "Chromium Picolinate", "dosage": "200-400 mcg daily", "timing": "with meals"},
            {"name": "Alpha-Lipoic Acid", "dosage": "300-600 mg daily", "timing": "before meals"},
            {"name": "Cinnamon Extract", "dosage": "500-1000 mg daily", "timing": "with meals"},
            {"name": "Bitter Melon Extract", "dosage": "500-1000 mg daily", "timing": "before meals"},
            {"name": "Fenugreek Extract", "dosage": "500 mg twice daily", "timing": "before meals"}
        ],
        "cardiovascular_health": [
            {"name": "Omega-3 Fatty Acids", "dosage": "1000-2000 mg daily", "timing": "with meals"},
            {"name": "Coenzyme Q10", "dosage": "100-200 mg daily", "timing": "with fat-containing meal"},
            {"name": "Magnesium", "dosage": "200-400 mg daily", "timing": "before bedtime"},
            {"name": "Arjuna Extract", "dosage": "500 mg twice daily", "timing": "after meals"},
            {"name": "Garlic Extract", "dosage": "600-900 mg daily", "timing": "with meals"}
        ],
        "hypertension": [
            {"name": "Magnesium", "dosage": "200-400 mg daily", "timing": "before bedtime"},
            {"name": "Potassium", "dosage": "99 mg daily", "timing": "with meals"},
            {"name": "Hawthorn Extract", "dosage": "300-600 mg daily", "timing": "with meals"},
            {"name": "Garlic Extract", "dosage": "600-900 mg daily", "timing": "with meals"}
        ],
        "general_wellness": [
            {"name": "Vitamin D3", "dosage": "1000-2000 IU daily", "timing": "with meals"},
            {"name": "Multivitamin", "dosage": "as directed", "timing": "with breakfast"},
            {"name": "Probiotics", "dosage": "10-50 billion CFU daily", "timing": "on empty stomach"},
            {"name": "Vitamin B12", "dosage": "1000 mcg daily", "timing": "with breakfast"},
            {"name": "Iron (if deficient)", "dosage": "18-27 mg daily", "timing": "on empty stomach"}
        ]
    }
    
    # Warning Signs for Medical Attention
    WARNING_SIGNS = {
        "immediate_attention": [
            "Chest pain or pressure",
            "Difficulty breathing",
            "Severe headache",
            "Blood pressure >180/110",
            "Blood glucose <70 or >400",
            "Loss of consciousness",
            "Severe allergic reaction"
        ],
        "urgent_consultation": [
            "Persistent fatigue",
            "Unexplained weight loss/gain",
            "Frequent urination and excessive thirst",
            "Blurred vision",
            "Slow-healing wounds",
            "Numbness or tingling in extremities"
        ]
    }

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False

# Configuration factory
def get_config():
    """Get configuration based on environment"""
    env = os.getenv("FLASK_ENV", "development")
    if env == "production":
        return ProductionConfig()
    return DevelopmentConfig()
