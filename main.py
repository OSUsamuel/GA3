from assignment3 import *
from time import *



"""
This file is used for debugging purposes allowing us to take advantage of VS code built in debugger
This will run through every test file that is spececified in the range clause of the for loop, 
so long as it is the format of GA3S#.txt and the file is under the test_cases directory.  Also 
printing the time to the terminal. This is then outputed similarly in the test_cases directory with 
the file name being output_GA3S#, respectively.

How to use for debugging:
There should be a button with a bug and run symbol in your left hand section of VS code.  If none
is present let me know.  
Shift to assignemnt3.py and move to a section of code you want to debug.  When you hover over the left
of the line numbers a red dot should appear, click it, this is known as a breakpoint and the debugger
will stop exectuion of the program at said spot and allow you move through each line of code one by one.

If you have more questions about using the debugger for certain operations, I guarentee you there is 
a way to do it just let me know or consult the documentation on VS code website.

If you would like any updates to the bottom code, i.e. a working U.I., more information to be displayed
feel free to update it yourself and push, or let me know and I will do it.


"""
def main():
    for i in range(1,5):
        input = "test_cases/GA3S{}.txt"
        output = "test_cases/output_GA3S{}.txt"

        input =input.format(str(i).zfill(1))
        output = output.format(str(i).zfill(1))   
        
        
        start_time = time()
        open(output,"w+").close()  #Creates new file if one doesn't exist
        minimum_cost_connecting_edges(input , output)
 
        print("Ran in " + str(time() - start_time))


if __name__ == "__main__":
    main()