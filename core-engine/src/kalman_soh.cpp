#include "kalman_soh.h"
#include <new>
#include <cstring>

struct KF {
    double q;
    double r;
    double x;
    double p;
};

extern "C" {

KALMAN_API KalmanHandle kalman_create(double q, double r, double x0, double p0) {
    KF* kf = new (std::nothrow) KF();
    if (!kf) return nullptr;
    kf->q = (q > 0.0 ? q : 1e-6);
    kf->r = (r > 0.0 ? r : 1e-3);
    kf->x = x0;
    kf->p = (p0 > 0.0 ? p0 : 1.0);
    return reinterpret_cast<KalmanHandle>(kf);
}

KALMAN_API void kalman_destroy(KalmanHandle h) {
    if (!h) return;
    KF* kf = reinterpret_cast<KF*>(h);
    delete kf;
}

KALMAN_API double kalman_update(KalmanHandle h, double z) {
    if (!h) return 0.0;
    KF* kf = reinterpret_cast<KF*>(h);

    double x_prior = kf->x;
    double p_prior = kf->p + kf->q;

    double S = p_prior + kf->r;
    double K = (S > 0.0) ? (p_prior / S) : 0.0;

    kf->x = x_prior + K * (z - x_prior);
    kf->p = (1.0 - K) * p_prior;

    return kf->x;
}

KALMAN_API void kalman_batch(KalmanHandle h, const double* z, int n, double* out) {
    if (!h || !z || !out || n <= 0) return;
    for (int i = 0; i < n; ++i) {
        out[i] = kalman_update(h, z[i]);
    }
}

KALMAN_API void kalman_smooth(double q, double r, double x0, double p0,
                              const double* z, int n, double* out) {
    if (!z || !out || n <= 0) return;
    KalmanHandle h = kalman_create(q, r, x0, p0);
    if (!h) return;
    kalman_batch(h, z, n, out);
    kalman_destroy(h);
}

}
