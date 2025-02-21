#ifndef _SPIN_BARRIER_H
#define _SPIN_BARRIER_H

#include <atomic>  // Include atomic for spinlock implementation

class spin_barrier {
private:
    std::atomic_flag lock = ATOMIC_FLAG_INIT;  // Spinlock using atomic_flag
    int count;                // Number of threads that have reached the barrier
    int total_threads;        // Total number of threads
    int generation;           // Used to distinguish between different rounds of barrier use

public:
    // Constructor: Initialize the barrier with the number of threads
    spin_barrier(int num_threads);

    // wait() method: This is where the threads will wait at the barrier
    void wait();

    // Destructor: No need to destroy atomic_flag, so no explicit destructor
    ~spin_barrier();
};

#endif




