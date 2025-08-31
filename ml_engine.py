"""
Machine Learning Engine for Patient Clustering and Analysis
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from typing import Dict, List, Tuple, Any
import joblib
import os

from models import Patient, ClusterProfile, PCAFeatures
from config import Config

class HealthMLEngine:
    """Machine Learning engine for patient health analysis"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.scaler = StandardScaler()
        self.kmeans = None
        self.pca = None
        self.cluster_profiles = {}
        self.feature_names = []
        self.is_trained = False
        
    def prepare_features(self, patients: List[Patient]) -> pd.DataFrame:
        """Convert patient data to feature matrix for ML"""
        features = []
        
        for patient in patients:
            patient_features = patient.to_dict()
            features.append(patient_features)
        
        df = pd.DataFrame(features)
        
        # Select numerical features for ML
        numerical_features = [
            'age', 'bmi', 'systolic_bp', 'diastolic_bp', 'heart_rate',
            'fasting_glucose', 'hba1c', 'total_cholesterol', 'ldl_cholesterol',
            'hdl_cholesterol', 'triglycerides', 'num_conditions', 'num_medications'
        ]
        
        # Add binary features
        binary_features = ['family_diabetes', 'family_heart_disease']
        
        # Convert gender to numerical
        df['gender_male'] = (df['gender'] == 'male').astype(int)
        df['gender_female'] = (df['gender'] == 'female').astype(int)
        
        # Combine all features
        self.feature_names = numerical_features + binary_features + ['gender_male', 'gender_female']
        
        # Fill missing values with median/mode
        for feature in numerical_features:
            if feature in df.columns:
                df[feature] = df[feature].fillna(df[feature].median())
        
        for feature in binary_features:
            if feature in df.columns:
                df[feature] = df[feature].fillna(False).astype(int)
        
        return df[self.feature_names]
    
    def train_clustering_model(self, patients: List[Patient]) -> Dict[str, Any]:
        """Train K-Means clustering model on patient data"""
        # Prepare features
        feature_df = self.prepare_features(patients)
        
        # Scale features
        scaled_features = self.scaler.fit_transform(feature_df)
        
        # Train K-Means
        self.kmeans = KMeans(
            n_clusters=self.config.ML_CONFIG['n_clusters'],
            random_state=self.config.ML_CONFIG['random_state'],
            n_init=10
        )
        
        cluster_labels = self.kmeans.fit_predict(scaled_features)
        
        # Calculate silhouette score
        silhouette_avg = silhouette_score(scaled_features, cluster_labels)
        
        # Train PCA
        self.pca = PCA(
            n_components=self.config.ML_CONFIG['pca_components'],
            random_state=self.config.ML_CONFIG['random_state']
        )
        
        pca_features = self.pca.fit_transform(scaled_features)
        
        # Create cluster profiles
        self._create_cluster_profiles(feature_df, cluster_labels, patients)
        
        self.is_trained = True
        
        return {
            'silhouette_score': silhouette_avg,
            'cluster_centers': self.kmeans.cluster_centers_,
            'explained_variance_ratio': self.pca.explained_variance_ratio_,
            'n_samples': len(patients)
        }
    
    def _create_cluster_profiles(self, feature_df: pd.DataFrame, 
                                cluster_labels: np.ndarray, 
                                patients: List[Patient]):
        """Create detailed profiles for each cluster"""
        
        cluster_names = [
            "Healthy Baseline",
            "Cardiovascular Risk",
            "Metabolic Syndrome",
            "Diabetes Management",
            "Complex Comorbidities"
        ]
        
        for cluster_id in range(self.config.ML_CONFIG['n_clusters']):
            cluster_mask = cluster_labels == cluster_id
            cluster_patients = [p for i, p in enumerate(patients) if cluster_mask[i]]
            cluster_features = feature_df[cluster_mask]
            
            # Calculate cluster characteristics
            characteristics = []
            typical_conditions = []
            risk_factors = []
            
            # Analyze age distribution
            ages = [p.age for p in cluster_patients]
            avg_age = np.mean(ages)
            characteristics.append(f"Average age: {avg_age:.1f} years")
            
            # Analyze BMI
            bmis = [p.vitals.bmi for p in cluster_patients if p.vitals.bmi]
            if bmis:
                avg_bmi = np.mean(bmis)
                characteristics.append(f"Average BMI: {avg_bmi:.1f}")
                if avg_bmi >= 30:
                    risk_factors.append("Obesity")
                elif avg_bmi >= 25:
                    risk_factors.append("Overweight")
            
            # Analyze blood pressure
            bp_systolic = [p.vitals.systolic_bp for p in cluster_patients if p.vitals.systolic_bp]
            if bp_systolic:
                avg_systolic = np.mean(bp_systolic)
                characteristics.append(f"Average systolic BP: {avg_systolic:.0f} mmHg")
                if avg_systolic >= 140:
                    risk_factors.append("Hypertension")
                elif avg_systolic >= 130:
                    risk_factors.append("Elevated blood pressure")
            
            # Analyze glucose/diabetes markers
            glucose_levels = [p.lab_results.fasting_glucose for p in cluster_patients 
                            if p.lab_results.fasting_glucose]
            hba1c_levels = [p.lab_results.hba1c for p in cluster_patients 
                          if p.lab_results.hba1c]
            
            if glucose_levels:
                avg_glucose = np.mean(glucose_levels)
                characteristics.append(f"Average fasting glucose: {avg_glucose:.0f} mg/dL")
                if avg_glucose >= 126:
                    typical_conditions.append("Type 2 Diabetes")
                elif avg_glucose >= 100:
                    risk_factors.append("Pre-diabetes")
            
            if hba1c_levels:
                avg_hba1c = np.mean(hba1c_levels)
                characteristics.append(f"Average HbA1c: {avg_hba1c:.1f}%")
            
            # Analyze common conditions
            all_conditions = []
            for patient in cluster_patients:
                all_conditions.extend(patient.medical_history.conditions)
            
            condition_counts = {}
            for condition in all_conditions:
                condition_counts[condition] = condition_counts.get(condition, 0) + 1
            
            # Get most common conditions (appearing in >30% of cluster)
            cluster_size = len(cluster_patients)
            for condition, count in condition_counts.items():
                if count / cluster_size > 0.3:
                    typical_conditions.append(condition)
            
            # Store cluster profile
            self.cluster_profiles[cluster_id] = ClusterProfile(
                cluster_id=cluster_id,
                cluster_name=cluster_names[cluster_id] if cluster_id < len(cluster_names) 
                           else f"Cluster {cluster_id}",
                characteristics=characteristics,
                typical_conditions=typical_conditions,
                risk_factors=risk_factors,
                similarity_score=0.0,  # Will be calculated per patient
                confidence_level=0.0   # Will be calculated per patient
            )
    
    def analyze_patient(self, patient: Patient) -> Tuple[ClusterProfile, PCAFeatures]:
        """Analyze a single patient and assign to cluster"""
        if not self.is_trained:
            raise ValueError("Model must be trained before analyzing patients")
        
        # Prepare patient features
        patient_df = pd.DataFrame([patient.to_dict()])
        
        # Ensure all required features are present
        for feature in self.feature_names:
            if feature not in patient_df.columns:
                if feature in ['gender_male', 'gender_female']:
                    patient_df[feature] = 0
                elif feature in ['family_diabetes', 'family_heart_disease']:
                    patient_df[feature] = 0
                else:
                    patient_df[feature] = 0
        
        # Convert gender
        patient_df['gender_male'] = (patient_df['gender'] == 'male').astype(int)
        patient_df['gender_female'] = (patient_df['gender'] == 'female').astype(int)
        
        # Convert family history
        family_history_str = ' '.join(patient.medical_history.family_history).lower()
        patient_df['family_diabetes'] = int('diabetes' in family_history_str)
        patient_df['family_heart_disease'] = int('heart' in family_history_str)
        
        # Select and scale features
        feature_vector = patient_df[self.feature_names].fillna(0)
        scaled_features = self.scaler.transform(feature_vector)
        
        # Predict cluster
        cluster_id = self.kmeans.predict(scaled_features)[0]
        
        # Calculate similarity score (distance to cluster center)
        cluster_center = self.kmeans.cluster_centers_[cluster_id]
        distance = np.linalg.norm(scaled_features[0] - cluster_center)
        max_distance = np.max([np.linalg.norm(center - cluster_center) 
                              for center in self.kmeans.cluster_centers_])
        similarity_score = max(0, 1 - (distance / max_distance)) if max_distance > 0 else 1.0
        
        # Calculate PCA features
        pca_features = self.pca.transform(scaled_features)[0]
        
        # Get feature importance (PCA component loadings)
        feature_importance = {}
        for i, feature_name in enumerate(self.feature_names):
            importance = np.sum(np.abs(self.pca.components_[:, i]))
            feature_importance[feature_name] = importance
        
        # Create cluster profile for this patient
        cluster_profile = self.cluster_profiles[cluster_id]
        cluster_profile.similarity_score = similarity_score
        cluster_profile.confidence_level = similarity_score * 0.9  # Slightly lower than similarity
        
        # Create PCA features
        pca_result = PCAFeatures(
            component_1=pca_features[0],
            component_2=pca_features[1],
            component_3=pca_features[2] if len(pca_features) > 2 else 0.0,
            explained_variance=self.pca.explained_variance_ratio_.tolist(),
            feature_importance=feature_importance
        )
        
        return cluster_profile, pca_result
    
    def save_model(self, filepath: str):
        """Save trained model to disk"""
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
        
        model_data = {
            'scaler': self.scaler,
            'kmeans': self.kmeans,
            'pca': self.pca,
            'cluster_profiles': self.cluster_profiles,
            'feature_names': self.feature_names,
            'config': self.config
        }
        
        joblib.dump(model_data, filepath)
    
    def load_model(self, filepath: str):
        """Load trained model from disk"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        model_data = joblib.load(filepath)
        
        self.scaler = model_data['scaler']
        self.kmeans = model_data['kmeans']
        self.pca = model_data['pca']
        self.cluster_profiles = model_data['cluster_profiles']
        self.feature_names = model_data['feature_names']
        self.config = model_data.get('config', Config())
        self.is_trained = True
