# Churn Prediction — Labs 3 to 10 (Windows 11)

## One-time setup

1. Extract this ZIP.
2. Open the extracted `churn-prediction` folder in VS Code.
3. Open Terminal → PowerShell.
4. Run the following command:

```powershell
Set-Location "C:\Users\ASUS\OneDrive\Desktop\churn-prediction\churn-prediction"
```

If you extracted it somewhere else, replace the path with your actual project folder.

## Recommended: one command to install and run Labs 3–10

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\setup_and_run.bat
```

The batch file creates a Python 3.11 virtual environment, installs the required packages, downloads and verifies the IBM Telco Customer Churn CSV, then runs Labs 3–10 in dependency order. An internet connection is required for package and dataset downloads.

## If setup is already complete

Activate the environment and run the complete sequence:

```powershell
.\.venv\Scripts\Activate.ps1
python .\run_all_labs.py
```

## Run one lab at a time

Run these from the project root, in order:

```powershell
python .\pipelines\run_lab3_baseline.py
python .\pipelines\run_lab4_tracking.py
python .\pipelines\run_lab5_pipeline.py
python .\pipelines\run_lab6_registry.py
python .\pipelines\run_lab7_pipeline.py
python .\pipelines\run_lab8_pipeline.py
python .\src\generate_registry_report.py
python .\pipelines\run_lab9_pipeline.py
python .\pipelines\run_lab10_pipeline.py
```

Lab 6 registers a model; Lab 8 promotes the best registered model to Production. The deployment report is generated after Lab 8.

## Important

- Do not run `run_lab3_baseline.py` from inside the `pipelines` folder. Run it from the project root.
- Keep `config.yaml` in the project root.
- Keep the raw CSV at `data/raw/churn.csv`.
- Lab 10 deliberately changes files temporarily to test failure handling, then restores them.
- Reports are written under `artifacts/` and `reports/`; inference CSVs are written under `outputs/`.
- The dataset is IBM's public Telco Customer Churn sample (7,043 rows, 21 columns). The downloader verifies the published SHA-256 checksum before saving it.
