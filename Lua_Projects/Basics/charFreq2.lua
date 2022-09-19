function charFrequency(freqDict, str)
    for char = 1, string.len(str)
    do
        freqDict[string.sub(str, char, char)] = freqDict[string.sub(str, char, char)] + 1
    end
end


freqDict = {}
freqDict = setmetatable({}, {
    __index = function(freqDict, key, value)
        if(value == nil)
        then
            return 0
        end
    end
})
charFrequency(freqDict, "SUPERSTUFF")
for key, value in pairs(freqDict)
do
    print(key, value)
end