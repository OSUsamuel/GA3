import math
import re
import sys
import random

# command to use: python3 bigger_input.py test_cases/bigger_input.txt numbervertices numberE'edges
# ex: python3 bigger_input.py test_cases/bigger_input.txt 9 3

def make_bigger_input_file(output_file_path, number_of_vertices, number_E_prime):
    output_file_path = output_file_path.strip()
    number_of_vertices = int(number_of_vertices)
    # print(number_of_vertices)

    Coordinates = set()
    CoordinatesPlusInverse = set()
    CoordinateString = ""

    i = 0
    while i < number_of_vertices-1:
        startlen = len(CoordinatesPlusInverse)
        A = random.randint(0, 500)
        B = random.randint(0, 500)
        NewCoordinate = (A, B)
        CoordinatesPlusInverse.add(NewCoordinate)
        if (len(CoordinatesPlusInverse)>startlen):
            Inverse = (B, A)
            CoordinatesPlusInverse.add(Inverse)
            i+= 1
            # print("New Coordinates: ",A, ",", B)
            CoordinateString = CoordinateString + "("+ str(A) + ", " + str(B) + "),"
            Coordinates.add(Inverse)
    while i < number_of_vertices:
        startlen = len(CoordinatesPlusInverse)
        A = random.randint(0, 500)
        B = random.randint(0, 500)
        NewCoordinate = (A, B)
        CoordinatesPlusInverse.add(NewCoordinate)
        if (len(CoordinatesPlusInverse)>startlen):
            Inverse = (B, A)
            CoordinatesPlusInverse.add(Inverse)
            i+= 1
            # print("New Coordinates: ",A, ",", B)
            CoordinateString = CoordinateString + "("+ str(A) + ", " + str(B) + ")"
            Coordinates.add(Inverse)

    Edges = set()
    EdgesPlusInverse = set()

    EPrimetxt = ""
    number_E_prime = int(number_E_prime)
    if (number_E_prime == 0):
         EPrimetxt = "none"
    else:
        j = 0
        while j < number_E_prime-1:
            startlen = len(EdgesPlusInverse)
            A = random.randint(0, number_of_vertices-1)
            B = random.randint(0, number_of_vertices-1)
            NewEdge = (A, B)
            EdgesPlusInverse.add(NewEdge)
            if (len(EdgesPlusInverse)>startlen):
                Inverse = (B, A)
                EdgesPlusInverse.add(Inverse)
                j+= 1
                # print("New Edge: ",A, ",", B)
                EPrimetxt = EPrimetxt + "("+ str(A) + ", " + str(B) + "),"
        while j < number_E_prime:
            startlen = len(EdgesPlusInverse)
            A = random.randint(0, number_of_vertices-1)
            B = random.randint(0, number_of_vertices-1)
            NewEdge = (A, B)
            EdgesPlusInverse.add(NewEdge)
            if (len(EdgesPlusInverse)>startlen):
                Inverse = (B, A)
                EdgesPlusInverse.add(Inverse)
                j+= 1
                # print("New Edge: ",A, ",", B)
                EPrimetxt = EPrimetxt + "("+ str(A) + ", " + str(B) + ")"
            
        # print(EPrimetxt)
         
    # print("CoordinateString: ", CoordinateString)

    with open(output_file_path, 'w') as output_file:
        output_file.write(f"{CoordinateString}\n")
        output_file.write(f"{EPrimetxt}\n")
    
    return

if len(sys.argv) != 4:
    print("Usage: python script.py output_file_path number_of_vertices number_E_prime)")
else:
    output_file_path = sys.argv[1]
    number_of_vertices = sys.argv[2]
    number_E_prime = sys.argv[3]
    print(make_bigger_input_file(output_file_path, number_of_vertices, number_E_prime))