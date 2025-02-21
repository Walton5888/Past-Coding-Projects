#include "io.h"

void read_file(struct options_t* args,
               int*              n_vals,
               int**             input_vals,
               int**             output_vals) {
    std::ifstream in(args->in_file);
    if (!in) {
        std::cerr << "Error opening input file: " << args->in_file << std::endl;
        exit(1);
    }

    in >> *n_vals;

    *input_vals = (int*) malloc(*n_vals * sizeof(int));
    *output_vals = (int*) malloc(*n_vals * sizeof(int));

    for (int i = 0; i < *n_vals; ++i) {
        in >> (*input_vals)[i];
    }

    in.close();
}

void write_file(struct options_t*         args,
                struct prefix_sum_args_t* opts) {
    std::ofstream out(args->out_file, std::ofstream::trunc);
    if (!out) {
        std::cerr << "Error opening output file: " << args->out_file << std::endl;
        exit(1);
    }

    for (int i = 0; i < opts->n_vals; ++i) {
        out << opts->output_vals[i] << std::endl;
    }

    out.close();

    free(opts->input_vals);
    free(opts->output_vals);
}



