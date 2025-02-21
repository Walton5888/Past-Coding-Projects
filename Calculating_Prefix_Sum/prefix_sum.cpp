#include "prefix_sum.h"
#include "helpers.h"
#include <cstring>  // For strerror

// Function to compute the prefix sum
void* compute_prefix_sum(void* a) {
    prefix_sum_args_t* args = (prefix_sum_args_t*)a;

    int start = args->t_id * (args->n_vals / args->n_threads);
    int end = (args->t_id + 1) * (args->n_vals / args->n_threads);

    if (args->t_id == args->n_threads - 1) {
        end = args->n_vals;  // Ensure the last thread processes any remaining values
    }

    // Up-sweep (local prefix sum calculation)
    for (int i = start; i < end; ++i) {
        if (i == start) {
            args->output_vals[i] = args->input_vals[i];
        } else {
            args->output_vals[i] = args->op(args->output_vals[i - 1], args->input_vals[i], args->n_loops);
        }
    }

    // Synchronize all threads after up-sweep
    if (args->spin) {
        args->spin_barrier->wait();
    } else {
        #ifdef _POSIX_BARRIERS
        pthread_barrier_wait(&(args->pthread_barrier));
        #else
        args->spin_barrier->wait();  // Fallback to spin barrier
        #endif
    }

    // Down-sweep (adjust local prefix sums based on previous thread)
    if (args->t_id > 0) {
        int adjustment = args->output_vals[start - 1];

        for (int i = start; i < end; ++i) {
            args->output_vals[i] = args->op(adjustment, args->output_vals[i], args->n_loops);
        }
    }

    // Synchronize all threads after down-sweep
    if (args->spin) {
        args->spin_barrier->wait();
    } else {
        #ifdef _POSIX_BARRIERS
        pthread_barrier_wait(&(args->pthread_barrier));
        #else
        args->spin_barrier->wait();  // Fallback to spin barrier
        #endif
    }

    return NULL;
}