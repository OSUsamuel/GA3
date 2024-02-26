import math
import re
import sys
from bisect import bisect_left

def display_edge(EdgeClassObject):
    print("          Edge -- (CoordinateA)(CoordinateB)[Weight]: ", EdgeClassObject.CoordinateA, EdgeClassObject.CoordinateB, " [", EdgeClassObject.Weight, "]")


def Kruskals(ArrayPoints, TreeIdentifier, Forrest, NumTreesInForrest, SortedEdges):

    AddedWeight = 0

    while (NumTreesInForrest > 1):
        chosen = 0
        i = 0 
        while (chosen == 0):
            
            CoordinateNumA = SortedEdges[i].CoordinateA
            CoordinateNumB = SortedEdges[i].CoordinateB

            #since the Sorted Edges Array is in ascending order, the first edge that spans separate components will be added to the spanning tree 
            if( (CoordinateNumA[2] < 0) and (CoordinateNumB[2] < 0) ):
                AddedWeight = AddedWeight + SortedEdges[i].Weight
                SortedEdges.remove(SortedEdges[i])
                NumTreesInForrest = NumTreesInForrest -1
                ATreeID = abs(CoordinateNumA[2])
                CoordinateNumA[2] = abs(CoordinateNumB[2])
                CoordinateNumB[2] = abs(CoordinateNumB[2])
                Forrest[CoordinateNumB[2]].insert(0, CoordinateNumA)
                Forrest[ATreeID] = [-1]
                TreeIdentifier = TreeIdentifier + 1 
                chosen = 1
            elif ( CoordinateNumA[2] != CoordinateNumB[2] ):
                AddedWeight = AddedWeight+ SortedEdges[i].Weight
                SortedEdges.remove(SortedEdges[i])
                NumTreesInForrest = NumTreesInForrest -1
                chosen = 1
                #following conditional logic to update tree labels and forrest
                if ( (CoordinateNumA[2] < 0) and  (CoordinateNumB[2] > -1) ):
                    ATreeID = abs(CoordinateNumA[2])
                    CoordinateNumA[2] = CoordinateNumB[2] 
                    Forrest[CoordinateNumB[2]].insert(0, Forrest[ATreeID][0])
                    Forrest[ATreeID]= [-1]
                elif ( (CoordinateNumB[2] < 0) and  (CoordinateNumA[2] > -1)  ):
                    BTreeID = abs(CoordinateNumB[2])
                    CoordinateNumB[2] = CoordinateNumA[2] 
                    Forrest[CoordinateNumA[2]].insert(0, Forrest[BTreeID][0])
                    Forrest[BTreeID]= [-1]
                else:
                    # #keeping IndexA's TreeIdentifer, adding IndexB to IndexA's tree, removing IndexB from its own tree
                    BTreeID = abs(CoordinateNumB[2])

                    # for every element in IndexB's former tree, add to IndexA's tree, update the tree label, and remove from former tree
                    for i in range (len(Forrest[ BTreeID ])):
                        Forrest[ BTreeID ][0][2] = CoordinateNumA[2] 
                        Forrest[ CoordinateNumA[2] ].insert(0, Forrest[ BTreeID ][0])
                        Forrest[ BTreeID ].remove(Forrest[ BTreeID ][0])
                    
                    Forrest[BTreeID]= [-1]
            else:
                i = i + 1

    return AddedWeight
        

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

        ArrayEPrime = [[-1 for column in range(3)] for row in range(0)]
    else:
        # taking a string containing E prime edge data and storing it in    
        # a matrix representation of array E Prime, with one collum for each
        # of the two index numbers of each coordinate
        EPrimeStringArray = re.findall('(\\-?\\d+,\\-?\\d+)', ArrayEPrimetxt)
        EPrimeNumElements = ( ArrayEPrimetxt.count(",") // 2 ) +1
        ArrayEPrime = [[-1 for column in range(3)] for row in range(EPrimeNumElements)]
        for e in range(0, EPrimeNumElements):
            CoordinateE = EPrimeStringArray[e].split(',')
            ArrayEPrime[e][0]= int(CoordinateE[0])
            ArrayEPrime[e][1]= int(CoordinateE[1])
            XCoordinateOfA = ArrayPoints[ArrayEPrime[e][0] - 1][0]
            XCoordinateOfB = ArrayPoints[ArrayEPrime[e][1] - 1][0]
            YCoordinateOfA = ArrayPoints[ArrayEPrime[e][0] - 1][1]
            YCoordinateOfB = ArrayPoints[ArrayEPrime[e][1] - 1][1]
            ManhatanDistance = int(math.dist([XCoordinateOfA],[XCoordinateOfB]) + math.dist([YCoordinateOfA],[YCoordinateOfB]))
            ArrayEPrime[e][2]= ManhatanDistance
    print("ArrayEPrime", ArrayEPrime) 

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
    for e in range(0, VNumVertices):
        for f in range((e+1), VNumVertices):
            XCoordinateOfA = ArrayPoints[e][0]
            XCoordinateOfB = ArrayPoints[f][0]
            YCoordinateOfA = ArrayPoints[e][1]
            YCoordinateOfB = ArrayPoints[f][1]
            ManhatanDistance = int(math.dist([XCoordinateOfA],[XCoordinateOfB]) + math.dist([YCoordinateOfA],[YCoordinateOfB]))
            # math.dist(ArrayPoints[x][0], ArrayPoints[y][0]) + math.dist(ArrayPoints[x][1], ArrayPoints[y][1])
            Edges[i]= Edge( ArrayPoints[e], ArrayPoints[f], ManhatanDistance )
            i = i + 1
    

    # Creating a sorted array of Edges with our exsisting array of Edges. O(ElogE)
    SortedEdgeWeights = [Edges[0].Weight]
    SortedEdges = [Edges[0]]
    for i in range(1, ENumElements):
        SortedEdgeWeights.insert(bisect_left(SortedEdgeWeights, Edges[i].Weight), Edges[i].Weight)
        SortedEdges.insert(bisect_left(SortedEdgeWeights, Edges[i].Weight), Edges[i])

    for e in range(len(SortedEdges)):
        display_edge(SortedEdges[e])
    
    # Creating a container to store connected components of our graph.
    Forrest = []
    NumTreesInForrest = 0

    # Creating a variable to store the running weight of the connected componenets in our forrest
    WeightEPrime = 0

    TreeIdentifier = 0

    # Filling out forrest in edge case where E Prime is empty
    if (EPrimeNumElements == 0):
        for i in range(0, VNumVertices):
            ArrayPoints[i][2] = -1 * TreeIdentifier
            Tree = [ArrayPoints[i]]
            Forrest.insert(i, Tree)
            NumTreesInForrest = NumTreesInForrest + 1
            TreeIdentifier = TreeIdentifier + 1
    
    # Filling out forrest in standard case where E Prime is not empty by inserting every connected component from E Prime
    elif (EPrimeNumElements > 0):

        # visit each edge in E Prime and update its points' tree values accordingly
        for i in range(0, EPrimeNumElements):

            WeightEPrime = WeightEPrime + ArrayEPrime[i][2]
            CoordinateNumA = ArrayEPrime[i][0] 
            CoordinateNumB = ArrayEPrime[i][1]

            #indices in Points Array
            IndexA = ArrayEPrime[i][0] - 1
            IndexB = ArrayEPrime[i][1] - 1

            #if neither of the edge's points have been added to a tree, add them to a new tree
            if( (ArrayPoints[IndexA][2] < 0) and (ArrayPoints[IndexB][2] < 0) ):

                ArrayPoints[IndexA][2] = TreeIdentifier
                ArrayPoints[IndexB][2] = TreeIdentifier
                Tree = []
                Tree.insert(0, ArrayPoints[IndexA])
                Tree.insert(0, ArrayPoints[IndexB])
                Forrest.insert(TreeIdentifier, Tree)
                TreeIdentifier = TreeIdentifier + 1 
                NumTreesInForrest = NumTreesInForrest + 1

            # if the IndexA point has been added to a tree, but the IndexB point has not, add the IndexB point
            # to the IndexA point's tree
            elif( (ArrayPoints[IndexA][2] > -1) and (ArrayPoints[IndexB][2] < 0) ):
                ArrayPoints[IndexB][2] = ArrayPoints[IndexA][2]
                Forrest[ ArrayPoints[IndexA][2] ].insert(len(Forrest[ ArrayPoints[IndexA][2] ]), ArrayPoints[IndexB])

            # if the IndexB point has been added to a tree, but the IndexA point has not, add the IndexA point 
            # to the IndexB point's tree 
            elif( (ArrayPoints[IndexA][2] < 0) and (ArrayPoints[IndexB][2] > -1) ):
                ArrayPoints[IndexA][2] = ArrayPoints[IndexB][2]
                Forrest[ ArrayPoints[IndexB][2] ].insert(len(Forrest[ ArrayPoints[IndexB][2] ]), ArrayPoints[IndexA])

            #if the both of the edge's points have been added to different trees, merge the trees.
            elif( ((ArrayPoints[IndexA][2] != -1) and (ArrayPoints[IndexB][2] != -1) ) and (ArrayPoints[IndexA][2] != ArrayPoints[IndexB][2]) ):

                #keeping IndexA's TreeIdentifer, adding IndexB to IndexA's tree, removing IndexB from its own tree
                BTreeID = ArrayPoints[IndexB][2] 
                ArrayPoints[IndexB][2] = ArrayPoints[IndexA][2]
                Forrest[ ArrayPoints[IndexA][2] ].insert(len(Forrest[ ArrayPoints[IndexA][2] ]), ArrayPoints[IndexB])
                Forrest[ BTreeID ].remove(ArrayPoints[IndexB])

                # for every element in IndexB's former tree, add to IndexA's tree, update the tree label, and remove from former tree
                while ( len(Forrest[ BTreeID ]) > 0 ):
                    Forrest[ BTreeID ][0][2] = ArrayPoints[IndexA][2]
                    Forrest[ ArrayPoints[IndexA][2] ].insert(0, Forrest[ BTreeID ][0])
                    Forrest[ BTreeID ].remove(Forrest[ BTreeID ][0])
                    
                #replacing IndexB's former tree with "-1" in the forrest, to signify that a tree no longer exsists at that index
                Forrest[ BTreeID ] = -1
                NumTreesInForrest = NumTreesInForrest - 1

        # every vertex not reached by E Prime still has a tree identifier value of -1, add each of these not yet reached vertices
        # to the forrest as their own connected components. 
        for i in range(0, len(ArrayPoints)):
            if (ArrayPoints[i][2] == -1):
                ArrayPoints[i][2] = -1 * TreeIdentifier
                Tree = [ArrayPoints[i]]
                Forrest.insert(i, Tree)
                NumTreesInForrest = NumTreesInForrest + 1
                TreeIdentifier = TreeIdentifier + 1
    
    # now we have the connected components from E Prime, and the remaining vertices not reached by E Prime each as their own components
    # from here we can implement Kruskal's Algorithm
    print("Start Kruskals")
    WeightEAsterix= Kruskals(ArrayPoints, TreeIdentifier, Forrest, NumTreesInForrest, SortedEdges)
            
    result = WeightEAsterix

    with open(output_file_path, 'w') as output_file:
        output_file.write(f"{result}\n")

    return result


if len(sys.argv) != 3:
    print("Usage: python script.py input_file_path output_file_path")
else:
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    print(minimum_cost_connecting_edges(input_file_path, output_file_path))