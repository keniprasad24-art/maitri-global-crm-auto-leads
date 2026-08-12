import requests
import json

# तुमची लिंक (सर्व्हर चालू असायला हवा)
url = "http://127.0.0.1:8000/leads/api/capture/"

data = {
    "name": "Rajesh Automation Test",
    "email": "rajesh_test@example.com",
    "phone": "9988776655",
    "company": "Automation IT",
    "source": "Facebook Ads"
}

try:
    # डेटा पाठवणे
    response = requests.post(url, json=data)
    print("निकाल (Result):", response.json())
except Exception as e:
    print("काहीतरी चूक झाली (Error):", e)