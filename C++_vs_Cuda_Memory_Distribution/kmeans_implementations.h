// kmeans_implementations.h
#ifndef KMEANS_IMPLEMENTATIONS_H
#define KMEANS_IMPLEMENTATIONS_H

#include "kmeans.h"

KMeansResult runCUDABasicKMeans(const std::vector<float>& points, const KMeansParams& params);
KMeansResult runCUDAShmemKMeans(const std::vector<float>& points, const KMeansParams& params);
KMeansResult runCUDAThrustKMeans(const std::vector<float>& points, const KMeansParams& params);
KMeansResult runSequentialKMeans(const std::vector<float>& points, const KMeansParams& params);

#endif // KMEANS_IMPLEMENTATIONS_H