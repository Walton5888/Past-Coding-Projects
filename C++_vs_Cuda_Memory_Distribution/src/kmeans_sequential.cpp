#include "kmeans.h"
#include <cmath>
#include <algorithm>
#include <chrono>
#include <random>
#include <limits>
#include <stdexcept>

// Custom random number generator
static unsigned long int next = 1;
static unsigned long kmeans_rmax = 32767;

int kmeans_rand() {
    next = next * 1103515245 + 12345;
    return (unsigned int)(next/65536) % (kmeans_rmax+1);
}

void kmeans_srand(unsigned int seed) {
    next = seed;
}

std::vector<std::vector<float>> initializeCentroids(const std::vector<float>& points, int k, int dims, uint32_t seed) {
    kmeans_srand(seed);
    std::vector<std::vector<float>> centroids(k, std::vector<float>(dims));
    int numPoints = points.size() / dims;
    
    for (int i = 0; i < k; i++) {
        int index = kmeans_rand() % numPoints;
        for (int d = 0; d < dims; d++) {
            centroids[i][d] = points[index * dims + d];
        }
    }
    
    return centroids;
}

float calculateDistance(const float* a, const float* b, int dims) {
    float sum = 0.0f;
    for (int d = 0; d < dims; d++) {
        float diff = a[d] - b[d];
        sum += diff * diff;
    }
    return std::sqrt(sum);
}

bool hasConverged(const std::vector<std::vector<float>>& oldCentroids, 
                  const std::vector<std::vector<float>>& newCentroids, 
                  double threshold) {
    for (size_t i = 0; i < oldCentroids.size(); i++) {
        if (calculateDistance(oldCentroids[i].data(), newCentroids[i].data(), oldCentroids[i].size()) > threshold) {
            return false;
        }
    }
    return true;
}

KMeansResult runSequentialKMeans(const std::vector<float>& points, const KMeansParams& params) {
    int numPoints = points.size() / params.dims;
    
    if (numPoints == 0) {
        throw std::runtime_error("No points to cluster");
    }
    
    if (params.k <= 0 || params.k > numPoints) {
        throw std::runtime_error("Invalid number of clusters");
    }
    
    auto centroids = initializeCentroids(points, params.k, params.dims, params.seed);
    std::vector<int> labels(numPoints);
    std::vector<int> clusterSizes(params.k);
    std::vector<std::vector<float>> newCentroids(params.k, std::vector<float>(params.dims));
    
    int iterations = 0;
    double totalTime = 0.0;
    
    while (iterations < params.maxIterations) {
        auto start = std::chrono::high_resolution_clock::now();
        
        // Assign points to nearest centroid
        for (int i = 0; i < numPoints; i++) {
            float minDist = std::numeric_limits<float>::max();
            int nearestCentroid = 0;
            for (int j = 0; j < params.k; j++) {
                float dist = calculateDistance(&points[i * params.dims], centroids[j].data(), params.dims);
                if (dist < minDist) {
                    minDist = dist;
                    nearestCentroid = j;
                }
            }
            labels[i] = nearestCentroid;
        }
        
        // Update centroids
        std::fill(clusterSizes.begin(), clusterSizes.end(), 0);
        for (auto& centroid : newCentroids) {
            std::fill(centroid.begin(), centroid.end(), 0.0f);
        }
        
        for (int i = 0; i < numPoints; i++) {
            int cluster = labels[i];
            clusterSizes[cluster]++;
            for (int d = 0; d < params.dims; d++) {
                newCentroids[cluster][d] += points[i * params.dims + d];
            }
        }
        
        bool emptyClusters = false;
        for (int j = 0; j < params.k; j++) {
            if (clusterSizes[j] > 0) {
                for (int d = 0; d < params.dims; d++) {
                    newCentroids[j][d] /= clusterSizes[j];
                }
            } else {
                emptyClusters = true;
                // Reinitialize empty clusters
                int index = kmeans_rand() % numPoints;
                for (int d = 0; d < params.dims; d++) {
                    newCentroids[j][d] = points[index * params.dims + d];
                }
            }
        }
        
        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double, std::milli> elapsed = end - start;
        totalTime += elapsed.count();
        
        // Check for convergence
        if (!emptyClusters && hasConverged(centroids, newCentroids, params.threshold)) {
            break;
        }
        
        centroids = newCentroids;
        iterations++;
    }
    
    return KMeansResult{labels, centroids, iterations, totalTime / iterations};
}