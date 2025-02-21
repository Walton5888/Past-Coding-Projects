// kmeans_shmem.cu
#include "kmeans_kernel.cuh"
#include "kmeans_implementations.h"
#include <cuda_runtime.h>
#include <thrust/device_vector.h>
#include <thrust/host_vector.h>
#include <thrust/copy.h>
#include <thrust/fill.h>
#include <thrust/extrema.h>
#include <cmath>

// Shared memory optimized kernels

__global__ void findNearestCentroidSharedKernel(const float* points, const float* centroids, int* labels, int numPoints, int numCentroids, int dims) {
    extern __shared__ float sharedCentroids[];
    
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    
    // Load centroids into shared memory
    for (int i = threadIdx.x; i < numCentroids * dims; i += blockDim.x) {
        sharedCentroids[i] = centroids[i];
    }
    __syncthreads();
    
    if (idx < numPoints) {
        float minDistance = INFINITY;
        int nearestCentroid = 0;
        for (int c = 0; c < numCentroids; c++) {
            float distance = 0;
            for (int d = 0; d < dims; d++) {
                float diff = points[idx * dims + d] - sharedCentroids[c * dims + d];
                distance += diff * diff;
            }
            if (distance < minDistance) {
                minDistance = distance;
                nearestCentroid = c;
            }
        }
        labels[idx] = nearestCentroid;
    }
}

// You can add more shared memory optimized functions here

KMeansResult runCUDAShmemKMeans(const std::vector<float>& points, const KMeansParams& params) {
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
        // Find nearest centroid for each point using shared memory
        gridSize = (numPoints + blockSize - 1) / blockSize;
        int sharedMemSize = params.k * params.dims * sizeof(float);
        findNearestCentroidSharedKernel<<<gridSize, blockSize, sharedMemSize>>>(
            thrust::raw_pointer_cast(d_points.data()),
            thrust::raw_pointer_cast(d_centroids.data()),
            thrust::raw_pointer_cast(d_labels.data()),
            numPoints, params.k, params.dims
        );

        // Reset new centroids and cluster sizes
        thrust::fill(d_newCentroids.begin(), d_newCentroids.end(), 0.0f);
        thrust::fill(d_clusterSizes.begin(), d_clusterSizes.end(), 0);

        // Update centroids
        updateCentroidsKernel<<<gridSize, blockSize>>>(
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