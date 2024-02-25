from assignment3 import *
from time import *




def main():
    for i in range(1,5):
        input = "test_cases/GA3S{}.txt"
        output = "test_cases/output_GA3S{}.txt"

        input =input.format(str(i).zfill(1))
        output = output.format(str(i).zfill(1))   
        
        
        start_time = time()
        open(output,"w+").close()
        minimum_cost_connecting_edges(input , output)
 
        print("Ran in " + str(time() - start_time))


if __name__ == "__main__":
    main()