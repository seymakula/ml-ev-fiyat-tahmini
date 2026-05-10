import pandas as pd
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

# Veri setini yükle
print("Veri seti yükleniyor...")
housing = fetch_california_housing()
df = pd.DataFrame(housing.data, columns=housing.feature_names)
df['Price'] = housing.target * 100000  # Dolar cinsinden

print(f"Veri seti boyutu: {df.shape}")
print(f"\nÖrnek veriler:\n{df.head()}")
print(f"\nİstatistikler:\n{df.describe()}")

# Özellikler ve hedef değişken
X = df[housing.feature_names]
y = df['Price']

# Eğitim ve test verisi
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Ölçeklendirme
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Model eğitimi
print("\nModel eğitiliyor...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Test
y_pred = model.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\nModel Performansı:")
print(f"R² Skoru: {r2:.4f}")
print(f"RMSE: {np.sqrt(mse):.2f} dolar")

# Modeli kaydet
os.makedirs('model', exist_ok=True)
joblib.dump(model, 'model/model.pkl')
joblib.dump(scaler, 'model/scaler.pkl')
joblib.dump(housing.feature_names, 'model/features.pkl')
print("\nModel kaydedildi: model/model.pkl")
