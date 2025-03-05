#!/usr/bin/env python

import ezdxf

def read_shapes_from_file(filename):
    shapes = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("#") or not line:  # Ignore comments and empty lines
                continue
            parts = line.split(",")
            shape = parts[0].strip().lower()
            if shape == "circle" and len(parts) == 4:
                x, y, radius = map(float, parts[1:])
                shapes.append(("circle", x, y, radius))
            elif shape == "square" and len(parts) == 4:
                x, y, size = map(float, parts[1:])
                shapes.append(("square", x, y, size))
    return shapes

def generate_dxf(shapes, output_file="output.dxf"):
    doc = ezdxf.new()
    msp = doc.modelspace()

    for shape in shapes:
        if shape[0] == "circle":
            _, x, y, radius = shape
            msp.add_circle(center=(x, y), radius=radius)
        elif shape[0] == "square":
            _, x, y, size = shape
            half = size / 2
            msp.add_lwpolyline([(x - half, y - half), 
                                (x + half, y - half), 
                                (x + half, y + half), 
                                (x - half, y + half), 
                                (x - half, y - half)])  # Close the square

    doc.saveas(output_file)
    print(f"DXF file '{output_file}' created successfully!")

if __name__ == "__main__":
    input_file = "shapes.txt"  # Change this to your input file
    shapes = read_shapes_from_file(input_file)
    generate_dxf(shapes, "output.dxf")
