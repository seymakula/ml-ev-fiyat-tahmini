# 🏠 House Price Prediction — AWS ML

**BLM3522 Cloud Computing Course | Project 3**  
**Şeyma Kula**

---

## 📌 About the Project

This project is a machine learning application that predicts California house prices using a Random Forest model trained with Scikit-learn. The model is deployed on AWS Lambda and accessible through a Flask web interface.

**Data flow:**
```
California Housing Dataset
        ↓
Python + Scikit-learn (Random Forest)
        ↓
Model files → AWS S3
        ↓
AWS Lambda (Prediction API)
        ↓
Flask Web Dashboard
```

---

## 🏗️ System Architecture

| Component | Technology | Description |
|---|---|---|
| Dataset | California Housing (Scikit-learn) | 20,640 samples, 8 features |
| ML Model | Random Forest Regressor | R² Score: 0.80 |
| Model Storage | AWS S3 | Stores .pkl model files |
| API | AWS Lambda (Python 3.13) | Serverless prediction endpoint |
| Web Interface | Python Flask | User-friendly prediction form |

---

## 📁 File Structure

```
ml-project/
│
├── train_model.py      # Model training script
├── app.py              # Flask web application
├── model/              # Trained model files (excluded from git)
│   ├── model.pkl
│   ├── scaler.pkl
│   └── features.pkl
└── README.md
```

---

## 📊 Model Details

| Property | Value |
|---|---|
| Algorithm | Random Forest Regressor |
| Dataset | California Housing |
| Training Samples | 16,512 |
| Test Samples | 4,128 |
| R² Score | 0.80 |
| RMSE | ~$50,610 |
| Features | MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude |

---

## ⚙️ Setup and Usage

### 1. Requirements

- Python 3.13+
- AWS account
- AWS CLI configured

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install scikit-learn pandas numpy joblib flask boto3
```

### 3. Train the model

```bash
python3 train_model.py
```

### 4. Upload model to S3

```bash
aws s3 cp model/model.pkl s3://ml-model-seymakula/model/model.pkl
aws s3 cp model/scaler.pkl s3://ml-model-seymakula/model/scaler.pkl
aws s3 cp model/features.pkl s3://ml-model-seymakula/model/features.pkl
```

### 5. Deploy Lambda function

- Runtime: Python 3.13
- Upload `lambda_function.py` via S3
- Attach `AmazonS3FullAccess` policy
- Set timeout: 3 minutes, Memory: 512 MB

### 6. Run the web app

```bash
python3 app.py
# Open in browser: http://127.0.0.1:5001
```

---

## ☁️ AWS Configuration

| Setting | Value |
|---|---|
| AWS Region | eu-central-1 (Frankfurt) |
| S3 Bucket | ml-model-seymakula |
| Lambda Function | ev-fiyat-tahmini |
| Lambda Runtime | Python 3.13 |
| Lambda Memory | 512 MB |
| Lambda Timeout | 3 minutes |

---

## 📈 Sample Prediction

**Input:**
```json
{
  "MedInc": 5.0,
  "HouseAge": 20.0,
  "AveRooms": 6.0,
  "AveBedrms": 1.0,
  "Population": 1000.0,
  "AveOccup": 3.0,
  "Latitude": 37.0,
  "Longitude": -120.0
}
```

**Output:**
```json
{
  "predicted_price": 141861.0,
  "currency": "USD"
}
```

---

## 🔒 Security Note

Model files and virtual environment are excluded from git via `.gitignore`. Never upload AWS credentials to public repositories.

---

## 📚 References

- [Scikit-learn Documentation](https://scikit-learn.org/)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [California Housing Dataset](https://scikit-learn.org/stable/datasets/real_world.html#california-housing-dataset)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Random Forest Regressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html)
