#include "spin_barrier.h"
#include <atomic>  // Use atomic_flag for spinlock

// Constructor: Initialize the barrier with the number of threads
spin_barrier::spin_barrier(int num_threads)
    : count(0), total_threads(num_threads), generation(0) {
    // Initialize the atomic flag for spinlock
    lock.clear();  // Clear the atomic flag (set to false)
}

// wait() method: This is where the threads will wait at the barrier
void spin_barrier::wait() {
    while (lock.test_and_set(std::memory_order_acquire));  // Acquire the lock (spin until lock is available)

    int current_generation = generation;  // Save the current generation to compare later
    count++;  // Increment the count of threads that have reached the barrier

    // If all threads have reached the barrier, reset the counter and signal the next generation
    if (count == total_threads) {
        count = 0;               // Reset the count for the next round of barrier
        generation++;            // Increment the generation to release waiting threads
        lock.clear(std::memory_order_release);  // Release the spinlock before releasing all threads
    } else {
        lock.clear(std::memory_order_release);  // Release the spinlock to allow other threads to progress

        // Busy-wait (spin) until the generation changes, meaning all threads have reached the barrier
        while (generation == current_generation) {
            // Spinning here: Threads are waiting for other threads to reach the barrier
        }
    }
}

// Destructor: Nothing to destroy here since we used std::atomic_flag
spin_barrier::~spin_barrier() {
    // No explicit destruction needed for std::atomic_flag
}




