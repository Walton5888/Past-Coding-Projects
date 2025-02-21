#include <iostream>
#include <getopt.h>  // For getopt_long and related identifiers
#include "argparse.h"

// Define the long_options array
static struct option long_options[] = {
    {"in", required_argument, NULL, 'i'},
    {"out", required_argument, NULL, 'o'},
    {"n_threads", required_argument, NULL, 'n'},
    {"loops", required_argument, NULL, 'l'},
    {"spin", no_argument, NULL, 's'},
    {0, 0, 0, 0}  // Terminate the array with zeros
};

// Usage function
void usage() {
    std::cout << "Usage:" << std::endl;
    std::cout << "\t--in or -i <file_path>" << std::endl;
    std::cout << "\t--out or -o <file_path>" << std::endl;
    std::cout << "\t--n_threads or -n <num_threads>" << std::endl;
    std::cout << "\t--loops or -l <num_loops>" << std::endl;
    std::cout << "\t[Optional] --spin or -s" << std::endl;
}

// Function to parse arguments
void get_opts(int argc, char **argv, struct options_t *opts) {
    int opt;
    while ((opt = getopt_long(argc, argv, "i:o:n:l:s", long_options, NULL)) != -1) {
        switch (opt) {
            case 'i':
                opts->in_file = optarg;
                break;
            case 'o':
                opts->out_file = optarg;
                break;
            case 'n':
                opts->n_threads = atoi(optarg);
                break;
            case 'l':
                opts->n_loops = atoi(optarg);
                break;
            case 's':
                opts->spin = true;
                break;
            default:
                usage();
                exit(EXIT_FAILURE);
        }
    }
}

