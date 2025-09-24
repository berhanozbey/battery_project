import numpy as np
import ctypes
from pathlib import Path

# core_engine.dll yolunu bul
dll_path = Path(__file__).resolve().parents[1] / "core-engine" / "build" / "core_engine.dll"
lib = ctypes.CDLL(str(dll_path))

# Fonksiyon imzalarını tanımla
lib.compute_mean_std.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int,
                                 ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
lib.compute_mean_std.restype = None

# Test verisi
data = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)
mean = ctypes.c_double()
std = ctypes.c_double()

# C++ fonksiyonunu çağır
lib.compute_mean_std(data.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), len(data),
                     ctypes.byref(mean), ctypes.byref(std))

print("Input data:", data)
print("Mean (from C++):", mean.value)
print("Std  (from C++):", std.value)
