--lua53.exe ex.lua: example for console 

function min_max(list, numElems)
    maxVal, minVal = list[1], list[1]
    maxPos, minPos = 1, 1
    for itemNum = 1, numElems, 1
    do
        if maxVal < list[itemNum]
        then
            maxVal = list[itemNum]
            maxPos = itemNum
        end
        if minVal > list[itemNum]
        then
            minVal = list[itemNum]
            minPos = itemNum
        end
    end
    return minVal, minPos, maxVal, maxPos
end

myList = {4,1,4,5,10,100,2,20}
numElems = 8
minVal, minInd, maxVal, maxInd = min_max(myList, numElems)
print("Minimum value is", minVal)
print("Minimum value is stored at location", minInd)
print("Maximum value is", maxVal)
print("Maximum value is stored at location", maxInd)

    