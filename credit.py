import pandas as pd
import uuid
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
DRIVERS_CSV = BASE_DIR / "drivers.csv"
LEDGER_CSV = BASE_DIR / "wallet_ledger.csv"


def _load_drivers():
    if not DRIVERS_CSV.exists() or DRIVERS_CSV.stat().st_size == 0:
        return pd.DataFrame(columns=["driver_id", "name", "phone", "created_at"])
    return pd.read_csv(DRIVERS_CSV)


def _save_drivers(df):
    df.to_csv(DRIVERS_CSV, index=False)


def _load_ledger():
    if not LEDGER_CSV.exists() or LEDGER_CSV.stat().st_size == 0:
        return pd.DataFrame(columns=[
            "entry_id", "driver_id", "type", "amount",
            "status", "reason", "reference_id", "timestamp"
        ])
    return pd.read_csv(LEDGER_CSV)


def _save_ledger(df):
    df.to_csv(LEDGER_CSV, index=False)


def driver_exists(driver_id):
    return driver_id in _load_drivers()["driver_id"].values


def add_driver(driver_id, name, phone):
    drivers = _load_drivers()
    if driver_exists(driver_id):
        print("⚠️ Driver already exists")
        return

    drivers = pd.concat([drivers, pd.DataFrame([{
        "driver_id": driver_id,
        "name": name,
        "phone": phone,
        "created_at": datetime.utcnow().isoformat()
    }])])
    _save_drivers(drivers)
    print("✅ Driver added")


def credit_driver(driver_id, amount, reason):
    ledger = _load_ledger()
    ledger = pd.concat([ledger, pd.DataFrame([{
        "entry_id": str(uuid.uuid4()),
        "driver_id": driver_id,
        "type": "CREDIT",
        "amount": amount,
        "status": "SUCCESS",
        "reason": reason,
        "reference_id": "",
        "timestamp": datetime.utcnow().isoformat()
    }])])
    _save_ledger(ledger)
    print("✅ Wallet credited")


def get_wallet_balance(driver_id):
    ledger = _load_ledger()
    credit = ledger[(ledger.driver_id == driver_id) & (ledger.type == "CREDIT")]["amount"].sum()
    debit = ledger[(ledger.driver_id == driver_id) & (ledger.type == "DEBIT") & (ledger.status == "SUCCESS")]["amount"].sum()
    return credit - debit