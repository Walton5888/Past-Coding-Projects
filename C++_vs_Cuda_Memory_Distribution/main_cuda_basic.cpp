#include "kmeans.h"
#include "kmeans_implementations.h"
#include <iostream>
#include <chrono>
#include <stdexcept>

KMeansParams parseCommandLine(int argc, char** argv, std::string& implementation) {
    KMeansParams params;
    implementation = "sequential";  // Default implementation

    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];

        if (arg == "-k" && i + 1 < argc) {
            params.k = std::stoi(argv[++i]);
        } else if (arg == "-d" && i + 1 < argc) {
            params.dims = std::stoi(argv[++i]);
        } else if (arg == "-i" && i + 1 < argc) {
            params.inputFile = argv[++i];
        } else if (arg == "-m" && i + 1 < argc) {
            params.maxIterations = std::stoi(argv[++i]);
        } else if (arg == "-t" && i + 1 < argc) {
            params.threshold = std::stod(argv[++i]);
        } else if (arg == "-c") {
            params.outputCentroids = true;
        } else if (arg == "-s" && i + 1 < argc) {
            params.seed = std::stoul(argv[++i]);
        } else if (arg == "-impl" && i + 1 < argc) {
            implementation = argv[++i];
        } else {
            std::cerr << "Unknown or incomplete argument: " << arg << std::endl;
            throw std::invalid_argument("Invalid command-line arguments");
        }
    }
    // Add this closing brace to properly end the parseCommandLine function
    return params;
}  // <-- Added missing closing brace here

int main(int argc, char** argv) {
    try {
        std::string implementation;
        KMeansParams params = parseCommandLine(argc, argv, implementation);

        int numPoints, numDims;
        std::vector<float> points = readInputFile(params.inputFile, numPoints, numDims);

        if (numDims != params.dims) {
            throw std::runtime_error("Mismatch between specified dimensions (" + std::to_string(params.dims) +
                                     ") and input file dimensions (" + std::to_string(numDims) + ")");
        }

        auto start = std::chrono::high_resolution_clock::now();
        KMeansResult result = runCUDABasicKMeans(points, params);
        auto end = std::chrono::high_resolution_clock::now();

        result.timePerIteration = std::chrono::duration<float, std::milli>(end - start).count() / result.iterations;
        writeOutput(result, params, "CUDA Basic KMeans");

    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    } catch (...) {
        std::cerr << "Unknown error occurred" << std::endl;
        return 1;
    }
    return 0;
}
