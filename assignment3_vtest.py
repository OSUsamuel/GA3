import math
import re
import sys
from bisect import bisect_left


"""
This file is a version of the Python deliverable for our GA3 submission, this version has print statement
so that you may see a visual representation of the algorithm's mechanisms printed to the terminal.

How to use for visual representation:
    Run the code directly in the terminal with the following command, where input_file.txt is the actual
    name of your input file and output_file.txt is the actual name of your output file.
    ** Please note that this command may need to be modified if your input or output files live in different
    levels of the directory than the assignment3_vtests.py file. **

        python3 assignment3_vtest.py input_file.txt output_file.txt 

    From the main branch in github:

        python3 assignment3_vtest.py test_cases/GA3S1.txt test_cases/output_GA3S1.txt
        python3 assignment3_vtest.py test_cases/GA3S2.txt test_cases/output_GA3S2.txt
        python3 assignment3_vtest.py test_cases/GA3S3.txt test_cases/output_GA3S3.txt
        python3 assignment3_vtest.py test_cases/GA3S4.txt test_cases/output_GA3S4.txt

    
Abstract of Algorithm:
    Step 1)     Read the input file, extract coordinate and edge data into:
                    - an array of coordinates (ArrayPoints)
                    - an array of all edges sorted by weight (SortedEdges)
                    - an array of edges from E Prime. (EPrimeEdges)

    Step 2)     Represent every coordinate in the array of coordinates (ArrayPoints) as a its own disjoint 
                set. Create an variable (Forrest) to hold the UnionFind structure of all disjoint sets.
    
                    
    Step 3)     Organize coordinates reached by E Prime edges (if any) into disjoint sets of coordinates, 
                such that all coordinates in the same set are connected by edges in E Prime. 
                To do this, iterate through the array of edges from E Prime (EPrimeEdges). 
                    -   For each edge, check if its two coordinates are in different sets by comparing the 
                        root coordinates of their disjoint sets. 
                    -   If the edge's two coordinates are in different sets consider the edge to be part 
                        E* preform a union operation on the two disjoint sets of the edge's coordinates, 
                        to reflect that they are connected by an E' input edge.
    
    Step 4)     Find edges that belong in E*, where E* is a subset of all edges that will span all 
                coordinates in complement with E'. 
                To do this, iterate through the sorted array of sorted edges (SortedEdges), starting with
                the smallest element in SortedEdges, until all disjoint sets have been unioned into a single
                set of all coordinates.
                    -   Create a variable (WeightEAsterix) to hold the cumulitive weight of all E* edges found. 
                    -   For each edge, check if its two coordinates are in different sets by comparing the
                        root coordinates of their disjoint sets.
                    -   If the edge's two coordinates are in different sets consider the edge to be part E*. 
                        To represent that the edge is being included in E*, preform a union operation on 
                        the two disjoint sets of the edge's coordinates and add the edge's weight to the
                        WeightEAsterix variable.

"""

## modification of Union-Find python implementaion from: https://yuminlee2.medium.com/union-find-algorithm-ffa9cd7d2dba
## Credit author: Claire Lee
## Original reference code compared int parent/root elements of disjoint sets, modifications to:
##      - compare coordinates
##      - return boolean for union operation
##      - store value of self as well as parent (in the original reference code the index number was the value)
class UnionFind:
    def __init__(self, numOfElements, arrayOfElements):
        self.parent = self.makeSet(numOfElements, arrayOfElements)
        self.value = self.makeSet(numOfElements, arrayOfElements)
        self.size = [1]*numOfElements
        self.count = numOfElements
    
    def makeSet(self, numOfElements, arrayOfElements):
        array = [x for x in range(numOfElements)]
        for i in range(0, numOfElements):
            array[i] = arrayOfElements[i]
        return array

    # Time: O(logn) | Space: O(1)
    def find(self, coordinate):
        # print("coordinate:", coordinate)
        # print("coordinate[2]:", coordinate[2])
        # print("self.parent:", self.parent)
        # print("self.parent[coordinate[2]]:", self.parent[coordinate[2]])
        while coordinate[2] != self.parent[coordinate[2]][2]:
            #path compression
            # print("path compression")
            coordinateidx = coordinate[2]
            self.parent[coordinateidx] = self.parent[self.parent[coordinateidx][2]]
            coordinate = self.parent[coordinateidx]
        return coordinate
    
    # Time: O(1) | Space: O(1)
    def union(self, coordinate1, coordinate2):
        root1 = self.find(coordinate1)
        root2 = self.find(coordinate2)

        # already in the same set
        if root1 == root2:
            return False

        # print("merge")
        if self.size[root1[2]] > self.size[root2[2]]:
            self.parent[root2[2]] = root1
            self.size[root1[2]] += 1
        else:
            self.parent[root1[2]] = root2
            self.size[root2[2]] += 1
        
        self.count -= 1

        return True

# helper function to display edge data encapsulated in class
def display_all_edges(EdgeList):
    print("")
    print("     _____Edges_______________________________________________________________________________________________ ")
    for e in range(len(EdgeList)):
        print("          (Coordinate)(Coordinate)[Weight]: ", EdgeList[e].CoordinateA, EdgeList[e].CoordinateB, " [", EdgeList[e].Weight, "]")

    print("")

# helper function to display edge data encapsulated in class
def display_Forrest(Forrest):
    print("     _____Forrest_____________________________________________________________________________________________ ")
    print("          Parent :", Forrest.parent)
    print("          Value  :", Forrest.value)
    print("          Size   :", Forrest.size)
    print("          Count  :", Forrest.count)

# main function
def minimum_cost_connecting_edges(input_file_path, output_file_path):

# STEP 1 : Read the input file, extract coordinate and edge data
    print("_______________________________________________________________________________________________________")
    print("_____START_____________________________________________________________________________________________")
    print("_______________________________________________________________________________________________________")
    print("")
    print("STEP 1 : Read the input file, extract coordinate and edge data")
    print("")

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
    # the two numbers of each coordinate, and a third collumn for the point's
    # index number in ArrayPoints
    PointStringArray = re.findall('(\\-?\\d+,\\-?\\d+)', ArrayPointstxt)
    VNumVertices = ( ArrayPointstxt.count(",") // 2 ) + 1
    ArrayPoints = [[-1 for column in range(3)] for row in range(VNumVertices)]
    for p in range(0, VNumVertices):
        CoordinateP = PointStringArray[p].split(',')
        ArrayPoints[p][0]= int(CoordinateP[0])
        ArrayPoints[p][1]= int(CoordinateP[1])
        ArrayPoints[p][2]= p


    #Creating Class Edge to encapsulate each possible edge's coordinate and weight 
    class Edge: 
        def __init__(self, CoordinateA, CoordinateB, Weight): 
           self.CoordinateA = CoordinateA
           self.CoordinateB = CoordinateB
           self.Weight = Weight


    if (line2 == "none"):
        EPrimeNumElements = 0
        EPrimeEdges = []

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

    print("     Array Points [x-index, y-index, index_within_array_points]:")
    print("")
    print("         ",ArrayPoints)
    print("")
    print("     SortedEdges (All Possible Edges):")
    display_all_edges(SortedEdges)
    print("     EPrimeEdges:")
    display_all_edges(EPrimeEdges)
    if(len(EPrimeEdges) == 0):
            print("         E Prime is empty.")
            print("")


# End STEP 1.
# We now have an array of coordinates, an array of all edges sorted by weight, and an array of edges from E Prime.
# ArrayPoints, SortedEdges, and EPrimeEdges
            

# STEP 2 :  Represent every coordinate in the array of coordinates (ArrayPoints) as a its own disjoint set. Create a
#           variable (Forrest) to hold the UnionFind structure of all disjoint sets.
    print("")
    print("")
    print("")
    print("STEP 2 :  Represent every coordinate in the array of coordinates (ArrayPoints) as a its own disjoint set.")
    print("          Create a variable (Forrest) to hold the UnionFind structure of all disjoint sets.")
    print("")
    print("     Forrest of Individial Verticies in a Union Find Structure:")
    print("")

    Forrest = UnionFind(VNumVertices, ArrayPoints)
    display_Forrest(Forrest)


#Step 3:    Organize coordinates reached by E Prime edges (if any) into disjoint sets of coordinates, such that all 
#           coordinates in the same set are connected by edges in E Prime.
    print("")
    print("")
    print("")
    print("STEP 3 :  Organize coordinates reached by E Prime edges (if any) into disjoint sets of coordinates,")
    print("          such that all coordinates in the same set are connected by edges in E Prime..")
    print("")
    print("     Forrest Updating with E Prime's Edges:")
    print("")
    if(len(EPrimeEdges) == 0):
            print("         E Prime is empty.")
            print("")
    for e in range(EPrimeNumElements):
        Forrest.union(EPrimeEdges[e].CoordinateA, EPrimeEdges[e].CoordinateB)
        display_Forrest(Forrest)
        print("")
    
            
#Step 4:    Find edges that belong in E*, where E* is a subset of edges that will span all points in complement with E'.
    print("")
    print("")
    print("")
    print("STEP 4 :  Find edges that belong in E*, where E* is a subset of edges that will span all points in complement with E'.")
    print("")

    # Create a variable (WeightEAsterix) to hold the cumulitive weight of all E* edges found. 
    WeightEAsterix = 0

    # For each edge, check if its two coordinates are in different sets
    for e in range(ENumEdges):
        # preform a union operation on the sets of each edge coordinate to union the sets if they are disjoint
        # union will return True if they were disjoint and two sets were unioned
        # union will return False if they were not disjoint and no two sets were unioned
        Belongs = Forrest.union(SortedEdges[e].CoordinateA, SortedEdges[e].CoordinateB)
        if (Belongs == True):
            # If the edge's two coordinates were in different sets, consider the edge to be part E*.
            # To represent that the edge is being included in E*, add the edge's weight to WeightEAsterix.
            WeightEAsterix = WeightEAsterix + SortedEdges[e].Weight
            print("     Found Edge (Coordinate)(Coordinate)[Weight]: ", SortedEdges[e].CoordinateA, SortedEdges[e].CoordinateB, " [", SortedEdges[e].Weight, "]")
            print("")
            print("     New Weight of E*:", WeightEAsterix)
            print("")
            print("     Forrest Updated with New E* Edge:")
            print("")
            display_Forrest(Forrest)
            print("")


    print("Weight of E* is:")

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