#include <vector>
#include <numeric>
#include <cmath>
#include <iostream>
#include <omp.h>   // OpenMP ekledik

extern "C" {

// Compute mean and std of an array (parallel with OpenMP)
__declspec(dllexport) void compute_mean_std(const double* data, int length,
                                            double* mean, double* stddev) {
    if (length <= 0) {
        *mean = NAN;
        *stddev = NAN;
        return;
    }

    double sum = 0.0;
    double sq_sum = 0.0;

    // OpenMP paralel for + reduction
    #pragma omp parallel for reduction(+:sum, sq_sum)
    for (int i = 0; i < length; i++) {
        sum += data[i];
        sq_sum += data[i] * data[i];
    }

    *mean = sum / length;
    *stddev = std::sqrt((sq_sum / length) - (*mean * *mean));
}

}
