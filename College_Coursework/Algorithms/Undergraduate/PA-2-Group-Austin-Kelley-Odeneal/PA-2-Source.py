
#Import all necessary libraries
import tkinter
from tkinter import scrolledtext
import math
import time
import random
import copy
import os

#Create a variable for generating the arrays.
arraySize = 1000

#Create the pieces of the gui
gui = tkinter.Tk()
arrayDisplay = scrolledtext.ScrolledText(gui, undo = True)
arrayChoices = tkinter.Spinbox(gui, from_ = 1, to = 9, wrap = True)
arrayChoicesLabel = tkinter.Label(gui, text = "Choose an integer between 1 and 9 from that box above.  Other values will not work.")
infoSaveCheckVar = tkinter.IntVar()
infoSave = tkinter.Checkbutton(gui, text = "Save Information to File?", height = 5, width = 20, variable = infoSaveCheckVar, offvalue = 0, onvalue = 1)
arrayShow = tkinter.Button(gui, text = "Display Array Sorting Results", command = lambda: MergeSortTest(int(arrayChoices.get()), infoSaveCheckVar.get()))
endProg = tkinter.Button(gui, text = "Terminate Program", command = gui.destroy)

#Show the gui
arrayDisplay.pack()
arrayChoices.pack()
arrayChoicesLabel.pack()
arrayShow.pack()
infoSave.pack()
endProg.pack()

#Prepare an array to hold the generated arrays
createdArrays = [[], [], [], [], [], [], [], [], []]
sortedArrays = [[], [], [], [], [], [], [], [], []]

#Set gui size
gui.geometry('{}x{}'.format(960, 600))

#Merge function
def Merge(list1, list2):
    #Create the final array as well as array location pointers
    list3 = []
    list1Location = 0
    list2Location = 0

    #Pre-check for best case scenario for improved speed up when it occurs
    if(list1[len(list1) - 1] <= list2[0]):
        for item in list1:
            list3.append(item)
        for item in list2:
            list3.append(item)
        return(list3)

    if (list2[len(list2) - 1] <= list1[0]):
        for item in list2:
            list3.append(item)
        for item in list1:
            list3.append(item)
        return(list3)

    #Standard merge algorithm based on Professor Huang's pseudocode
    while(True):

        #Test which value should be added to the new list as well as which list pointer should be moved
        if(list1[list1Location] < list2[list2Location]):
            list3.append(list1[list1Location])
            list1Location += 1
        else:
            list3.append(list2[list2Location])
            list2Location += 1

        #Boundary check
        if(list1Location >= len(list1)):
            for remaining in range(list2Location, len(list2)):
                list3.append(list2[remaining])
            break
        if (list2Location >= len(list2)):
            for remaining in range(list1Location, len(list1)):
                list3.append(list1[remaining])
            break

    #Return merged list
    return(list3)

#Mergesort Algorithm; adjusted to properly handle lists with an odd number of items
def MergeSort(list):
    if(len(list) == 1):
        return(list)
    else:
        list1 = MergeSort(list[0 : int(math.floor(len(list) / 2))])
        list2 = MergeSort(list[int(math.floor(len(list) / 2)) : len(list)])
        return Merge(list1, list2)

#Function for testing how long Mergesort takes
def MergeSortTest(i, fileSave):
    i = int(i)

    #Make sure i is an appropriate value
    if(i >= 1 and i <= 9):

        #Bring in global variables
        global arraySize
        global arrayDisplay
        global createdArrays
        global sortedArrays

        #Clear the current display
        arrayDisplay.delete(1.0, tkinter.END)

        #If array_i has not been created yet, create it, create a sorted version of it, and save the sort time in milliseconds
        if(len(createdArrays[i - 1]) == 0):
            theList = []
            random.seed(time.time())
            for x in range(0, i * arraySize):
                theList.append(random.randint(-32768, 32768) * random.random())
            createdArrays[i - 1] = theList
            sortedArrays[i - 1] = copy.deepcopy(createdArrays[i - 1])
            starttime = time.clock()
            sortedArrays[i - 1] = MergeSort(sortedArrays[i - 1])
            endtime = time.clock()
            createdArrays[i - 1].append((endtime - starttime) * 1000)

        #Display the information for array_i
        arrayDisplay.insert(tkinter.INSERT, "Number of elements: " + str(i * arraySize) + "\n"
                            + "Time taken to sort: " + str((createdArrays[i - 1])[i * arraySize]) + " milliseconds\n"
                            + "\tOriginal Array\t\t\tSorted Array\n")
        for y in range(0, i * arraySize):
            arrayDisplay.insert(tkinter.INSERT, str(y + 1) + ":\t" + str((createdArrays[i - 1])[y]) + "\t\t\t" + str((sortedArrays[i - 1])[y]) + "\n")

        #If the user wants to save the deliverable data to a file, do so
        if(fileSave != 0):

            #Create directory if it does not already exist
            Dir = "MergeSortFile\\"
            if not os.path.exists(os.path.dirname(Dir)):
                os.makedirs(Dir)
            #Create a file if it does not alreay exist
            if not os.path.isfile(Dir + "Mergesort_Time.csv"):
                prepFile = open(Dir + "Mergesort_Time.csv", "w")
                prepFile.write("Input Size n for Array_i,Value of n * lg(n),Time Spent (milliseconds),Value of (n * lg(n)) / time\n")
                prepFile.close()

            #Prepare deliverable information to write to file
            n = i * arraySize
            nlgn = n * math.log(n, 2)
            elapsedTime = (createdArrays[i - 1])[i * arraySize]
            nlgnDivtime = nlgn / elapsedTime
            sciNoteExp = 0
            if(nlgnDivtime > 1):
                while(nlgnDivtime > 10):
                    nlgnDivtime /= 10
                    sciNoteExp += 1
            elif (nlgnDivtime < 1):
                while (nlgnDivtime < 1):
                    nlgnDivtime *= 10
                    sciNoteExp -= 1
            nlgnDivtime = int(round(nlgnDivtime))

            #Write deliverable information to file
            originalFile = open(Dir + "Mergesort_Time.csv", "a")
            originalFile.write("Array_" + str(i) + "; Input size: " + str(n) + "," + str(nlgn) + "," + str(elapsedTime) + ","
                               + str(nlgnDivtime) + " * 10^(" + str(sciNoteExp) + ")\n")
            originalFile.close()
            arrayDisplay.insert(tkinter.INSERT, "\nResults have been saved in:\n" + os.path.realpath(__file__) + "\\" + Dir + "Mergesort_Time.csv")





#Begin GUI
gui.mainloop()
