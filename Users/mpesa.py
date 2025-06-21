import requests
import base64
import datetime
from django.conf import settings
import json


# M-Pesa Client for handling STK Push transactions
class MpesaClient:
    def __init__(self):
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.shortcode = settings.MPESA_SHORTCODE
        self.passkey = settings.MPESA_PASSKEY
        self.callback_url = settings.MPESA_CALLBACK_URL
        if settings.MPESA_SANDBOX:
            self.base_url = "https://sandbox.safaricom.co.ke"
        else:
            self.base_url = "https://api.safaricom.co.ke"
        self.auth_url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        self.stk_push_url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
    
    # Get OAuth access token from M-Pesa API
    def get_auth_token(self):
        auth = base64.b64encode(f"{self.consumer_key}:{self.consumer_secret}".encode()).decode("utf-8")
        headers = {
            "Authorization": f"Basic {auth}"
        }
        try:
            response = requests.get(self.auth_url, headers=headers)
            response_data = response.json()
            return response_data.get('access_token')
        except Exception as e:
            return None
    
    # Generate encoded password using shortcode, passkey, and timestamp
    def generate_password(self):
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        password_str = f"{self.shortcode}{self.passkey}{timestamp}"
        password = base64.b64encode(password_str.encode()).decode('utf-8')
        return {
            "timestamp": timestamp,
            "password": password
        }
    
    # Initiate STK Push request
    def stk_push(self, phone_number, amount, account_reference, transaction_desc):
        token = self.get_auth_token()
        if not token:
            return {"status": "failed", "message": "Unable to generate auth token"}
        
        password_data = self.generate_password()
        
        # Ensure phone number is in the correct format (remove leading '+' if present)
        if phone_number.startswith('+'):
            phone_number = phone_number[1:]
        # Ensure phone number starts with '254' (Kenya code)
        if phone_number.startswith('0'):
            phone_number = '254' + phone_number[1:]
        elif not phone_number.startswith('254'):
            phone_number = '254' + phone_number
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password_data["password"],
            "Timestamp": password_data["timestamp"],
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.callback_url,
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc
        }
        
        try:
            response = requests.post(self.stk_push_url, json=payload, headers=headers)
            return response.json()
        except Exception as e:
            return {"status": "failed", "message": str(e)}