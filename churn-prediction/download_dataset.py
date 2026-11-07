from pathlib import Path
from urllib.request import urlopen
import hashlib
import sys

URL = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
EXPECTED_SHA256 = "16320c9c1ec72448db59aa0a26a0b95401046bef5d02fd3aeb906448e3055e91"
DEST = Path(__file__).resolve().parent / "data" / "raw" / "churn.csv"

def main():
    DEST.parent.mkdir(parents=True, exist_ok=True)
    if DEST.exists():
        digest = hashlib.sha256(DEST.read_bytes()).hexdigest()
        if digest == EXPECTED_SHA256:
            print(f"[OK] Dataset already exists and checksum is valid: {DEST}")
            return 0
        print("[INFO] Existing dataset has a different checksum; downloading a clean copy.")
    print("[INFO] Downloading IBM Telco Customer Churn dataset...")
    try:
        with urlopen(URL, timeout=45) as response:
            data = response.read()
        digest = hashlib.sha256(data).hexdigest()
        if digest != EXPECTED_SHA256:
            raise ValueError(f"Dataset checksum mismatch: {digest}")
        DEST.write_bytes(data)
        print(f"[SUCCESS] Saved {len(data):,} bytes to {DEST}")
        print("[SUCCESS] SHA-256 verified.")
        return 0
    except Exception as exc:
        print(f"[ERROR] Dataset download failed: {exc}")
        print("Download the IBM Telco Customer Churn CSV manually and save it as:")
        print(DEST)
        return 1

if __name__ == "__main__":
    sys.exit(main())
