function threeOrFive(theArray){
    return theArray.filter((theNumber) => ((theNumber % 3 == 0) || (theNumber % 5 == 0)));
}

arrayTest = [12, 5, 8, 130, 44];

arrayTested = threeOrFive(arrayTest);

console.log(arrayTested);