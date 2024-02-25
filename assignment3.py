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
        EPrimeStringArray = re.findall('(\\-?\\d+,\\-?\\d+)', ArrayEPrimetxt)
        EPrimeNumElements = ( ArrayEPrimetxt.count(",") // 2 ) +1
        ArrayEPrime = [[-1 for column in range(2)] for row in range(EPrimeNumElements)]
        for e in range(0, EPrimeNumElements):
            CoordinateE = EPrimeStringArray[e].split(',')
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
    NumTreesInForrest = 0

    # Filling out forrest in edge case where E Prime is empty
    if (EPrimeNumElements == 0):
        for i in range(0, VNumVertices):
            Tree = [ArrayPoints[i]]
            Forrest.insert(i, Tree)
            NumTreesInForrest = NumTreesInForrest + 1
    
    # Filling out forrest in standard case where E Prime is not empty by inserting every connected component from E Prime
    elif (EPrimeNumElements > 0):
        print("ArrayPoints", ArrayPoints)

        # visit each edge in E Prime and update its points' tree values accordingly
        TreeIdentifier = 0
        for i in range(0, EPrimeNumElements):


            CoordinateNumA = ArrayEPrime[i][0] 
            CoordinateNumB = ArrayEPrime[i][1]
            print("CoordinateNumA: ", CoordinateNumA)
            print("CoordinateNumB: ", CoordinateNumB)

            IndexA = ArrayEPrime[i][0] - 1
            IndexB = ArrayEPrime[i][1] - 1
            print("IndexA: ", IndexA)
            print("IndexB: ", IndexB)

            print("ArrayPoints[IndexA]: ", ArrayPoints[IndexA])
            print("ArrayPoints[IndexB]: ", ArrayPoints[IndexB])

            #if neither of the edge's points have been added to a tree, add them to a new tree and remove them from the array of all other points
            if( (ArrayPoints[IndexA][2] == -1) and (ArrayPoints[IndexB][2] == -1) ):
                ArrayPoints[IndexA][2] = TreeIdentifier
                ArrayPoints[IndexB][2] = TreeIdentifier
                Tree = [[ArrayPoints[IndexA]], [ArrayPoints[IndexB]]]
                print("ArrayPoints", ArrayPoints)
                print("ArrayPoints[IndexA]: ", ArrayPoints[IndexA])
                print("ArrayPoints[IndexB]: ", ArrayPoints[IndexB])
                # ArrayPoints.remove([ArrayPoints[IndexA]])
                # ArrayPoints.remove([ArrayPoints[IndexB]])
                Forrest.insert(TreeIdentifier, Tree)
                TreeIdentifier = TreeIdentifier + 1 
                NumTreesInForrest = NumTreesInForrest + 1

            # if the IndexA point has been added to a tree, but the IndexB point has not, add the IndexB point
            # to the IndexA point's tree and remove the IndexB point from the array of all other points
            elif( (ArrayPoints[IndexA][2] != -1) and (ArrayPoints[IndexB][2] == -1) ):
                ArrayPoints[IndexB][2] = ArrayPoints[IndexA][2]
                print("Forrest[ ArrayPoints[IndexA][2] ] ", Forrest[ ArrayPoints[IndexA][2] ])
                Forrest[ ArrayPoints[IndexA][2] ].insert(len(Forrest[ ArrayPoints[IndexA][2] ]), ArrayPoints[IndexB])
                # ArrayPoints.remove([ArrayPoints[IndexB]])

            # if the IndexB point has been added to a tree, but the IndexA point has not, add the IndexA point 
            # to the IndexB point's tree and remove the IndexA point from the array of all other points
            elif( (ArrayPoints[IndexA][2] == -1) and (ArrayPoints[IndexB][2] != -1) ):
                ArrayPoints[IndexA][2] = ArrayPoints[IndexB][2]
                print("Forrest[ ArrayPoints[IndexB][2] ]: ", Forrest[ ArrayPoints[IndexB][2] ])
                Forrest[ ArrayPoints[IndexB][2] ].insert(len(Forrest[ ArrayPoints[IndexB][2] ]), ArrayPoints[IndexA])
                # ArrayPoints.remove([ArrayPoints[IndexA]])

            #if the both of the edge's points have been added to different trees, merge the trees.
            elif( ((ArrayPoints[IndexA][2] != -1) and (ArrayPoints[IndexB][2] != -1) ) and (ArrayPoints[IndexA][2] != ArrayPoints[IndexB][2]) ):
                #keeping IndexA's TreeIdentifer, adding IndexB to IndexA's tree, removing IndexB from its own tree
                ArrayPoints[IndexB][2] = ArrayPoints[IndexA][2]
                Forrest[ ArrayPoints[IndexA][2] ].insert(len(Forrest[ ArrayPoints[IndexA][2] ]), ArrayPoints[IndexB])
                Forrest[ ArrayPoints[IndexB][2] ].remove(ArrayPoints[IndexB])

                #adding all element's from IndexB's former tree to IndexA's tree
                while ( len(Forrest[ ArrayPoints[IndexB][2] ]) > 0 ):
                    Forrest[ ArrayPoints[IndexA][2] ].insert(len(Forrest[ ArrayPoints[IndexA][2] ]), [ ArrayPoints[IndexB][2] ][0])
                    Forrest[ ArrayPoints[IndexB][2] ].remove([ ArrayPoints[IndexB][2] ][0])

                #replacing IndexB's former tree with "-1" in the forrest, to signify that a tree no longer exsists at that index
                Forrest[ ArrayPoints[IndexB][2] ] = -1
                NumTreesInForrest = NumTreesInForrest - 1

        # every vertex not reached by E Prime still has a tree identifier value of -1, add each of these not yet reached vertices
        # to the forrest as their own connected components. 
        for i in range(0, len(ArrayPoints)):
            if (ArrayPoints[i][2] == -1):
                Tree = [ArrayPoints[i]]
                Forrest.insert(i, Tree)
                NumTreesInForrest = NumTreesInForrest + 1
            
    # print("ArrayEPrime[0][0]: ", ArrayEPrime[0][0])
    # print("ArrayEPrime[0][1]: ", ArrayEPrime[0][1])
    # print("ArrayPoints[IndexA][2] :", ArrayPoints[ ArrayEPrime[0][0] ][2])
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
    print("NumTreesInForrest: ", NumTreesInForrest)
    for e in range(NumTreesInForrest):
            print("Tree in Forrest: ", Forrest[e])
        

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