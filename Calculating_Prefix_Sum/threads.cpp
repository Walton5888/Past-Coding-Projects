#include "threads.h"
#include <cstring>  // For strerror

pthread_t* alloc_threads(int n_threads) {
    return (pthread_t*)malloc(n_threads * sizeof(pthread_t));
}

void start_threads(pthread_t *threads, int n_threads, struct prefix_sum_args_t *args, void *(*start_routine)(void *)) {
    int ret = 0;
    for (int i = 0; i < n_threads; ++i) {
        ret = pthread_create(&(threads[i]), NULL, start_routine, (void *)&(args[i]));
        if (ret != 0) {
            std::cerr << "Error starting thread " << i << ": " << strerror(ret) << std::endl;
        }
    }

    if (ret) {
        std::cerr << "Error starting threads" << std::endl;
        exit(1);
    }
}

void join_threads(pthread_t* threads, int n_threads) {
    int res = 0;
    for (int i = 0; i < n_threads; ++i) {
        int ret = pthread_join(threads[i], NULL);
        if (ret) {
            std::cerr << "Error joining thread " << i << ": " << strerror(ret) << std::endl;
            res = 1;  // Set the result flag if any join fails
        }
    }

    if (res) {
        std::cerr << "One or more threads failed to join." << std::endl;
        exit(1);
    }
}



