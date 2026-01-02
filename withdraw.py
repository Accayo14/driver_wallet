import pandas as pd
import uuid
from datetime import datetime
from pathlib import Path

from credit import (
    driver_exists,
    get_wallet_balance,
    _load_ledger,
    _save_ledger
)

from razorpay_payments import create_withdraw_order

BASE_DIR = Path(__file__).parent
WITHDRAWALS_CSV = BASE_DIR / "withdrawals.csv"


def _load_withdrawals():
    if not WITHDRAWALS_CSV.exists() or WITHDRAWALS_CSV.stat().st_size == 0:
        return pd.DataFrame(columns=[
            "withdrawal_id", "driver_id", "amount",
            "status", "razorpay_order_id", "created_at"
        ])
    return pd.read_csv(WITHDRAWALS_CSV)


def _save_withdrawals(df):
    df.to_csv(WITHDRAWALS_CSV, index=False)


def withdraw(driver_id, amount):
    if not driver_exists(driver_id):
        raise ValueError("Driver not found")

    balance = get_wallet_balance(driver_id)
    if balance < amount:
        raise ValueError("Insufficient balance")

    withdrawal_id = f"wd_{uuid.uuid4().hex[:8]}"

    # Lock wallet
    ledger = _load_ledger()
    ledger = pd.concat([ledger, pd.DataFrame([{
        "entry_id": str(uuid.uuid4()),
        "driver_id": driver_id,
        "type": "DEBIT",
        "amount": amount,
        "status": "PENDING",
        "reason": "WITHDRAW",
        "reference_id": withdrawal_id,
        "timestamp": datetime.utcnow().isoformat()
    }])])
    _save_ledger(ledger)

    # Create Razorpay order
    order = create_withdraw_order(amount)

    # Mark SUCCESS (demo assumption)
    ledger.loc[ledger.reference_id == withdrawal_id, "status"] = "SUCCESS"
    _save_ledger(ledger)

    withdrawals = _load_withdrawals()
    withdrawals = pd.concat([withdrawals, pd.DataFrame([{
        "withdrawal_id": withdrawal_id,
        "driver_id": driver_id,
        "amount": amount,
        "status": "SUCCESS",
        "razorpay_order_id": order["id"],
        "created_at": datetime.utcnow().isoformat()
    }])])
    _save_withdrawals(withdrawals)

    print("✅ Withdrawal completed")
    print("Razorpay Order ID:", order["id"])