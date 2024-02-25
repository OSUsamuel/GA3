import math
import re
import sys
from bisect import bisect_left

def minimum_cost_connecting_edges(input_file_path, output_file_path):
    
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
    # the two numbers of each coordinate, and another coolum to denote if 
    # which connected component it is part of - if any.
    PointStringArray = re.findall('(\\-?\\d+,\\-?\\d+)', ArrayPointstxt)
    VNumVertices = ( ArrayPointstxt.count(",") // 2 ) + 1
    ArrayPoints = [[-1 for column in range(3)] for row in range(VNumVertices)]
    for p in range(0, VNumVertices):
        CoordinateP = PointStringArray[p].split(',')
        ArrayPoints[p][0]= int(CoordinateP[0])
        ArrayPoints[p][1]= int(CoordinateP[1])

    if (line2 == "none"):
        EPrimeNumElements = 0

        ArrayEPrime = [[-1 for column in range(2)] for row in range(0)]
    else:
        # taking a string containing E prime edge data and storing it in    
        # a matrix representation of array E Prime, with one collum for each
        # of the two index numbers of each coordinate
        QStringArray = re.findall('(\\-?\\d+,\\-?\\d+)', ArrayEPrimetxt)
        EPrimeNumElements = ( ArrayEPrimetxt.count(",") // 2 ) +1
        ArrayEPrime = [[-1 for column in range(2)] for row in range(EPrimeNumElements)]
        for e in range(0, EPrimeNumElements):
            CoordinateE = QStringArray[e].split(',')
            ArrayEPrime[e][0]= int(CoordinateE[0])
            ArrayEPrime[e][1]= int(CoordinateE[1])
    
    #Creating Class Edge to encapsulate each possible edge's coordinate and weight 
    class Edge: 
        def __init__(self, CoordinateA, CoordinateB, Weight): 
           self.CoordinateA = CoordinateA
           self.CoordinateB = CoordinateB
           self.Weight = Weight

    # Calculating number of edges using know number of vertices
    ENumElements = (VNumVertices * (VNumVertices - 1)) // 2

    # Creating an array of Edges, filling in coordinate and weight data for each edge. O(E)
    Edges = [-1 for element in range(ENumElements)]
    i = 0
    for x in range(0, VNumVertices):
        for y in range((x+1), VNumVertices):
            Edges[i]= Edge( ArrayPoints[x], ArrayPoints[y], math.dist(ArrayPoints[x], ArrayPoints[y]))
            i = i + 1

    # Creating a sorted array of Edges with our exsisting array of Edges. O(ElogE)
    SortedEdgeWeights = [Edges[0].Weight]
    SortedEdges = [Edges[0]]
    for i in range(1, ENumElements):
        SortedEdgeWeights.insert(bisect_left(SortedEdgeWeights, Edges[i].Weight), Edges[i].Weight)
        SortedEdges.insert(bisect_left(SortedEdgeWeights, Edges[i].Weight), Edges[i])

    # Creating a container to store connected components of our graph.
    Forrest = []

    # Filling out forrest in edge case where E Prime is empty
    if (EPrimeNumElements == 0):
        for i in range(0, VNumVertices):
            Tree = [ArrayPoints[i]]
            Forrest.insert(Tree)

    # Filling out forrest in standard case where E Prime is not empty by inserting every connected component from E Prime
    elif (EPrimeNumElements > 0):
        # base case. adding the two vertices from the first edge of E Prime to a new tree
        IndexA = ArrayEPrime[0][0] 
        IndexB = ArrayEPrime[0][1]
        ArrayPoints[IndexA][2] = 1
        ArrayPoints[IndexB][2] = 1
        Tree = [ArrayPoints[IndexA]], [ArrayPoints[IndexB]]
        Forrest.insert(Tree)

        # visit each edge in E Prime and update its points' tree values accordingly
        TreeIdentifier = 1
        for i in range(1, EPrimeNumElements):
            IndexA = ArrayEPrime[i][0] 
            IndexB = ArrayEPrime[i][1]
            #if neither of the edge's points have been added to a tree, add them to a new tree
            if( (ArrayPoints[IndexA][2] == -1) and (ArrayPoints[IndexB][2] == -1) )
                ArrayPoints[IndexA][2] = TreeIdentifier
                ArrayPoints[IndexB][2] = TreeIdentifier
                TreeIdentifier = TreeIdentifier + 1 
            #if the IndexA point has been added to a tree, but the other point has not, add other point to the IndexA point's tree
            elif( (ArrayPoints[IndexA][2] == -1) and (ArrayPoints[IndexB][2] != -1) )
                ArrayPoints[IndexA][2] = ArrayPoints[IndexB][2]
            #if the IndexB point has been added to a tree, but the other point has not, add other point to the IndexB point's tree
            elif( (ArrayPoints[IndexA][2] != -1) and (ArrayPoints[IndexB][2] == -1) )
                ArrayPoints[IndexB][2] = ArrayPoints[IndexA][2]
            elif( ((ArrayPoints[IndexA][2] != -1) and (ArrayPoints[IndexB][2] != -1) ) and (ArrayPoints[IndexA][2] != ArrayPoints[IndexB][2]) ):


        #adding every vertex not reached by E Prime as its own connected component

    print("ArrayEPrime[0][0]: ", ArrayEPrime[0][0])
    print("ArrayEPrime[0][1]: ", ArrayEPrime[0][1])
    print("ArrayPoints[IndexA][2] :", ArrayPoints[ ArrayEPrime[0][0] ][2])
    print("VNumVertices", VNumVertices)
    print("EPrimeNumElements", EPrimeNumElements)
    print("ArrayPoints", ArrayPoints)
    print("ArrayEPrime", ArrayEPrime)
    # print("EdgeWeights", EdgeWeights)
    print("ENumElements", ENumElements)
    print("Length of Sorted Edges Array: ", len(SortedEdges))
    for e in range(ENumElements):
        print("Edge CoordinateA: [", Edges[e].CoordinateA, "]  |  Edge CoordinateB: [", Edges[e].CoordinateB, "]  | Edge Weight: ", Edges[e].Weight)
    print("Sorted Edge Weights", SortedEdgeWeights)
    for e in range(ENumElements):
        print("Sorted --- Edge CoordinateA: [", SortedEdges[e].CoordinateA, "]  |  Edge CoordinateB: [", SortedEdges[e].CoordinateB, "]  | Edge Weight: ", SortedEdges[e].Weight)



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