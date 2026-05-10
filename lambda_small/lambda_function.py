import json
import boto3
import os
import tempfile
import pickle

s3 = boto3.client('s3')
BUCKET = 'ml-model-seymakula'

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        tmp = tempfile.gettempdir()
        
        for filename in ['model.pkl', 'scaler.pkl', 'features.pkl']:
            s3.download_file(BUCKET, f'model/{filename}', f'{tmp}/{filename}')
        
        with open(f'{tmp}/features.pkl', 'rb') as f:
            features = list(pickle.load(f))
        
        with open(f'{tmp}/scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        
        with open(f'{tmp}/model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        input_data = [[float(body[f]) for f in features]]
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
