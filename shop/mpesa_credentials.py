import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64

class MpesaC2bCredential:
    consumer_key = 'JljpJPedfeDQswq8iEp8KiezAyyXuA0Q'
    consumer_secret = 'Cet2aYSMsfEdQEum'
    api_URL = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

# class MpesaAccessToken:
#     r = requests.get(MpesaC2bCredential.api_URL,
#                      auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret))
#     print("WORKING TO HERE ------------------>")
#     print(r.content)
#     mpesa_access_token = json.loads(r.text)
#     validated_mpesa_access_token = mpesa_access_token['access_token']

class LipanaMpesaPpassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = "174379"
    passkey ="bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    data_to_encode = Business_short_code + passkey + lipa_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')
    # passkey = "a12e0f53ed291f694d752321736228f718d40a45f5e871401882037ccf0f5a41"

class MpesaB2cCredential:
    consumer_key = 'H3rGKgGKUWJBAeLi8SdecehfKdexN1Du'
    consumer_secret = 'oRUDeTkraL18TjjY'
    api_URL = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

class WthdrawalsMpesaCreds:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = "3027753"
    # passkey = 'a12e0f53ed291f694d752321736228f718d40a45f5e871401882037ccf0f5a41'
    passkey ="bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    data_to_encode = Business_short_code + passkey + lipa_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')