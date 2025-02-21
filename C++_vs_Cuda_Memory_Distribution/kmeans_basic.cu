// kmeans_basic.cu
#include "kmeans_kernel.cuh"
#include <cuda_runtime.h>
#include <curand_kernel.h>
#include <thrust/device_vector.h>
#include <thrust/host_vector.h>
#include <thrust/copy.h>
#include <thrust/fill.h>
#include <thrust/extrema.h>
#include <cmath>

__device__ float calculateDistanceBasic(const float* a, const float* b, int dims) {
    float sum = 0;
    for (int i = 0; i < dims; i++) {
        float diff = a[i] - b[i];
        sum += diff * diff;
    }
    return sum;
}

__global__ void findNearestCentroidBasicKernel(const float* points, const float* centroids, int* labels, int numPoints, int numCentroids, int dims) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < numPoints) {
        float minDistance = INFINITY;
        int nearestCentroid = 0;
        for (int c = 0; c < numCentroids; c++) {
            float distance = calculateDistanceBasic(&points[idx * dims], &centroids[c * dims], dims);
            if (distance < minDistance) {
                minDistance = distance;
                nearestCentroid = c;
            }
        }
        labels[idx] = nearestCentroid;
    }
}

__global__ void updateCentroidsBasicKernel(const float* points, const int* labels, float* newCentroids, int* clusterSizes, int numPoints, int numCentroids, int dims) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < numPoints) {
        int label = labels[idx];
        for (int d = 0; d < dims; d++) {
            atomicAdd(&newCentroids[label * dims + d], points[idx * dims + d]);
        }
        atomicAdd(&clusterSizes[label], 1);
    }
}

KMeansResult runCUDABasicKMeans(const std::vector<float>& points, const KMeansParams& params) {
    int numPoints = points.size() / params.dims;
    
    // Create device vectors
    thrust::device_vector<float> d_points = points;
    thrust::device_vector<float> d_centroids(params.k * params.dims);
    thrust::device_vector<float> d_newCentroids(params.k * params.dims);
    thrust::device_vector<int> d_labels(numPoints);
    thrust::device_vector<int> d_clusterSizes(params.k);
    thrust::device_vector<int> d_converged(1);

    // Initialize centroids
    int blockSize = 256;
    int gridSize = (params.k + blockSize - 1) / blockSize;
    initializeCentroidsKernel<<<gridSize, blockSize>>>(
        thrust::raw_pointer_cast(d_centroids.data()),
        thrust::raw_pointer_cast(d_points.data()),
        numPoints, params.k, params.dims, params.seed
    );

    int iterations = 0;
    bool converged = false;
    while (iterations < params.maxIterations && !converged) {
        // Find nearest centroid for each point
        gridSize = (numPoints + blockSize - 1) / blockSize;
        findNearestCentroidBasicKernel<<<gridSize, blockSize>>>(
            thrust::raw_pointer_cast(d_points.data()),
            thrust::raw_pointer_cast(d_centroids.data()),
            thrust::raw_pointer_cast(d_labels.data()),
            numPoints, params.k, params.dims
        );

        // Reset new centroids and cluster sizes
        thrust::fill(d_newCentroids.begin(), d_newCentroids.end(), 0.0f);
        thrust::fill(d_clusterSizes.begin(), d_clusterSizes.end(), 0);

        // Update centroids
        updateCentroidsBasicKernel<<<gridSize, blockSize>>>(
            thrust::raw_pointer_cast(d_points.data()),
            thrust::raw_pointer_cast(d_labels.data()),
            thrust::raw_pointer_cast(d_newCentroids.data()),
            thrust::raw_pointer_cast(d_clusterSizes.data()),
            numPoints, params.k, params.dims
        );

        // Normalize centroids
        gridSize = (params.k + blockSize - 1) / blockSize;
        normalizeCentroidsKernel<<<gridSize, blockSize>>>(
            thrust::raw_pointer_cast(d_newCentroids.data()),
            thrust::raw_pointer_cast(d_clusterSizes.data()),
            params.k, params.dims
        );

        // Check for convergence
        thrust::fill(d_converged.begin(), d_converged.end(), 1);
        checkConvergenceKernel<<<gridSize, blockSize>>>(
            thrust::raw_pointer_cast(d_centroids.data()),
            thrust::raw_pointer_cast(d_newCentroids.data()),
            params.k, params.dims, params.threshold,
            thrust::raw_pointer_cast(d_converged.data())
        );

        converged = d_converged[0] == 1;

        // Update centroids for next iteration
        d_centroids = d_newCentroids;

        iterations++;
    }

    // Copy results back to host
    thrust::host_vector<int> h_labels = d_labels;
    thrust::host_vector<float> h_centroids = d_centroids;

    std::vector<int> labels(h_labels.begin(), h_labels.end());
    std::vector<std::vector<float>> finalCentroids(params.k, std::vector<float>(params.dims));
    for (int i = 0; i < params.k; i++) {
        for (int d = 0; d < params.dims; d++) {
            finalCentroids[i][d] = h_centroids[i * params.dims + d];
        }
    }

    return KMeansResult{labels, finalCentroids, iterations, 0.0}; // Time per iteration is calculated in main.cpp
}