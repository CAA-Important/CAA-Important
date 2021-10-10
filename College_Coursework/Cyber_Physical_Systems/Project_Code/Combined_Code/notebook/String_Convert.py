def StringConvert(theString, mode):
    returnString = ""
    if(mode == 'e'):
        for x in theString:
            if(ord(x) > 127):
                returnString = returnString + str(hex(ord("a")))
                toAdd = ord(x) - 97
                while toAdd > 97:
                    returnString = returnString + "a"
                    toAdd = toAdd - 97
                returnString = returnString + chr(toAdd)

            elif ord(x) < 10:
                returnString = returnString + "0x0" + str((ord(x)))

            else:
                returnString = returnString + str(hex(ord(x)))

        return returnString

    if(mode == 'd'):
        returnList = theString.split("0x")[1:]
        for x in returnList:
            if len(x) == 2:
                toAdd = chr(int("0x" + x, 0))
                returnString = returnString + toAdd
            else:
                value = int("0x" + x[0:2], 0)
                for y in x[2:]:
                    value = value + ord(y)
                returnString = returnString + chr(value)

        return returnString
