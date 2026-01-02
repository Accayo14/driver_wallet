import requests
from requests.auth import HTTPBasicAuth

KEY = "rzp_test_Ryb78kFQqtHzV8"
SECRET = "pZ46Rkh0GElxjxVNPLTdQAZd"

url = "https://api.razorpay.com/v1/payouts"

payload = {
    "account_number": "2323230064404282",  # REQUIRED (test balance)
    "amount": 100,                       # 1 INR in paise
    "currency": "INR",
    "mode": "UPI",
    "purpose": "payout",
    "fund_account": {
        "account_type": "upi",
        "upi": {
            "address": "success@razorpay"
        }
    }
}

r = requests.post(
    url,
    json=payload,
    auth=HTTPBasicAuth(KEY, SECRET)
)

print(r.status_code)
print(r.text)