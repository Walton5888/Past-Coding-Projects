#include "kmeans.h"
#include <thrust/device_vector.h>
#include <thrust/host_vector.h>
#include <thrust/copy.h>
#include <thrust/fill.h>
#include <thrust/transform.h>
#include <thrust/functional.h>
#include <thrust/iterator/counting_iterator.h>
#include <thrust/extrema.h>
#include <thrust/random.h>
#include <cmath>
#include <limits>

struct CalculateDistance {
    const float* points;
    const float* centroids;
    int dims;
    int k;
    int numPoints;

    CalculateDistance(const float* _points, const float* _centroids, int _dims, int _k, int _numPoints) 
        : points(_points), centroids(_centroids), dims(_dims), k(_k), numPoints(_numPoints) {}

    __device__
    int operator()(int idx) const {
        const float* point = points + idx * dims;
        float min_dist = INFINITY;
        int nearest_centroid = 0;

        for (int i = 0; i < k; ++i) {
            float dist = 0;
            for (int d = 0; d < dims; ++d) {
                float diff = point[d] - centroids[i * dims + d];
                dist += diff * diff;
            }
            if (dist < min_dist) {
                min_dist = dist;
                nearest_centroid = i;
            }
        }

        return nearest_centroid;
    }
};

KMeansResult runThrustKMeans(const std::vector<float>& points, const KMeansParams& params) {
    int numPoints = points.size() / params.dims;

    // Create device vectors
    thrust::device_vector<float> d_points = points;
    thrust::device_vector<float> d_centroids(params.k * params.dims);
    thrust::device_vector<int> d_labels(numPoints);
    thrust::device_vector<float> d_newCentroids(params.k * params.dims);
    thrust::device_vector<int> d_clusterSizes(params.k);

    // Initialize centroids randomly
    thrust::default_random_engine rng(params.seed);
    thrust::uniform_int_distribution<int> dist(0, numPoints - 1);
    for (int i = 0; i < params.k; ++i) {
        int idx = dist(rng);
        thrust::copy(d_points.begin() + idx * params.dims, 
                     d_points.begin() + (idx + 1) * params.dims, 
                     d_centroids.begin() + i * params.dims);
    }

    int iterations = 0;
    bool converged = false;

    while (iterations < params.maxIterations && !converged) {
        // Assign points to nearest centroid
        thrust::transform(
            thrust::counting_iterator<int>(0),
            thrust::counting_iterator<int>(numPoints),
            d_labels.begin(),
            CalculateDistance(thrust::raw_pointer_cast(d_points.data()),
                              thrust::raw_pointer_cast(d_centroids.data()),
                              params.dims, params.k, numPoints)
        );

        // Reset new centroids and cluster sizes
        thrust::fill(d_newCentroids.begin(), d_newCentroids.end(), 0.0f);
        thrust::fill(d_clusterSizes.begin(), d_clusterSizes.end(), 0);

        // Update centroids
        for (int i = 0; i < numPoints; ++i) {
            int label = d_labels[i];
            for (int d = 0; d < params.dims; ++d) {
                d_newCentroids[label * params.dims + d] += d_points[i * params.dims + d];
            }
            d_clusterSizes[label]++;
        }

        // Normalize centroids
        for (int i = 0; i < params.k; ++i) {
            if (d_clusterSizes[i] > 0) {
                for (int d = 0; d < params.dims; ++d) {
                    d_newCentroids[i * params.dims + d] /= d_clusterSizes[i];
                }
            }
        }

        // Check for convergence
        float max_movement = 0.0f;
        for (int i = 0; i < params.k * params.dims; ++i) {
            float diff = d_centroids[i] - d_newCentroids[i];
            max_movement = max(max_movement, diff * diff);
        }

        converged = (std::sqrt(max_movement) <= params.threshold);

        // Update centroids for next iteration
        d_centroids = d_newCentroids;

        iterations++;
    }

    // Copy results back to host
    std::vector<int> labels(numPoints);
    thrust::copy(d_labels.begin(), d_labels.end(), labels.begin());

    std::vector<std::vector<float>> finalCentroids(params.k, std::vector<float>(params.dims));
    thrust::host_vector<float> h_centroids = d_centroids;
    for (int i = 0; i < params.k; i++) {
        for (int d = 0; d < params.dims; d++) {
            finalCentroids[i][d] = h_centroids[i * params.dims + d];
        }
    }

    return KMeansResult{labels, finalCentroids, iterations, 0.0}; // Time per iteration is calculated in main.cpp
}

