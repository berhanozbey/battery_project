# 🔋 Battery Project

This repository contains a complete end-to-end pipeline for **battery health monitoring (SOH & RUL prediction)**, optimized across Python, C++, and C#.

---

## 📂 Project Structure

battery_project/
│
├── ml-service/ # Python (data preprocessing & machine learning models)
├── core-engine/ # C++ (high-performance computations, compiled with CMake)
├── BatteryVisualizer/ # C# WPF Desktop App (interactive visualization, MVVM)
│
├── artifacts/ # Generated features, trained models, reports (ignored in git)
├── data/ # Raw dataset (ignored in git, too large for GitHub)
├── samples/ # Small sample dataset (10–15 MB) to test pipeline
│
├── config.yaml # Central config (paths, seeds, thresholds)
├── rul_linear.py # Simple RUL prediction script (Python)
└── README.md # This file



## ⚙️ Technical Requirements

- **Python 3.x** → pandas, scikit-learn, NumPy  
- **C++17** → CMake + Ninja (or MSVC)  
- **C# .NET 8 WPF** → MVVM architecture, LiveCharts for visualization  
- **Git LFS** (if full dataset is needed)

---

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/berhanozbey/battery_project.git
cd battery_project
2. Python (ml-service)
bash

cd ml-service
python -m venv venv
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# Example: prepare data
python prepare_data_isu_ilcc.py --config ../config.yaml --limit 100

# Train SOH model
python train_soh.py --input ../artifacts/features.parquet
3. C++ (core-engine)
bash

cd core-engine
mkdir build && cd build
cmake .. -G "Ninja"
cmake --build .

# produces core_engine.dll
4. C# WPF UI (BatteryVisualizer)
Open BatteryVisualizer.sln in Visual Studio

Run the project → you’ll see interactive charts:

Capacity vs Cycle

SOH vs Cycle

RUL predictions

📊 Features
✅ SOH prediction (Python) – Linear Regression & Random Forest

✅ RUL estimation – Linear fit over last SOH points

✅ High-performance C++ core – mean/std feature extraction

✅ WPF desktop app – interactive visualization with LiveCharts
🧪 Tests

Python unit tests under ml-service/tests/

C++ DLL tested via test_core_meanstd.py

C# UI logic separated in ViewModels/ for unit testing

📦 Deliverables

Full source code (Python, C++, C#)

Sample dataset (samples/) to test pipeline quickly

End-to-end desktop app

Technical report (see /docs/ if provided)

👤 Author

Berhan Özbey
GitHub: @berhanozbey

Email: berhan3030@hotmail.com