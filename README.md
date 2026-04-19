# 🚗 Vehicle Damage Detection System

An AI-powered system that detects vehicle damage using **Computer Vision (CV)** and **Natural Language Processing (NLP)** models deployed on AWS SageMaker.

## ✨ Features

- 🎯 **Damage Detection** - Identifies vehicle damage from images using deep learning
- 📊 **Severity Assessment** - Classifies damage as Minor, Moderate, or Severe  
- 🏷️ **Damage Classification** - Detects specific damage types (dent, scratch, crack, etc.)
- 📝 **NLP Report Generation** - Generates automated damage assessment reports
- ☁️ **AWS Integration** - Lambda functions + S3 storage + DynamoDB database
- 🌐 **REST API** - Flask frontend for easy access

## 📁 Project Structure
vehicle-damage-project/
├── frontend/
│   └── app.py                    # Flask web application
├── lambda/
│   └── lambda_function.py        # AWS Lambda handler
├── vehicle-damage-main.ipynb     # CV + NLP model training
├── vehicle-damage-NLP.ipynb      # NLP-specific experiments
└── README.md

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Computer Vision** | TensorFlow, OpenCV, AWS Rekognition |
| **NLP** | NLTK, spaCy, TextBlob |
| **Backend** | AWS Lambda, S3, DynamoDB |
| **Frontend** | Flask, HTML/CSS |
| **Deployment** | AWS SageMaker |

## 📊 Model Output Example
STATUS: DAMAGED
CONFIDENCE: 94.0%
SEVERITY: Medium
DAMAGE: Car Dent
ASSESSMENT: MODERATE damage on body panels
ACTION: Schedule repair within 1 week


## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- AWS Account (SageMaker, Lambda, S3, DynamoDB)
- Jupyter Notebook

### Installation

```bash
git clone https://github.com/22krishnaG/vehicle-damage-project.git
cd vehicle-damage-project
pip install -r requirements.txt
```

### Usage

1. **Train Models** - Run `vehicle-damage-main.ipynb`
2. **Deploy Lambda** - Upload `lambda/lambda_function.py` to AWS
3. **Start Frontend** - Run `python frontend/app.py`

## 📈 Performance Metrics

| Metric | Score |
|--------|-------|
| Detection Accuracy | 94%+ |
| Damage Types | 5 classes |
| Processing Time | <2 seconds/image |

## 👤 Author

**Krishna Goyal** - [GitHub](https://github.com/22krishnaG)
University of Limerick - Cloud Computing

## 📝 License

MIT License
