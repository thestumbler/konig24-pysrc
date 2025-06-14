#!/usr/bin/env python

import numpy as np

def generate_sine_lut(num_rows, f0, f1, f2, f3):
    """
    Generates a lookup table of sine waves in 4 columns with different frequencies.
    Returns: 2D NumPy array of shape (num_rows, 4), dtype=uint16
    """
    x = np.arange(num_rows)
    table = np.zeros((num_rows, 4), dtype=np.uint16)

    for i, f in enumerate([f0, f1, f2, f3]):
        radians = 2 * np.pi * f * x / num_rows
        sine_wave = 0.5 * (1 + np.sin(radians)) * 65535
        table[:, i] = sine_wave.astype(np.uint16)

    return table


def write_header_file(filename, table, var_name="sine_table"):
    """
    Writes the sine table to a C header file as a static constexpr uint16_t array in hex format.
    """
    num_rows, num_cols = table.shape

    with open(filename, 'w') as f:
        f.write("#pragma once\n\n")
        f.write("#include <stdint.h>\n\n")
        f.write("namespace lut {\n\n")
        f.write(f"static constexpr uint16_t {var_name}[{num_rows}][{num_cols}] = {{\n")

        for row in table:
            row_str = ", ".join(f"0x{v:04X}" for v in row)
            f.write(f"    {{ {row_str} }},\n")

        f.write("};\n\n} // namespace lut\n")


if __name__ == "__main__":
    num_rows = 2000
    table = generate_sine_lut(num_rows, 1, 2, 3, 4)
    write_header_file("sine_lut.h", table)
    print("Header file 'sine_lut.h' written.")
