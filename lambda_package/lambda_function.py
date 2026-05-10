import json
import boto3
import joblib
import numpy as np
import os
import tempfile

s3 = boto3.client('s3')
BUCKET = 'ml-model-seymakula'

def load_model():
    tmp = tempfile.gettempdir()
    for filename in ['model.pkl', 'scaler.pkl', 'features.pkl']:
        s3.download_file(BUCKET, f'model/{filename}', f'{tmp}/{filename}')
    model = joblib.load(f'{tmp}/model.pkl')
    scaler = joblib.load(f'{tmp}/scaler.pkl')
    features = joblib.load(f'{tmp}/features.pkl')
    return model, scaler, features

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        model, scaler, features = load_model()
        input_data = np.array([[body[f] for f in features]])
        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)[0]
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'predicted_price': round(float(prediction), 2),
                'currency': 'USD'
            })
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
