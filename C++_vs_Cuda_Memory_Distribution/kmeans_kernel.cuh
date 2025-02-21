// kmeans_kernel.cuh
#ifndef KMEANS_KERNEL_CUH
#define KMEANS_KERNEL_CUH

#include "kmeans.h"

#ifdef __CUDACC__
#define CUDA_CALLABLE_MEMBER __device__
#define CUDA_KERNEL __global__
#else
#define CUDA_CALLABLE_MEMBER
#define CUDA_KERNEL
#endif

extern CUDA_CALLABLE_MEMBER float calculateDistanceDevice(const float* a, const float* b, int dims);
extern CUDA_KERNEL void initializeCentroidsKernel(float* centroids, const float* points, int numPoints, int numCentroids, int dims, unsigned long seed);
extern CUDA_KERNEL void findNearestCentroidKernel(const float* points, const float* centroids, int* labels, int numPoints, int numCentroids, int dims);
extern CUDA_KERNEL void updateCentroidsKernel(const float* points, const int* labels, float* newCentroids, int* clusterSizes, int numPoints, int numCentroids, int dims);
extern CUDA_KERNEL void normalizeCentroidsKernel(float* centroids, const int* clusterSizes, int numCentroids, int dims);
extern CUDA_KERNEL void checkConvergenceKernel(const float* oldCentroids, const float* newCentroids, int numCentroids, int dims, float threshold, int* converged);



#endif // KMEANS_KERNEL_CUH