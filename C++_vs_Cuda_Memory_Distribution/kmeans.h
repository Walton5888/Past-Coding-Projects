#ifndef KMEANS_H
#define KMEANS_H

#include <vector>
#include <string>

struct KMeansParams {
    int k = 0;
    int dims = 0;
    int maxIterations = 100;
    double threshold = 0.001;
    std::string inputFile;
    bool outputCentroids = false;
    unsigned long seed = 0;
};

struct KMeansResult {
    std::vector<int> labels;
    std::vector<std::vector<float>> centroids;
    int iterations;
    double timePerIteration;
};

// Sequential K-means functions
std::vector<std::vector<float>> initializeCentroids(const std::vector<float>& points, int k, int dims, uint32_t seed);
float calculateDistance(const float* a, const float* b, int dims);
bool hasConverged(const std::vector<std::vector<float>>& oldCentroids, 
                  const std::vector<std::vector<float>>& newCentroids, 
                  double threshold);
KMeansResult runSequentialKMeans(const std::vector<float>& points, const KMeansParams& params);

// CUDA Basic K-means function
KMeansResult runCUDABasicKMeans(const std::vector<float>& points, const KMeansParams& params);

// CUDA Shared Memory K-means function
KMeansResult runCUDAShmemKMeans(const std::vector<float>& points, const KMeansParams& params);

// Thrust K-means function
KMeansResult runThrustKMeans(const std::vector<float>& points, const KMeansParams& params);

// Utility functions
KMeansParams parseCommandLine(int argc, char** argv);
std::vector<float> readInputFile(const std::string& filename, int& numPoints, int& numDims);
void writeOutput(const KMeansResult& result, const KMeansParams& params, const std::string& implementation);

#endif // KMEANS_H