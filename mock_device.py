import requests
import random
import time

url = 'http://127.0.0.1:8000/device-data/'

# while True:
data = {
    'patient_id': 1,
    'heart_rate': random.randint(60, 100),
    'blood_pressure': f"{random.randint(110, 130)}/{random.randint(70, 90)}"
}
response = requests.post(url, json=data)
print(f"Sent data: {data}, Response: {response.status_code}")
    # time.sleep(5)  # Send data every 5 seconds