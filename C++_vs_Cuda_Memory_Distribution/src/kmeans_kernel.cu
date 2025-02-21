// kmeans_kernel.cu
#include "kmeans_kernel.cuh"
#include <cuda_runtime.h>
#include <curand_kernel.h>

__device__ float calculateDistanceDevice(const float* a, const float* b, int dims) {
    float sum = 0;
    for (int i = 0; i < dims; i++) {
        float diff = a[i] - b[i];
        sum += diff * diff;
    }
    return sum;
}

__global__ void initializeCentroidsKernel(float* centroids, const float* points, int numPoints, int numCentroids, int dims, unsigned long seed) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < numCentroids) {
        curandState state;
        curand_init(seed, idx, 0, &state);
        int randomIndex = curand(&state) % numPoints;
        for (int d = 0; d < dims; d++) {
            centroids[idx * dims + d] = points[randomIndex * dims + d];
        }
    }
}

__global__ void findNearestCentroidKernel(const float* points, const float* centroids, int* labels, int numPoints, int numCentroids, int dims) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < numPoints) {
        float minDistance = INFINITY;
        int nearestCentroid = 0;
        for (int c = 0; c < numCentroids; c++) {
            float distance = calculateDistanceDevice(&points[idx * dims], &centroids[c * dims], dims);
            if (distance < minDistance) {
                minDistance = distance;
                nearestCentroid = c;
            }
        }
        labels[idx] = nearestCentroid;
    }
}

__global__ void updateCentroidsKernel(const float* points, const int* labels, float* newCentroids, int* clusterSizes, int numPoints, int numCentroids, int dims) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < numPoints) {
        int label = labels[idx];
        for (int d = 0; d < dims; d++) {
            atomicAdd(&newCentroids[label * dims + d], points[idx * dims + d]);
        }
        atomicAdd(&clusterSizes[label], 1);
    }
}

__global__ void normalizeCentroidsKernel(float* centroids, const int* clusterSizes, int numCentroids, int dims) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < numCentroids) {
        int size = clusterSizes[idx];
        if (size > 0) {
            for (int d = 0; d < dims; d++) {
                centroids[idx * dims + d] /= size;
            }
        }
    }
}

__global__ void checkConvergenceKernel(const float* oldCentroids, const float* newCentroids, int numCentroids, int dims, float threshold, int* converged) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < numCentroids) {
        float distance = calculateDistanceDevice(&oldCentroids[idx * dims], &newCentroids[idx * dims], dims);
        if (distance > threshold * threshold) {
            *converged = 0;
        }
    }
}