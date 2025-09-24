#pragma once
#include <cstddef>

#if defined(_WIN32) || defined(_WIN64)
  #ifdef KALMAN_SOH_EXPORTS
    #define KALMAN_API __declspec(dllexport)
  #else
    #define KALMAN_API __declspec(dllimport)
  #endif
#else
  #define KALMAN_API __attribute__((visibility("default")))
#endif

#ifdef __cplusplus
extern "C" {
#endif

typedef void* KalmanHandle;

KALMAN_API KalmanHandle kalman_create(double q, double r, double x0, double p0);
KALMAN_API void kalman_destroy(KalmanHandle h);
KALMAN_API double kalman_update(KalmanHandle h, double z);
KALMAN_API void kalman_batch(KalmanHandle h, const double* z, int n, double* out);
KALMAN_API void kalman_smooth(double q, double r, double x0, double p0,
                              const double* z, int n, double* out);

#ifdef __cplusplus
}
#endif
