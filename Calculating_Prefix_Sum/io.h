#ifndef _IO_H
#define _IO_H

#include "argparse.h"  // Include the header where options_t is defined
#include "prefix_sum.h"  // Include the header where prefix_sum_args_t is defined
#include <iostream>  // Include iostream for std::cerr
#include <fstream>   // Include fstream for file operations

// Function declarations
void read_file(struct options_t* args,
               int*              n_vals,
               int**             input_vals,
               int**             output_vals);

void write_file(struct options_t*         args,
                struct prefix_sum_args_t* opts);

#endif  // _IO_H

