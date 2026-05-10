from flask import Flask, request, render_template_string
import json
import boto3

app = Flask(__name__)
lambda_client = boto3.client('lambda', region_name='eu-central-1')

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Ev Fiyat Tahmini</title>
    <style>
        body { font-family: Arial; background: #1a1a2e; color: white; padding: 40px; }
        h1 { color: #00d4ff; text-align: center; }
        .form-container { max-width: 600px; margin: 0 auto; background: #16213e; padding: 30px; border-radius: 10px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; color: #00d4ff; }
        input { width: 100%; padding: 8px; border-radius: 5px; border: 1px solid #00d4ff; background: #1a1a2e; color: white; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #00d4ff; color: black; border: none; border-radius: 5px; font-size: 16px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        button:hover { background: #0099bb; }
        .result { text-align: center; margin-top: 20px; padding: 20px; background: #0f3460; border-radius: 10px; }
        .price { font-size: 36px; font-weight: bold; color: #00d4ff; }
        .error { color: #ff6b6b; }
    </style>
</head>
<body>
    <h1>🏠 Ev Fiyat Tahmini</h1>
    <div class="form-container">
        <form method="POST">
            <div class="form-group">
                <label>Ortalama Gelir (MedInc)</label>
                <input type="number" step="0.01" name="MedInc" value="5.0" required>
            </div>
            <div class="form-group">
                <label>Evin Yaşı (HouseAge)</label>
                <input type="number" step="0.1" name="HouseAge" value="20.0" required>
            </div>
            <div class="form-group">
                <label>Ortalama Oda Sayısı (AveRooms)</label>
                <input type="number" step="0.01" name="AveRooms" value="6.0" required>
            </div>
            <div class="form-group">
                <label>Ortalama Yatak Odası (AveBedrms)</label>
                <input type="number" step="0.01" name="AveBedrms" value="1.0" required>
            </div>
            <div class="form-group">
                <label>Nüfus (Population)</label>
                <input type="number" step="1" name="Population" value="1000.0" required>
            </div>
            <div class="form-group">
                <label>Ortalama Kişi Sayısı (AveOccup)</label>
                <input type="number" step="0.01" name="AveOccup" value="3.0" required>
            </div>
            <div class="form-group">
                <label>Enlem (Latitude)</label>
                <input type="number" step="0.01" name="Latitude" value="37.0" required>
            </div>
            <div class="form-group">
                <label>Boylam (Longitude)</label>
                <input type="number" step="0.01" name="Longitude" value="-120.0" required>
            </div>
            <button type="submit">Fiyat Tahmin Et</button>
        </form>
        {% if price %}
        <div class="result">
            <p>Tahmini Ev Fiyatı</p>
            <div class="price">${{ "{:,.0f}".format(price) }}</div>
        </div>
        {% endif %}
        {% if error %}
        <div class="result">
            <p class="error">Hata: {{ error }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    price = None
    error = None
    if request.method == 'POST':
        try:
            data = {k: float(v) for k, v in request.form.items()}
            response = lambda_client.invoke(
                FunctionName='ev-fiyat-tahmini',
                InvocationType='RequestResponse',
                Payload=json.dumps({'body': json.dumps(data)})
            )
            result = json.loads(response['Payload'].read())
            body = json.loads(result['body'])
            price = body['predicted_price']
        except Exception as e:
            error = str(e)
    return render_template_string(HTML, price=price, error=error)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
