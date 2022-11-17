"""
Author: N00DL3S
Version: V1
GitHub: https://github.com/B1GN00DL3S
"""
import hashlib
import math

class Base:
    Error = ["Error Command Type Was Not Selected.", "Error Text Was Not Inputed.", "Error Password Was Not Inputed.",
             "Error Length Of Key Was Not Inputed.", "Error Count Type Was Not Selected.", "Error File Does Not Exist."]#This holds all the Error's

    y = 2#Length of the key

    CharList = (
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
    "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "!", '"', "£", "$", "%", "^", "&", "*",
    "(", ")", "_", "-", "+", "=", "[", "]", "{", "}", "#", "~", ":", ";", "@", "'", "/", "<", ">", ",", ".", "?",
    "`", " ", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
    "u", "v", "w", "x", "y", "z")#This is a list of characters that

    def PasswordToKey(password, y, CharList):#This function creates the first set of keys from the password that is input
        test = ""
        hash = str(password)
        for x in range(math.ceil((y * len(CharList)) / 128) - 1):#Checks to make sure that the hashed password is long enough and if not it hashs it and adds it to the hash
            hash += str(hashlib.sha512(hash.encode()).hexdigest())
        StartKey = []
        for x in range(len(CharList)):#Creates all the slots in the StartKey var
            StartKey.append([])
        for x in range(len(CharList)):#Sets the keys from the hashed password
            if len(StartKey[x]) == 0:
                test = hash[int(x * y):int(x * y + y)]
            while True:#This loop tests the key to see if it is already in the key list to prevent doubles
                count = 0
                for c in range(len(StartKey)):
                    try:
                        StartKey[c].index(test)  # Test if in list
                    except:
                        count += 1
                if count == len(StartKey):
                    StartKey[x].append(test)  # Append if not in list
                    break
                else:
                    test = hex(int(test, 16) + 1)[2:]#Adds 1 to the test key to create new test key
                    if len(test) < y:#Checks if the new test key is the right lenght if not then it adds 0's to the start of the test key
                        while True:
                            test = str("0" + test)
                            if len(test) == y:
                                break
        return (StartKey)

    def Encryption(text,password,y,CharList,Count):
        StartKey = Base.PasswordToKey(hashlib.sha512(password.encode()).hexdigest(), y, CharList)#This gets the first set of keys
        KeyCount = len(StartKey)#This var counts the ammount of keys created
        EncryptedText = ""
        for x in text:#Loops through the inputed text
            if Count and len(EncryptedText) == 0:#This prints out the progress if count is selected
                print(int(len(EncryptedText)/y),"/",len(text))
            EncryptedText += StartKey[CharList.index(x)][len(StartKey[CharList.index(x)]) - 1]  #This selects the key for the letter in text and adds it to EncryptedText
            KeyCount += 1
            # Create new key and check if the max ammount of keys has been hit
            if KeyCount == math.trunc((16 ** y) / len(CharList)) * len(CharList):  # Checks if it has done all possable
                print("a")
                KeyCount = len(StartKey)  # Sets up count
                newStartKey = []  # Sets up newStartKey
                for x in range(len(CharList)):
                    newStartKey.append([])
                for x in range(len(StartKey)):  # Loops through all of the keys and create the new hash startkey
                    test = str(hashlib.sha512(StartKey[x][len(StartKey[x]) - 1].encode()).hexdigest()[
                               int(0):int(y)])  # hash the start key
                    while True:
                        count = 0
                        for c in range(len(newStartKey)):
                            try:
                                newStartKey[c].index(test)  # Test if in list
                            except:
                                count += 1
                        if count == len(newStartKey):
                            newStartKey[x].append(test)  # Append if not in list
                            break
                        else:
                            test = hex(int(test, 16) + 1)[2:]
                            if len(test) < y:
                                test = str("0" + test)
                StartKey = newStartKey
            else:
                test = str(hashlib.sha512(
                    StartKey[CharList.index(x)][len(StartKey[CharList.index(x)]) - 1].encode()).hexdigest()[
                           int(0):int(y)])  # hash the start key
                while True:
                    count = 0
                    for c in range(len(StartKey)):
                        try:
                            StartKey[c].index(test)  # Test if in list
                        except:
                            count += 1
                    if count == len(StartKey):
                        StartKey[CharList.index(x)].append(test)  # Append if not in list
                        break
                    else:
                        test = hex(int(test, 16) + 1)[2:]
                        if len(test) < y:
                            test = str("0" + test)
            if Count:
                print(int(len(EncryptedText)/y),"/",len(text))
        return (EncryptedText)

    def Decryption(EncryptedText,password,y,CharList,Count):
        StartKey = Base.PasswordToKey(hashlib.sha512(password.encode()).hexdigest(), y, CharList)
        KeyCount = len(StartKey)
        DecryptedText = ""
        for z in range(int(len(EncryptedText) / y)):  # loops for each char according to the y
            if Count and len(DecryptedText) == 0:
                print(len(DecryptedText),"/",int(len(EncryptedText) / y))
            for x in range(len(StartKey) + 1):  # loops for the length of StartKey
                try:
                    StartKey[x].index(EncryptedText[z * y:z * y + y])  # Trys list in start key and the last on the list of the list
                except:
                    ValueError
                else:
                    DecryptedText += CharList[x]  # if no error means in list so add to decrypted
                    KeyCount += 1
                    # Create new key and check if the max ammount of keys has been hit
                    if KeyCount == math.trunc((16 ** y) / len(CharList)) * len(CharList):  # Checks if it has done all possable
                        print("a")
                        KeyCount = len(StartKey)  # Sets up count
                        newStartKey = []  # Sets up newStartKey
                        for x in range(len(CharList)):
                            newStartKey.append([])
                        for x in range(len(StartKey)):  # Loops through all of the keys and create the new hash startkey
                            test = str(hashlib.sha512(StartKey[x][len(StartKey[x]) - 1].encode()).hexdigest()[
                                       int(0):int(y)])  # hash the start key
                            while True:
                                count = 0
                                for c in range(len(newStartKey)):
                                    try:
                                        newStartKey[c].index(test)  # Test if in list
                                    except:
                                        count += 1
                                if count == len(newStartKey):
                                    newStartKey[x].append(test)  # Append if not in list
                                    break
                                else:
                                    test = hex(int(test, 16) + 1)[2:]
                                    if len(test) < y:
                                        test = str("0" + test)
                        StartKey = newStartKey
                    else:
                        # Create new key
                        test = str(hashlib.sha512(StartKey[x][len(StartKey[x]) - 1].encode()).hexdigest()[
                                   int(0):int(y)])  # hash the start key
                        while True:
                            count = 0
                            for c in range(len(StartKey)):
                                try:
                                    StartKey[c].index(test)  # Test if in list
                                except:
                                    count += 1
                            if count == len(StartKey):
                                StartKey[x].append(test)  # Append if not in list
                                break
                            else:
                                test = hex(int(test, 16) + 1)[2:]
                                if len(test) < y:
                                    test = str("0" + test)
            if Count:
                print(len(DecryptedText),"/",int(len(EncryptedText) / y))
        return (DecryptedText)

class Text:
    def Encryption(*args):
        try:  # Checks if command is there
            args[0]
        except:
            return (Base.Error[0])
        if args[0] != True and False:  # No Command Type Error
            return (Base.Error[0])
        if args[0]:#Checks if command is there if so then starts to check everything else
            try:
                Count = args[1]
            except:
                return (Base.Error[4])
            else:
                if args[1] == "True" or "False":
                    Count = args[1]
                else:
                    return (Base.Error[4])
            for x in range(2):
                try:
                    args[x + 2]
                except:
                    return (Base.Error[x + 2])
            text, password = args[2:]#Sets text and password from the input
            if len(text) == 0:
                return(Base.Error[1])
            if len(password) == 0:
                return(Base.Error[2])
        else:
            while True:
                text = input("Enter the text that you want to encrypt: ")
                if len(text) != 0:
                    break
                else:
                    print(Base.Error[1])
            while True:
                password = input("Input the password that you want to use: ")
                if len(password) != 0:
                    break
                else:
                    print(Base.Error[2])
            while True:
                Count = input("Do you want to show the progress (True/False): ").upper()
                if Count == "TRUE":
                    Count = True
                    break
                elif Count == "FALSE":
                    Count = False
                    break
                else:
                    print(Base.Error[4])
        return(Base.Encryption(text,password,Base.y,Base.CharList,Count))

    def Decryption(*args):
        try:  # Checks if command is there
            args[0]
        except:
            return (Base.Error[0])
        if args[0] != True and False:  # No Command Type Error
            return (Base.Error[0])
        if args[0]:#Checks if command is there if so then starts to check everything else
            try:
                Count = args[1]
            except:
                return (Base.Error[4])
            else:
                if args[1] == "True" or "False":
                    Count = args[1]
                else:
                    return (Base.Error[4])
            for x in range(2):
                try:
                    args[x + 2]
                except:
                    return (Base.Error[x + 2])
            text, password = args[2:]#Sets text and password from the input
            if len(text) == 0:
                return(Base.Error[1])
            if len(password) == 0:
                return(Base.Error[2])
        else:
            while True:
                text = input("Enter the text that you want to decrypt: ")
                if len(text) != 0:
                    break
                else:
                    print(Base.Error[1])
            while True:
                password = input("Input the password that you want to use: ")
                if len(password) != 0:
                    break
                else:
                    print(Base.Error[2])
            while True:
                Count = input("Do you want to show the progress (True/False): ").upper()
                if Count == "TRUE":
                    Count = True
                    break
                elif Count == "FALSE":
                    Count = False
                    break
                else:
                    print(Base.Error[4])
        return(Base.Decryption(text,password,Base.y,Base.CharList,Count))