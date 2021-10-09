from datetime import datetime
import time
import random
import os

#Method for the original Euclid Algorithm
#Returns a tuple containing the calculated GCD and the execution time in milliseconds
def EuclidOriginal(a, b):
    startTime = time.clock() #Set an initial time value for before the algorithm starts.
    remainder = 1
    while (remainder):
        quotient = a / b;
        remainder = a - (quotient * b);
        a = b;
        b = remainder;
    endTime = time.clock() #Set time value after algorithm is finished executing.
    return (a, (endTime - startTime) * 1000)

#Method for the improved(?) Euclid Algorithm
#Returns a tuple containing the calculated GCD and the execution time in milliseconds
#Improved Euclid Algorithm is done with the three bugs fixed.
def EuclidImproved(a, b):
    startTime = time.clock()
    remainder = 1
    while (remainder):
        remainder = a - b
        if (remainder >= b):
            remainder = remainder - b
            if (remainder >= b):
                remainder = remainder - b
                if (remainder >= b):
                    remainder = a - b * (a/b)
        a = b
        b = remainder
    endTime = time.clock()
    return (a, (endTime - startTime) * 1000)

#Initialization of variables to be used in the program
randomA = []
randomB = []
originalGCD = []
improvedGCD = []
originalBetter = 0
improvedBetter = 0
timeListOriginal = []
timeListImproved = []
originalTimeSum = 0
improvedTimeSum = 0
improvedSavedTimeSum = 0
originalSavedTimeSum = 0
maxOriginal = 0
maxImproved = 0
minOriginal = 0
minImproved = 0
avgOriginal = 0
avgImproved = 0
medianOriginal = 0
medianImproved = 0

#Seed the random number generator
random.seed(datetime.now())

#Perform 100 Euclidean Algorithm tests using randomly generated inputs.
for count in range(0, 100, 1):
    #Get random integer values for a and b.  First parameter of random.randit being 1 guarantees that a,b >= 1 is true.
    #Makes sure that a,b <= 0 never happens.
    a = random.randint(1, 32767)
    b = random.randint(1, 32767)

    #Preprocessing to make sure a >= b.  If a < b is true, their values are swapped.
    if (a < b):
        a,b = b,a

    #Add values of a and b to their respective arrays.
    randomA.append(a)
    randomB.append(b)

    #Running of the original Euclid Algorithm.  Putting returned values into their proper lists.
    #Adding to the time sum for the average calculation later.
    originalResult = EuclidOriginal(a, b)
    originalGCD.append(originalResult[0])
    timeListOriginal.append(originalResult[1])
    originalTimeSum += timeListOriginal[count]

    # Running of the improved(?) Euclid Algorithm.  Putting returned values into their proper lists.
    # Adding to the time sum for the average calculation later.
    improvedResult = EuclidImproved(a, b)
    improvedGCD.append(improvedResult[0])
    timeListImproved.append(improvedResult[1])
    improvedTimeSum += timeListImproved[count]

    #Preparing algorithm comparisons for the Conclusions document later.
    if (timeListImproved[count] > timeListOriginal[count]):
        originalBetter += 1
        originalSavedTimeSum += timeListImproved[count] - timeListOriginal[count]
    if (timeListOriginal[count] > timeListImproved[count]):
        improvedBetter += 1
        improvedSavedTimeSum += timeListOriginal[count] - timeListImproved[count]

#Create a directory for the Algorithm files.
Dir = "EuclidsAlgorithmFiles/"
if not os.path.exists(os.path.dirname(Dir)):
    os.makedirs(Dir)

#Create Results file for the original algorithm.
originalFile = open(Dir + "Original_Euclid_Results.csv", "w")
originalFile.write("Number One,Number Two,Their GCD,Time Spent (Milliseconds)\n")
for i in range(0, 100, 1):
    originalFile.write(str(randomA[i]) + "," + str(randomB[i]) + "," + str(originalGCD[i]) + "," + str(timeListOriginal[i]) + "\n")
originalFile.close()

#Create Results file for the improved algorithm.
improvedFile = open(Dir + "Improved_Euclid_Results.csv", "w")
improvedFile.write("Number One,Number Two,Their GCD,Time Spent (Milliseconds)\n")
for i in range(0, 100, 1):
    improvedFile.write(str(randomA[i]) + "," + str(randomB[i]) + "," + str(improvedGCD[i]) + "," + str(timeListImproved[i]) + "\n")
improvedFile.close()

#Sort the time lists for the max, min, and median values.
timeListOriginal.sort()
timeListOriginal.sort()

#Get max, min, and median values.  Also, calculate average values.
maxOriginal = timeListOriginal[99]
maxImproved = timeListImproved[99]
minOriginal = timeListOriginal[0]
minImproved = timeListImproved[0]
avgOriginal = originalTimeSum / 100.0
avgImproved = improvedTimeSum / 100.0
medianOriginal = (timeListOriginal[49] + timeListOriginal[50]) / 2.0
medianImproved = (timeListImproved[49] + timeListImproved[50]) / 2.0

#Create statistics file for original algorithm
originalStatsFile = open(Dir + "Original_Euclid_Statistics.csv", "w")
originalStatsFile.write("Statistics,Milliseconds\nMaximum Time," + str(maxOriginal) + "\nMinimum Time" + str(minOriginal) + "\nAverage Time," + str(avgOriginal) + "\nMedian Time," + str(medianOriginal))
originalStatsFile.close()

#Create statistics file for improved algorithm
improvedStatsFile = open(Dir + "Improved_Euclid_Statistics.csv", "w")
improvedStatsFile.write("Statistics,Milliseconds\nMaximum Time," + str(maxImproved) + "\nMinimum Time" + str(minImproved) + "\nAverage Time," + str(avgImproved) + "\nMedian Time," + str(medianImproved))
improvedStatsFile.close()

#Create Conclusion file
conclusionFile = open(Dir + "Conclusions.txt", "w")
conclusionFile.write("(1) Out of 100 pairs of integers, the improved(?) Euclid's algorithm outperformed the original one in " + str(improvedBetter) + " pairs,"
+ "and the average saved time for one pair of integers was " + str(improvedSavedTimeSum / improvedBetter) + "milliseconds.\n"
"(2) Out of 100 pairs of integers, the original Euclid's algorithm outperformed the improved(?) one in " + str(originalBetter) + " pairs,"
+ "and the average saved time for one pair of integers was " + str(originalSavedTimeSum / originalBetter) + "milliseconds.")
conclusionFile.close()

#Notify user on where the files have been stored
input("Program finished.  Desired files have been created in: \n"  + os.path.realpath(__file__) + "/" + Dir +  "\n\nPress the \"enter\" key to continue.")