"""
[INPUT] - TESTED
    1. input file
        - test if the file got read
    2. access array
        - test if array is correctly accessed
    3. store data in the array
        - test data is correctly stored

[OUTPUT] - NOT tested
    1. access array
    2. traverse & write a new manifestOUTBOUND.txt
"""

import sys
from ship import Ship
from container import Container

# INPUT, tested 
def INPUT_manifest(input_file):
    ship = Ship()

    #READ
    try: 
        with open(input_file, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    
    for line in lines:
        try:
            # parse the parts [x,y], {lbs}, name. Also check if valid manifest
            parts = line.strip().split(", ")
            if len(parts) != 3: # no 3 parts must be wrong
                raise ValueError(f"Invalid manifest, check line {line}")
            
            coordinates = parts[0].strip("[]").split(",")
            y, x = int(coordinates[0]) - 1, int(coordinates[1]) - 1 # WATCHOUT, zero-based array

            weight = int(parts[1].strip("{}"))
            name = parts[2]

            # CASE MANAGEMENT: for name, UNUSED, NAN
            if name == "UNUSED":
                ship.grid[y][x] = "Place" # placeholder, meaning can put stuffs
            elif name == "NAN":
                ship.grid[y][x] = "NAN" # permanetly unusale
            else:
                container = Container(weight = weight, name = name)
                ship.place_container(y, x, container)

        except ValueError as val:
            print(f"Error processing line '{line.strip()}': {val}")
        except Exception as esc:
            print(f"Error processing line '{line.strip()}': {esc}")
            continue

    return ship


# OUTPUT, YET TO BE test

def OUTPUT_manifest(ship, input_manifest):
    # apply OUTBOUND
    if '.' in input_manifest:
        original_name, ext = input_manifest.rsplit('.', 1)
        output_manifest = f"{original_name}OUTBOUND.{ext}"
    else:
        output_manifest = f"{input_manifest}OUTBOUND"

    try:
        with open(output_manifest, 'w') as file:
            for container in ship.get_ALLcontainerS(): # updated for container compatibility
                file.write(f"[{container.y + 1}, {container.x + 1}], {{{container.weight}}}, {container.name}\n")
        print(f"Output written to '{output_manifest}' successfully.")
    except Exception as esc:
        print(f"Error writting output file: {esc}")
        sys.exit(1)