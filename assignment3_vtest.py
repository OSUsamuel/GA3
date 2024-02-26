import math
import re
import sys
from bisect import bisect_left


def display_edge(EdgeClassObject):
    print("          (Coordinate)(Coordinate)[Weight]: ", EdgeClassObject.CoordinateA, EdgeClassObject.CoordinateB, " [", EdgeClassObject.Weight, "]")

def display_all_edges(EdgeList):
    print("")
    print("_____Edges_______________________________________________________________________________________________ ")
    for e in range(len(EdgeList)):
            display_edge(EdgeList[e])
    print("")

def minimum_cost_connecting_edges(input_file_path, output_file_path):

# STEP 1 : Read the input file, extract coordinate and edge data
    
    with open(input_file_path, 'r') as file:
        # reading input files for coordinate point data in line 1
        line1 = file.readline()
        if line1:
            ArrayPointstxt = " "
            ArrayPointstxt+=line1
            ArrayPointstxt = ArrayPointstxt.strip()

        # reading input files for E prime edge data in line 2
        line2 = file.readline()
        if line2:
            ArrayEPrimetxt = " "
            ArrayEPrimetxt+=line2
            ArrayEPrimetxt = ArrayEPrimetxt.strip()

    # taking a string containing coordinate point data and storing it in    
    # a matrix representation of array Points, with one collum for each of
    # the two numbers of each coordinate
    PointStringArray = re.findall('(\\-?\\d+,\\-?\\d+)', ArrayPointstxt)
    VNumVertices = ( ArrayPointstxt.count(",") // 2 ) + 1
    ArrayPoints = [[-1 for column in range(2)] for row in range(VNumVertices)]
    for p in range(0, VNumVertices):
        CoordinateP = PointStringArray[p].split(',')
        ArrayPoints[p][0]= int(CoordinateP[0])
        ArrayPoints[p][1]= int(CoordinateP[1])

    #Creating Class Edge to encapsulate each possible edge's coordinate and weight 
    class Edge: 
        def __init__(self, CoordinateA, CoordinateB, Weight): 
           self.CoordinateA = CoordinateA
           self.CoordinateB = CoordinateB
           self.Weight = Weight


    if (line2 == "none"):
        EPrimeNumElements = 0
        EPrimeEdges = [[-1 for column in range(3)] for row in range(0)]

    else:
        # taking a string containing E prime edge data and storing it in    
        # an array of edge structures
        EPrimeStringArray = re.findall('(\\-?\\d+,\\-?\\d+)', ArrayEPrimetxt)
        EPrimeNumElements = ( ArrayEPrimetxt.count(",") // 2 ) +1
        EPrimeEdges = [-1 for edge in range(EPrimeNumElements)]

        for e in range(0, EPrimeNumElements):
            CoordinateE = EPrimeStringArray[e].split(',')
            CoordinateAIdx = int(CoordinateE[0])-1
            CoordinateBIdx = int(CoordinateE[1])-1
            # filling in collums for coordinate data
            XCoordinateOfA = ArrayPoints[CoordinateAIdx][0]
            XCoordinateOfB = ArrayPoints[CoordinateBIdx][0]
            YCoordinateOfA = ArrayPoints[CoordinateAIdx][1]
            YCoordinateOfB = ArrayPoints[CoordinateBIdx][1]
            # computing manhattan distance between points to store as weight
            ManhatanDistance = int(math.dist([XCoordinateOfA],[XCoordinateOfB]) + math.dist([YCoordinateOfA],[YCoordinateOfB]))
            # adding edge to array of E Prime Edges
            EPrimeEdges[e]= Edge( ArrayPoints[CoordinateAIdx], ArrayPoints[CoordinateBIdx], ManhatanDistance )


    # Calculating number of possible edges using know number of vertices
    ENumEdges = (VNumVertices * (VNumVertices - 1)) // 2

    # Creating a Sorted array of Edges, filling in coordinate and weight data for each edge. 
    # binary search insert for each edge. building list of weights for biselect functionality. O(ElogE)
    SortedEdgeWeights = []
    SortedEdges = []
    i = 0
    for e in range(0, VNumVertices):
        for f in range((e+1), VNumVertices):
            XCoordinateOfA = ArrayPoints[e][0]
            XCoordinateOfB = ArrayPoints[f][0]
            YCoordinateOfA = ArrayPoints[e][1]
            YCoordinateOfB = ArrayPoints[f][1]
            ManhatanDistance = int(math.dist([XCoordinateOfA],[XCoordinateOfB]) + math.dist([YCoordinateOfA],[YCoordinateOfB]))
            SortedEdgeWeights.insert(bisect_left(SortedEdgeWeights,ManhatanDistance), ManhatanDistance)
            SortedEdges.insert(bisect_left(SortedEdgeWeights,ManhatanDistance), Edge( ArrayPoints[e], ArrayPoints[f], ManhatanDistance ))
            i = i + 1

    # print("len(SortedEdges): ",len(SortedEdges))
    # print("ENumEdges = (VNumVertices * (VNumVertices - 1)) // 2: ", ENumEdges)
    # display_all_edges(SortedEdges)

# End STEP 1.
# We now have an array of coordinates, an array of all edges sorted by weight, and an array of edges from E Prime.
# ArrayPoints, SortedEdges, and EPrimeEdges
            

    
    
    














    result = -1

    with open(output_file_path, 'w') as output_file:
        output_file.write(f"{result}\n")

    return result


if len(sys.argv) != 3:
    print("Usage: python script.py input_file_path output_file_path")
else:
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    print(minimum_cost_connecting_edges(input_file_path, output_file_path))