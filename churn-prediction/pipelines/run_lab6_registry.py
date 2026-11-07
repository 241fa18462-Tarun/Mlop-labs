import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def main():
    print("[INFO] =========================================")
    print("[INFO] Starting Lab 6: Model Registry")
    print("[INFO] =========================================")
    script = PROJECT_ROOT / "src" / "train_registry.py"
    result = subprocess.run([sys.executable, str(script)], cwd=PROJECT_ROOT)
    if result.returncode:
        print("[ERROR] Lab 6 registry training failed.")
        return result.returncode
    print("[SUCCESS] Lab 6 registry model created.")
    print("[INFO] Run Lab 8 to promote a registered version to Production.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
