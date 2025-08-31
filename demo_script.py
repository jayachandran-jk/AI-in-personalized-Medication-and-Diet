#!/usr/bin/env python3
"""
Quick demo script for the AI-Powered Personalized Healthcare Assistant
"""

import sys
from healthcare_assistant import PersonalizedHealthcareAssistant
from sample_data import create_sample_patients, get_test_patient
from config import get_config

def main():
    print("🏥 AI-Powered Personalized Healthcare Assistant - Quick Demo")
    print("=" * 60)
    
    try:
        # Initialize configuration and assistant
        print("📊 Initializing AI Healthcare Assistant...")
        config = get_config()
        assistant = PersonalizedHealthcareAssistant(config)
        
        # Create sample patients for training
        print("📋 Creating sample patient data...")
        training_patients = create_sample_patients()
        print(f"✅ Created {len(training_patients)} sample patients")
        
        # Train the ML model
        print("🤖 Training machine learning model...")
        training_results = assistant.train_model(training_patients)
        print(f"✅ Model trained successfully!")
        print(f"   - Silhouette Score: {training_results['silhouette_score']:.3f}")
        print(f"   - Number of Clusters: {config.ML_CONFIG['n_clusters']}")
        print(f"   - Training Samples: {training_results['n_samples']}")
        
        # Demonstrate with test patient
        print("\n👤 Analyzing test patient...")
        test_patient = get_test_patient()
        print(f"   Patient: {test_patient.name}, Age: {test_patient.age}")
        print(f"   Conditions: {', '.join(test_patient.medical_history.conditions) or 'None'}")
        
        # Generate wellness plan
        print("🧠 Generating personalized wellness plan...")
        wellness_plan = assistant.generate_wellness_plan(test_patient)
        
        # Display key results
        print("\n📋 KEY RESULTS")
        print("=" * 40)
        print(f"Patient: {wellness_plan.patient.name}")
        print(f"Cluster: {wellness_plan.cluster_profile.cluster_name}")
        print(f"Similarity: {wellness_plan.cluster_profile.similarity_score:.1%}")
        print(f"Risk Level: {wellness_plan.safety_alerts.risk_level.value.upper()}")
        
        print(f"\nTop Nutrition Recommendations:")
        for i, food in enumerate(wellness_plan.nutrition.foods_to_emphasize[:3], 1):
            print(f"  {i}. {food}")
        
        print(f"\nExercise Recommendation:")
        print(f"  {wellness_plan.lifestyle.exercise_type}")
        
        print(f"\nFollow-up Timeline:")
        print(f"  {wellness_plan.safety_alerts.follow_up_timeline}")
        
        # Save detailed report
        output_file = "demo_wellness_plan.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(wellness_plan.to_formatted_report())
        print(f"\n💾 Full wellness plan saved to: {output_file}")
        
        print("\n✅ Demo completed successfully!")
        print("\nNext steps:")
        print("  • Run 'python main.py' for interactive mode")
        print("  • Run 'python app.py' for web interface")
        print("  • Run 'python test_healthcare_assistant.py' for tests")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Please install required dependencies: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
