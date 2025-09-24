import numpy as np
import ctypes
from pathlib import Path
import time

# DLL yolunu bul
dll_path = Path(__file__).resolve().parents[1] / "core-engine" / "build" / "core_engine.dll"
lib = ctypes.CDLL(str(dll_path))

# Fonksiyon imzaları
lib.compute_mean_std.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int,
                                 ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
lib.compute_mean_std.restype = None

# Küçük test verisi
data = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)
mean = ctypes.c_double()
std = ctypes.c_double()

lib.compute_mean_std(data.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), len(data),
                     ctypes.byref(mean), ctypes.byref(std))

print("Input data:", data)
print("Mean (from C++):", mean.value)
print("Std  (from C++):", std.value)

# NumPy karşılaştırması
np_mean = np.mean(data)
np_std = np.std(data)
print("Mean (NumPy):", np_mean)
print("Std  (NumPy):", np_std)

# Büyük veri testi (performans)
big_data = np.random.rand(10_000_000).astype(np.float64)

# NumPy zaman ölçümü
t0 = time.time()
np_mean = np.mean(big_data)
np_std = np.std(big_data)
t1 = time.time()
print(f"\n[NumPy] Mean={np_mean:.5f}, Std={np_std:.5f}, Time={t1-t0:.4f}s")

# C++ zaman ölçümü
mean = ctypes.c_double()
std = ctypes.c_double()

t0 = time.time()
lib.compute_mean_std(big_data.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), len(big_data),
                     ctypes.byref(mean), ctypes.byref(std))
t1 = time.time()
print(f"[C++]   Mean={mean.value:.5f}, Std={std.value:.5f}, Time={t1-t0:.4f}s")
