#include "kmeans.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <stdexcept>

// Function to read points from the input file
std::vector<float> readInputFile(const std::string& filename, int& numPoints, int& numDims) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        throw std::runtime_error("Unable to open input file: " + filename);
    }
    std::vector<float> points;
    std::string line;
    numPoints = 0;

    while (std::getline(file, line)) {
        std::istringstream iss(line);
        float value;
        while (iss >> value) {
            points.push_back(value);
        }
        numPoints++;
    }

    if (numPoints == 0) {
        throw std::runtime_error("No points read from input file");
    }
    numDims = points.size() / numPoints;
    return points;
}

// Function to print the output of the KMeans algorithm
void writeOutput(const KMeansResult& result, const KMeansParams& params, const std::string& implementation) {
    std::cout << implementation << ": " << result.iterations << " iterations, "
              << result.timePerIteration << " ms per iteration" << std::endl;

    if (params.outputCentroids) {
        std::cout << "Centroids:" << std::endl;
        for (int i = 0; i < params.k; i++) {
            std::cout << "Centroid " << i << ": ";
            for (int d = 0; d < params.dims; d++) {
                std::cout << result.centroids[i][d] << " ";
            }
            std::cout << std::endl;
        }
    } else {
        std::cout << "Cluster labels:" << std::endl;
        for (int label : result.labels) {
            std::cout << label << " ";
        }
        std::cout << std::endl;
    }
}
