import ctypes
import numpy as np

# Derlenen DLL dosyasını yükle
lib = ctypes.CDLL(r"C:\Users\berha\battery_project\core-engine\build\core_engine.dll")

# Fonksiyonun imzasını tanımla
lib.compute_features.argtypes = [
    ctypes.POINTER(ctypes.c_double),  # data pointer
    ctypes.c_int,                     # length
    ctypes.POINTER(ctypes.c_double),  # mean output
    ctypes.POINTER(ctypes.c_double)   # std output
]
lib.compute_features.restype = None

# Test verisi
data = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)

mean_val = ctypes.c_double()
std_val = ctypes.c_double()

# C++ fonksiyonunu çağır
lib.compute_features(
    data.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
    len(data),
    ctypes.byref(mean_val),
    ctypes.byref(std_val)
)

print("Mean:", mean_val.value)
print("Std :", std_val.value)
