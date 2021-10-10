import tkinter
from tkinter import scrolledtext
import random
import os
import math
import time

class MS:

    def __init__(self):
        #Array to hold the 9 arrays
        self.theArrays = []
        #Seed the random number generator
        random.seed()
        #From 1 (inclusive) to 10 (exclusive)
        for i in range(1, 10):
            #Initialize an array to hold the numbers
            anArray = []
            #Generate i * 1000 numbers for each Array_i
            for x in range(0, i * 1000):
                #Generate a random real number between the standard MIN_INT and MAX_INT for a signed integer
                #And add it to Array_i
                anArray.append(random.uniform(-2147483648, 2147483647))

            #Add Array_i to the list of arrays
            self.theArrays.append(anArray)

        self.gui = None


    #Merge Function
    def Merge(self, L1, L2):
        #Initialize array to hold merged list
        L3 = []
        #As long as we have not moved outside the memory space of either array
        while len(L1) > 0 and len(L2) > 0:
            #If L1 contains the smaller
            if L1[0] < L2[0]:
                #Add L1's value to the new array and move L1's pointer
                L3.append(L1.pop(0))

            #Otherwise, L2 contains the smaller
            else:
                # Add L2's value to the new array and move L1's pointer
                L3.append(L2.pop(0))


        #If L1 still has items in it, append them to the end of L3
        while len(L1) > 0:
            L3.append(L1.pop(0))

        #If L2 still has items in it, append them to the end of L3
        while len(L2) > 0:
            L3.append(L2.pop(0))

        #Return the final sorted array
        return(L3)

    def MergeSort(self, toSort):
        if len(toSort) <= 1:
            #Array of size one is sorted, making it suitable for merging
            return(toSort)

        else:
            #Otherwise, divide array into two halves, recursively call MergeSort on the halves, and Merge those
            return self.Merge(self.MergeSort(toSort[0:len(toSort)//2]), self.MergeSort(toSort[len(toSort)//2:]))


    def SaveToCSV(self):
        self.stb_for_arrays.delete(1.0, tkinter.END)
        #Initial save information as the column names
        toSave = "Input size n for Array_i,Value of n * log(n),Time spent (milliseconds),Value of ( n * log(n) ) / time\n"
        for array in self.theArrays:
            #For each array, create desired information to be save to the file and add it to the string of information
            n = len(array)
            nlogn = n * math.log(n, 2)
            starttime = time.clock()
            self.MergeSort(array)
            endtime = time.clock()
            elapsed_millis = (endtime - starttime) * 1000
            nlognOverTime = nlogn / elapsed_millis
            nlognOverTimeString = "{:.0E}".format(nlognOverTime).replace("+0", "").replace("+", "")
            nlognOverTimeStringSplit = nlognOverTimeString.split("E")
            toSave += str(n) + "," + str(nlogn) + "," + str(elapsed_millis) + "," + nlognOverTimeStringSplit[0] + " * 10^(" + nlognOverTimeStringSplit[1] + ")" + "\n"

        try:
            #Directory to save file in
            placeToSave = "Mergesort_Save_Folder\\"
            #Check if directory exists.  If not, make it.
            if not os.path.exists(os.path.dirname(placeToSave)):
                os.makedirs(placeToSave)

            #Create the file to save in
            theFile = open(placeToSave + "Mergesort_Time.csv", "w")
            #Write information to the file
            theFile.write(toSave)
            #Close the file
            theFile.close()
            #Display to user that the file was successfully saved
            self.stb_for_arrays.insert(tkinter.INSERT, "File successfully saved to " +  os.path.abspath(placeToSave + "Mergesort_Time.csv"))

        except:
            #Display to user that the file failed to save
            self.stb_for_arrays.insert(tkinter.INSERT, "An error occurred.  File failed to save")


    def run(self):
        #Build the pieces of the gui
        self.gui = tkinter.Tk()
        self.stb_for_arrays = scrolledtext.ScrolledText(self.gui, undo = True)
        array_1_button = tkinter.Button(self.gui, text="1", height=2, width=15, command=lambda:self.DisplayChosen(1))
        array_2_button = tkinter.Button(self.gui, text="2", height=2, width=15, command=lambda: self.DisplayChosen(2))
        array_3_button = tkinter.Button(self.gui, text="3", height=2, width=15, command=lambda: self.DisplayChosen(3))
        array_4_button = tkinter.Button(self.gui, text="4", height=2, width=15, command=lambda: self.DisplayChosen(4))
        array_5_button = tkinter.Button(self.gui, text="5", height=2, width=15, command=lambda: self.DisplayChosen(5))
        array_6_button = tkinter.Button(self.gui, text="6", height=2, width=15, command=lambda:self.DisplayChosen(6))
        array_7_button = tkinter.Button(self.gui, text="7", height=2, width=15, command=lambda: self.DisplayChosen(7))
        array_8_button = tkinter.Button(self.gui, text="8", height=2, width=15, command=lambda: self.DisplayChosen(8))
        array_9_button = tkinter.Button(self.gui, text="9", height=2, width=15, command=lambda: self.DisplayChosen(9))
        save_button = tkinter.Button(self.gui, text="Save CSV", height=2, width=15, command=self.SaveToCSV)
        quit_button = tkinter.Button(self.gui, text="Quit", height=2, width=15, command=self.gui.destroy)

        #Display the pieces of the gui
        self.stb_for_arrays.pack()
        array_1_button.pack()
        array_2_button.pack()
        array_3_button.pack()
        array_4_button.pack()
        array_5_button.pack()
        array_6_button.pack()
        array_7_button.pack()
        array_8_button.pack()
        array_9_button.pack()
        save_button.pack()
        quit_button.pack()

        #Format the gui and the pieces
        self.gui.geometry('{}x{}'.format(960, 600))
        self.stb_for_arrays.place(x=150, y=25)
        array_1_button.place(x=90, y=450)
        array_2_button.place(x=250, y=450)
        array_3_button.place(x=410, y=450)
        array_4_button.place(x=570, y=450)
        array_5_button.place(x=730, y=450)
        array_6_button.place(x=90, y=500)
        array_7_button.place(x=250, y=500)
        array_8_button.place(x=410, y=500)
        array_9_button.place(x=570, y=500)
        save_button.place(x=730, y=500)
        quit_button.place(x=730, y=550)

        #Start the gui
        self.gui.mainloop()

    def DisplayChosen(self, array_number):
        #Clear the text
        self.stb_for_arrays.delete(1.0, tkinter.END)
        #Get the time taken and a sorted array
        start = time.clock()
        sorted_array = self.MergeSort(self.theArrays[array_number - 1])
        end = time.clock()
        elapsed_millis = (end - start) * 1000
        #Display the information
        self.stb_for_arrays.insert(tkinter.INSERT, "Number of items: " + str(array_number * 1000) + "\n"
                                   + "Time taken (milliseconds): " + str(elapsed_millis) + "\n" +
                                   "\tOriginal Array\t\t\tSorted Array\n")

        for count in range(0, len(sorted_array)):
            self.stb_for_arrays.insert(tkinter.INSERT, "\t" + str(self.theArrays[array_number - 1][count])
                                       + "\t\t\t" + str(sorted_array[count]) + "\n")





if __name__ == "__main__":
    ms = MS()
    ms.run()