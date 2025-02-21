#!/usr/bin/env python3
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from subprocess import check_output, CalledProcessError, STDOUT
from time import sleep
import numpy as np

# Constants
THREADS = [0] + [i for i in range(2, 34, 2)]
LOOPS = [1, 10, 100000]
INPUTS = ["seq_64_test.txt", "1k.txt", "8k.txt", "16k.txt"]
USE_SPIN_BARRIER = True
OUTPUT_CSV = "results.csv"
NUM_TRIALS = 3  # Reduced number of trials for large workloads
MIN_TIME = 1  # Minimum time in microseconds to avoid zero values

# List to store test results
csvs = []

def run_command(cmd):
    """Run the command and return the execution time, applying a minimum time threshold."""
    try:
        print(f"Running command: {cmd}")  # Debug print
        out = check_output(cmd, shell=True, stderr=STDOUT).decode("ascii")
        print(f"Output: {out}")  # Debug print
        m = re.search(r"time:\s*(\d+)", out)
        if m:
            time = int(m.group(1))
            return max(time, MIN_TIME)  # Ensure no time is below MIN_TIME
        else:
            print(f"No time found in output for command: {cmd}")
            return None
    except CalledProcessError as e:
        print(f"Error running command '{cmd}': {e.output.decode('ascii')}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def measure_time(cmd, trials=1):
    """Run the command multiple times and return the average execution time."""
    times = []
    for _ in range(trials):
        time = run_command(cmd)
        if time is not None:
            times.append(time)
        sleep(0.1)  # Shorter pause for trials
    return int(np.mean(times)) if times else None

# Running the tests and collecting data
for inp in INPUTS:
    for loop in LOOPS:
        csv = ["{}/{}".format(inp, loop)]  # Record the current test configuration (input file and loop count)
        for thr in THREADS:
            cmd = f"./bin/prefix_scan -o temp.txt -n {thr} -i tests/{inp} -l {loop}"
            if USE_SPIN_BARRIER:
                cmd += " -s"

            # Determine number of trials based on workload size
            trials = NUM_TRIALS if loop <= 10 or thr == 0 else 1

            # Measure time and append results
            time = measure_time(cmd, trials=trials)
            if time is not None:
                csv.append(str(time))
            else:
                csv.append("Error")

        csvs.append(csv)

# Save the results to a CSV file
header = ["Input/Loops"] + [str(x) for x in THREADS]
with open(OUTPUT_CSV, 'w') as f:
    f.write(", ".join(header) + "\n")
    for csv in csvs:
        f.write(", ".join(csv) + "\n")

print(f"\nResults written to {OUTPUT_CSV}")

# ----- Graphing Section -----
def plot_execution_time(csv_file):
    """Plot execution time vs number of threads for each input/loop count combination."""
    data = pd.read_csv(csv_file)
    for index, row in data.iterrows():
        input_loop = row['Input/Loops']
        times = row[1:].astype(float)  # Convert times to float for plotting
        plt.figure(figsize=(10, 6))
        plt.plot(THREADS, times, marker='o', label=input_loop)

        plt.title(f"Execution Time vs Number of Threads for {input_loop}")
        plt.xlabel("Number of Threads")
        plt.ylabel("Execution Time (microseconds)")
        plt.legend()
        plt.grid(True)

        plt.savefig(f"plot_{input_loop.replace('/', '_')}.png")
        plt.close()

def plot_speedup(csv_file):
    """Plot speedup vs number of threads for each input/loop count combination."""
    data = pd.read_csv(csv_file)
    for index, row in data.iterrows():
        input_loop = row['Input/Loops']
        times = row[1:].astype(float)  # Convert times to float for plotting

        baseline = times.iloc[0]
        if baseline <= MIN_TIME or np.isnan(baseline):
            print(f"Skipping speedup plot for {input_loop} due to no valid baseline.")
            continue

        speedup = baseline / times
        plt.figure(figsize=(10, 6))
        plt.plot(THREADS, speedup, marker='o', label=f"Speedup for {input_loop}")

        plt.title(f"Speedup vs Number of Threads for {input_loop}")
        plt.xlabel("Number of Threads")
        plt.ylabel("Speedup")
        plt.legend()
        plt.grid(True)

        plt.savefig(f"speedup_{input_loop.replace('/', '_')}.png")
        plt.close()

# Generate and save the graphs
plot_execution_time(OUTPUT_CSV)
plot_speedup(OUTPUT_CSV)
print("Graphs saved as PNG files.")
