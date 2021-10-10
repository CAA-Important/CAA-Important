function charFrequency(freqDict, str)
    for char = 1, string.len(str)
    do
        if freqDict[string.sub(str, char, char)] == nil
        then
            freqDict[string.sub(str, char, char)] = 0
        end
        freqDict[string.sub(str, char, char)] = freqDict[string.sub(str, char, char)] + 1
    end
end

freqDict = {}
charFrequency(freqDict, "SUPERSTUFF")
for key, value in pairs(freqDict)
do
    print(key, value)
end