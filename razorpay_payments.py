import razorpay
import uuid
from config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET

client = razorpay.Client(
    auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)
)


def create_withdraw_order(amount):
    """
    Creates a Razorpay ORDER (test mode).
    """

    order = client.order.create({
        "amount": int(amount * 100),  # paise
        "currency": "INR",
        "receipt": f"withdraw_{uuid.uuid4().hex[:8]}",
        "payment_capture": 1
    })

    return order