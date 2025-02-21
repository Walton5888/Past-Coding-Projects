// prefix_sum.h
#ifndef _PREFIX_SUM_H
#define _PREFIX_SUM_H

// Include necessary headers
#include <pthread.h>  // For pthread_t, pthread functions

// Define the prefix_sum_args_t structure
struct prefix_sum_args_t {
    int* input_vals;        // Pointer to input values array
    int* output_vals;       // Pointer to output values array
    bool spin;              // Flag to indicate use of spin lock
    int n_vals;             // Number of values to process
    int n_threads;          // Number of threads
    int t_id;               // Thread ID
    int (*op)(int, int, int); // Operator function for prefix sum
    int n_loops;            // Number of loops for prefix sum computation
    spin_barrier* spin_barrier; // Pointer to spin barrier (custom barrier)
};

// Function prototype for prefix sum computation
void* compute_prefix_sum(void* args);

#endif // _PREFIX_SUM_H
