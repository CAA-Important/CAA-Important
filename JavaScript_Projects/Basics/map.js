function evenOneOddZero(theArray){
    return theArray.map((theNumber) => ((theNumber + 1) % 2));
}

arrayTest = [1, 3, 4, 7, 100, 412, 13, 15, 20];

arrayTested = evenOneOddZero(arrayTest);

console.log(arrayTested);