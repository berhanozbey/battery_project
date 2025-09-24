\# 🔋 Battery Project



This project implements a \*\*battery health prediction pipeline\*\* with three main components:



1\. \*\*Machine Learning Service (Pytho# 🔋 Battery Project



This project implements a \*\*battery health prediction pipeline\*\* with three main components:



1\. \*\*Machine Learning Service (Python)\*\*

&nbsp;  - Preprocess raw battery test data (CSV/JSON/Parquet)

&nbsp;  - Extract features (capacity, SOH, RUL, cycle statistics)

&nbsp;  - Train predictive models (SOH regression, RUL estimation)

&nbsp;  - Scripts:

&nbsp;    - `prepare\_data\_isu\_ilcc.py`: Preprocess ISU-ILCC dataset

&nbsp;    - `train\_soh.py`: Train models (Linear Regression, Random Forest)

&nbsp;    - `rul\_linear.py`: Estimate Remaining Useful Life (RUL)



2\. \*\*High-Performance Core Engine (C++17)\*\*

&nbsp;  - Optimized numerical routines (mean/std, feature extraction, etc.)

&nbsp;  - Built with \*\*CMake\*\* and \*\*Ninja\*\*

&nbsp;  - Exposed as a shared library (`core\_engine.dll`) for Python and C# interoperability



3\. \*\*Desktop Visualization (C# WPF, .NET 8)\*\*

&nbsp;  - User-friendly UI for loading processed data

&nbsp;  - Interactive charts (Capacity vs Cycle, SOH/RUL predictions)

&nbsp;  - Toggle between \*\*Cycling\*\* vs \*\*RPT\*\* views

&nbsp;  - Highlight censored cells (no 80% crossing) in RUL plots

&nbsp;  - Export results to \*\*PDF\*\* or \*\*Excel\*\*



---



\## 📂 Repository Structure



battery\_project/

│

├── ml-service/ # Python scripts for preprocessing \& modeling

│ ├── prepare\_data\_isu\_ilcc.py

│ ├── train\_soh.py

│ ├── rul\_linear.py

│ └── test\_core.py

│

├── core-engine/ # C++ high-performance engine

│ ├── src/core\_engine.cpp

│ ├── CMakeLists.txt

│ └── build/

│

├── BatteryVisualizer/ # C# WPF Desktop UI (MVVM)

│ ├── Models/

│ ├── ViewModels/

│ ├── Views/

│ └── MainWindow.xaml

│

├── samples/ # Small sample dataset (10–15 MB max)

│ ├── sample.json

│ └── sample.parquet

│

├── config.yaml # Config file (paths, seeds, nominal capacity)

├── README.md # Project documentation (this file)

└── .gitignore



yaml

Kodu kopyala



---



\## 🚀 Installation \& Usage



\### 1. Clone Repository

```bash

git clone https://github.com/berhanozbey/battery\_project.git

cd battery\_project

2\. Python ML Service

bash

Kodu kopyala

cd ml-service

python -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt



\# Example: preprocess 50 rows

python prepare\_data\_isu\_ilcc.py --config ../config.yaml --limit 50



\# Train SOH model

python train\_soh.py --input ../artifacts/features.parquet



\# Estimate RUL

python rul\_linear.py --input ../artifacts/features.parquet

3\. C++ Core Engine

bash

Kodu kopyala

cd core-engine

mkdir build \&\& cd build

cmake .. -G "Ninja"

cmake --build .

This produces core\_engine.dll in the build/ directory.



4\. WPF Desktop App (C# .NET 8)

bash

Kodu kopyala

cd BatteryVisualizer

dotnet build

dotnet run

📊 Features Implemented

✅ Data cleaning and preprocessing



✅ Feature extraction (C/5 capacity, ΔV\_hyst, cycles between RPTs)



✅ SOH regression (Linear Regression, Random Forest)



✅ RUL estimation (linear fit)



✅ High-performance C++ backend with Python interop



✅ WPF UI for visualization and reporting



📈 Performance Benchmarks

Task	Python (NumPy)	C++ Core Engine

Mean/Std (1e6 data)	~0.046s	~0.025s



📦 Deliverables

Full source code in Python, C++, C#



Example dataset (samples/)



Config file (config.yaml)



Automated tests (ml-service/test\_core.py)



Documentation (README.md)



WPF UI screenshots (to be added)



🛠 Requirements

Python 3.10+



C++17 (MSVC, GCC, or Clang)



CMake + Ninja



.NET 8 SDK



Git



✅ Next Steps

Add unit tests in each module (pytest, gtest, MSTest/NUnit).



Upload sample dataset under samples/.



Add screenshots of the WPF app to README.md.



📜 License

MIT License (or specify your choice)



📧 Contact

Maintainer: Berhan Özbey

Email: berhan3030@hotmail.com

GitHub: @berhanozbey



yaml

Kodu kopyala



---



\# 🔧 GitHub’a README.md ekleme adımları



1\. Proje klasörüne `README.md` dosyası oluştur:  

&nbsp;  ```powershell

&nbsp;  cd C:\\Users\\berha\\battery\_project

&nbsp;  notepad README.mdn)\*\*

&nbsp;  - Preprocess raw battery test data (CSV/JSON/Parquet)

&nbsp;  - Extract features (capacity, SOH, RUL, cycle statistics)

&nbsp;  - Train predictive models (SOH regression, RUL estimation)

&nbsp;  - Scripts:

&nbsp;    - `prepare\_data\_isu\_ilcc.py`: Preprocess ISU-ILCC dataset

&nbsp;    - `train\_soh.py`: Train models (Linear Regression, Random Forest)

&nbsp;    - `rul\_linear.py`: Estimate Remaining Useful Life (RUL)



2\. \*\*High-Performance Core Engine (C++17)\*\*

&nbsp;  - Optimized numerical routines (mean/std, feature extraction, etc.)

&nbsp;  - Built with \*\*CMake\*\* and \*\*Ninja\*\*

&nbsp;  - Exposed as a shared library (`core\_engine.dll`) for Python and C# interoperability



3\. \*\*Desktop Visualization (C# WPF, .NET 8)\*\*

&nbsp;  - User-friendly UI for loading processed data

&nbsp;  - Interactive charts (Capacity vs Cycle, SOH/RUL predictions)

&nbsp;  - Toggle between \*\*Cycling\*\* vs \*\*RPT\*\* views

&nbsp;  - Highlight censored cells (no 80% crossing) in RUL plots

&nbsp;  - Export results to \*\*PDF\*\* or \*\*Excel\*\*



---



\## 📂 Repository Structure



battery\_project/

│

├── ml-service/ # Python scripts for preprocessing \& modeling

│ ├── prepare\_data\_isu\_ilcc.py

│ ├── train\_soh.py

│ ├── rul\_linear.py

│ └── test\_core.py

│

├── core-engine/ # C++ high-performance engine

│ ├── src/core\_engine.cpp

│ ├── CMakeLists.txt

│ └── build/

│

├── BatteryVisualizer/ # C# WPF Desktop UI (MVVM)

│ ├── Models/

│ ├── ViewModels/

│ ├── Views/

│ └── MainWindow.xaml

│

├── samples/ # Small sample dataset (10–15 MB max)

│ ├── sample.json

│ └── sample.parquet

│

├── config.yaml # Config file (paths, seeds, nominal capacity)

├── README.md # Project documentation (this file)

└── .gitignore



yaml

Kodu kopyala



---



\## 🚀 Installation \& Usage



\### 1. Clone Repository

```bash

git clone https://github.com/berhanozbey/battery\_project.git

cd battery\_project

2\. Python ML Service

bash

Kodu kopyala

cd ml-service

python -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt



\# Example: preprocess 50 rows

python prepare\_data\_isu\_ilcc.py --config ../config.yaml --limit 50



\# Train SOH model

python train\_soh.py --input ../artifacts/features.parquet



\# Estimate RUL

python rul\_linear.py --input ../artifacts/features.parquet

3\. C++ Core Engine

bash

Kodu kopyala

cd core-engine

mkdir build \&\& cd build

cmake .. -G "Ninja"

cmake --build .

This produces core\_engine.dll in the build/ directory.



4\. WPF Desktop App (C# .NET 8)

bash

Kodu kopyala

cd BatteryVisualizer

dotnet build

dotnet run

📊 Features Implemented

✅ Data cleaning and preprocessing



✅ Feature extraction (C/5 capacity, ΔV\_hyst, cycles between RPTs)



✅ SOH regression (Linear Regression, Random Forest)



✅ RUL estimation (linear fit)



✅ High-performance C++ backend with Python interop



✅ WPF UI for visualization and reporting



📈 Performance Benchmarks

Task	Python (NumPy)	C++ Core Engine

Mean/Std (1e6 data)	~0.046s	~0.025s



📦 Deliverables

Full source code in Python, C++, C#



Example dataset (samples/)



Config file (config.yaml)



Automated tests (ml-service/test\_core.py)



Documentation (README.md)



WPF UI screenshots (to be added)



🛠 Requirements

Python 3.10+



C++17 (MSVC, GCC, or Clang)



CMake + Ninja



.NET 8 SDK



Git



✅ Next Steps

Add unit tests in each module (pytest, gtest, MSTest/NUnit).



Upload sample dataset under samples/.



Add screenshots of the WPF app to README.md.



📜 License

MIT License (or specify your choice)



📧 Contact

Maintainer: Berhan Özbey

Email: berhan3030@hotmail.com

GitHub: @berhanozbey







