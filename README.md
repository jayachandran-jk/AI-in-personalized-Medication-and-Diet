# 🏥 AI-Powered Personalized Healthcare Assistant

An intelligent healthcare assistant that provides personalized wellness recommendations using machine learning analysis of patient health data.

## 🌟 Features

- **Pharmacy Interface**: Quick patient lookup by ID or name for pharmacists
- **Patient Database**: SQLite database storing complete patient profiles
- **Machine Learning Analysis**: K-Means clustering and PCA to identify patient similarity groups
- **Personalized Recommendations**: Tailored nutrition, lifestyle, and supplement guidance
- **Risk Assessment**: Automated health risk evaluation with safety alerts
- **Web Interface**: User-friendly web application for easy interaction
- **Comprehensive Reporting**: Detailed wellness plans with medical disclaimers

## 🧠 Machine Learning Components

### K-Means Clustering

- Groups patients into 5 distinct health clusters
- Identifies similar patient patterns and risk profiles
- Calculates similarity scores and confidence levels

### Principal Component Analysis (PCA)

- Reduces dimensionality of health features
- Identifies key health condition patterns
- Provides feature importance rankings

### Feature Engineering

- Processes 15+ health parameters including:
  - Vital signs (BP, heart rate, BMI)
  - Laboratory results (glucose, HbA1c, cholesterol)
  - Medical history and family history
  - Demographics and lifestyle factors

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**

   ```bash
   cd "asp new project"
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the command-line interface**

   ```bash
   python main.py
   ```

4. **Run the web application**
   ```bash
   python app.py
   ```
   Then open http://localhost:5000 in your browser

## 💊 Pharmacy Interface Usage

The pharmacy interface is designed for pharmacists to quickly access patient wellness recommendations:

1. **Access the Pharmacy Interface**: Click "Pharmacy" in the navigation or go to `/pharmacy`
2. **Patient Lookup**: Enter either:
   - Patient ID (e.g., `PT-2024-0002`)
   - Patient Name (e.g., `Sarah Johnson`)
3. **Select Patient**: Choose from search results to view patient details
4. **Generate Plan**: Click "Generate Plan" to get AI-powered wellness recommendations
5. **Review Results**: View personalized nutrition, lifestyle, and supplement guidance
6. **Print/Download**: Save the wellness plan for patient consultation

### Quick Access Examples:

- `PT-2024-0002` - Sarah Johnson (Pre-diabetic)
- `PT-2024-0003` - Robert Chen (High Risk)
- `PT-2024-0001` - Alex Johnson (Healthy)

## 📊 Usage Examples

### Command Line Interface

```python
from healthcare_assistant import PersonalizedHealthcareAssistant
from sample_data import get_test_patient

# Initialize assistant
assistant = PersonalizedHealthcareAssistant()

# Train with sample data
training_patients = create_sample_patients()
assistant.train_model(training_patients)

# Analyze a patient
patient = get_test_patient()
wellness_plan = assistant.generate_wellness_plan(patient)

# Display results
print(wellness_plan.to_formatted_report())
```

### Web Interface

1. Navigate to the **Analyze Patient** page
2. Fill in patient information (or use quick-fill examples)
3. Click **Generate Wellness Plan**
4. Review personalized recommendations
5. Download or print the report

## 🏗️ Project Structure

```
asp new project/
├── main.py                    # Command-line interface
├── app.py                     # Flask web application
├── healthcare_assistant.py    # Main AI assistant class
├── ml_engine.py              # Machine learning components
├── models.py                 # Data models and structures
├── config.py                 # Configuration settings
├── sample_data.py            # Sample patient data
├── test_healthcare_assistant.py  # Test suite
├── requirements.txt          # Python dependencies
├── templates/                # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── analyze.html
│   ├── results.html
│   ├── demo.html
│   └── error.html
└── README.md                 # This file
```

## 🔬 Technical Implementation

### Data Models

- **Patient**: Complete patient profile with vitals, labs, and history
- **ClusterProfile**: ML cluster analysis results
- **PCAFeatures**: Principal component analysis output
- **WellnessPlan**: Complete personalized recommendations

### Machine Learning Pipeline

1. **Data Preprocessing**: Feature extraction and normalization
2. **Clustering**: K-Means algorithm with silhouette score validation
3. **Dimensionality Reduction**: PCA for pattern identification
4. **Risk Assessment**: Multi-factor risk stratification
5. **Recommendation Generation**: Evidence-based wellness guidance

### Safety Features

- **Medical Disclaimers**: Clear warnings about AI limitations
- **Risk Alerts**: Automated identification of concerning patterns
- **Specialist Referrals**: Recommendations for professional consultation
- **Safety Thresholds**: Predefined limits for critical values

## 🧪 Testing

Run the test suite:

```bash
python test_healthcare_assistant.py
```

Or use pytest:

```bash
pytest test_healthcare_assistant.py -v
```

## 📋 Sample Patient Profiles

The system includes diverse sample patients:

1. **Healthy Adult** (John, 30M) - Normal vitals, low risk
2. **Pre-diabetic** (Sarah, 52F) - Elevated glucose, moderate risk
3. **High Risk** (Robert, 64M) - Multiple comorbidities, high risk
4. **Metabolic Syndrome** (Maria, 35F) - PCOS, insulin resistance
5. **Elderly Complex** (Eleanor, 78F) - Multiple conditions
6. **Athletic** (David, 24M) - Optimal health markers
7. **Cardiovascular Risk** (Jennifer, 48F) - Hypertension, hyperlipidemia
8. **Family History** (Michael, 32M) - Genetic risk factors

## ⚠️ Important Disclaimers

### Medical Disclaimer

This AI healthcare assistant is for **educational and informational purposes only**. It:

- ❌ Does NOT provide medical diagnoses
- ❌ Does NOT prescribe medications
- ❌ Does NOT replace professional medical care
- ✅ Provides wellness guidance based on general health principles
- ✅ Suggests when to consult healthcare professionals

### Limitations

- Recommendations are based on statistical patterns, not individual medical assessment
- AI analysis may not account for all health factors
- Always consult qualified healthcare providers for medical decisions
- Regular medical monitoring is essential for chronic conditions

## 🔧 Configuration

Key settings in `config.py`:

```python
ML_CONFIG = {
    "n_clusters": 5,           # Number of patient clusters
    "pca_components": 3,       # PCA dimensions
    "random_state": 42,        # Reproducible results
}

HEALTH_THRESHOLDS = {
    "blood_pressure": {...},   # BP risk categories
    "glucose": {...},          # Glucose ranges
    "bmi": {...},             # BMI categories
}
```

## 🚀 Future Enhancements

- [ ] Integration with electronic health records (EHR)
- [ ] Advanced deep learning models
- [ ] Real-time monitoring capabilities
- [ ] Mobile application development
- [ ] Multi-language support
- [ ] Clinical validation studies

## 📄 License

This project is for educational purposes only. Not intended for commercial use or actual medical practice.

## 🤝 Contributing

This is an educational project. For improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📞 Support

For questions about this educational project:

- Review the code documentation
- Check the test cases for usage examples
- Refer to the configuration settings

---

**Remember**: This is a demonstration project for learning about AI in healthcare. Always consult qualified healthcare professionals for actual medical advice and treatment decisions.
