import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PYTHON = sys.executable

STEPS = [
    ("Lab 3 - Baseline ML Pipeline", "pipelines/run_lab3_baseline.py"),
    ("Lab 4 - MLflow Experiment Tracking", "pipelines/run_lab4_tracking.py"),
    ("Lab 5 - Production Data Pipeline", "pipelines/run_lab5_pipeline.py"),
    ("Lab 6 - Model Registry", "pipelines/run_lab6_registry.py"),
    ("Lab 7 - Model Quality Gate", "pipelines/run_lab7_pipeline.py"),
    ("Lab 8 - Model Lifecycle Promotion", "pipelines/run_lab8_pipeline.py"),
    ("Registry Deployment Report", "src/generate_registry_report.py"),
    ("Lab 9 - Production Inference", "pipelines/run_lab9_pipeline.py"),
    ("Lab 10 - Failure Handling and Recovery", "pipelines/run_lab10_pipeline.py"),
]

def main():
    print("=" * 72)
    print("CHURN PREDICTION PROJECT - LABS 3 TO 10")
    print("=" * 72)
    for label, relpath in STEPS:
        print(f"\n\n[RUNNING] {label}")
        result = subprocess.run([PYTHON, str(ROOT / relpath)], cwd=ROOT)
        if result.returncode != 0:
            print(f"\n[STOPPED] {label} failed (exit code {result.returncode}).")
            print("Fix the first reported error, then rerun: python run_all_labs.py")
            return result.returncode
        print(f"[PASSED] {label}")
    print("\n" + "=" * 72)
    print("[SUCCESS] ALL LABS 3 TO 10 COMPLETED.")
    print("Check reports/, artifacts/, outputs/, and the MLflow database.")
    print("=" * 72)
    return 0

if __name__ == "__main__":
    sys.exit(main())
