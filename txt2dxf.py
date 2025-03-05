#!/usr/bin/env python


import ezdxf
import math

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
            elif shape == "square" and len(parts) == 5:
                x, y, size, corner_radius = map(float, parts[1:])
                shapes.append(("square", x, y, size, corner_radius))
    return shapes

def generate_dxf(shapes, output_file="output.dxf"):
    doc = ezdxf.new()
    msp = doc.modelspace()

    for shape in shapes:
        if shape[0] == "circle":
            _, x, y, radius = shape
            msp.add_circle(center=(x, y), radius=radius)

        elif shape[0] == "square":
            _, x, y, size, corner_radius = shape
            half = size / 2
            cr = min(corner_radius, half)  # Ensure radius is not larger than half the square size

            # Define the 4 corner centers for the fillets
            corners = [
                (x + half - cr, y + half - cr),  # Top-right
                (x - half + cr, y + half - cr),  # Top-left
                (x - half + cr, y - half + cr),  # Bottom-left
                (x + half - cr, y - half + cr),  # Bottom-right
            ]

            # Define the 4 straight edge segments
            edges = [
                ((x - half + cr, y + half), (x + half - cr, y + half)),  # Top
                ((x - half, y + half - cr), (x - half, y - half + cr)),  # Left
                ((x - half + cr, y - half), (x + half - cr, y - half)),  # Bottom
                ((x + half, y - half + cr), (x + half, y + half - cr)),  # Right
            ]

            # Draw straight edges
            for start, end in edges:
                msp.add_line(start, end)

            # Draw fillet arcs
            for i, center in enumerate(corners):
                start_angle = i * 90
                end_angle = start_angle + 90
                msp.add_arc(center=center, radius=cr, start_angle=start_angle, end_angle=end_angle)

    doc.saveas(output_file)
    print(f"DXF file '{output_file}' created successfully!")

if __name__ == "__main__":
    input_file = "shapes.txt"  # Change this to your input file
    shapes = read_shapes_from_file(input_file)
    generate_dxf(shapes, "output.dxf")
