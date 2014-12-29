#############################################################################
#Usage : >Script LegacyFile SwitchFile
#ISO request comparator
#outputCompact contains comparisons of unique ISOs of a particular amount
#outputDetailed contains comparisons of all ISOs of a particular amount
#############################################################################

import re
import sys

#This function defines global variables
def globalVariables():
    global x,y,outputString,outputStringShort
    __author__ = 'dbatheja'
    x = ""
    y = ""
    outputString=""
    outputStringShort=""

#File Usage instruction
def usage():
    print("Usage:\t>Script LegacyFile SwitchFile")


#main Function
def main():
    global x,y,outputString,outputStringShort
    filesChosen = sys.argv
    #filesChosen = ['1','2','3']#
    if len(filesChosen) > 2:

        x = filesChosen[1]
        y = filesChosen[2]

        #x = "fdmsLogs.txt"
        #y = "new2.LOG"

        old = open(x, "r")
        new = open(y, "r")
        outputString+="FILES COMPARED:\n"+x+"\n"+y+"\n\n"
        outputStringShort+="FILES COMPARED:\n"+x+"\n"+y+"\n\n"
        dictionaryOld = cleanUp(old,x)
        dictionaryNew = cleanUp(new,y)
        f = str(len(dictionaryOld.keys()))
        g = str(len(dictionaryNew.keys()))
        outputString +="\nNo. of unique amount values in "+str(x)+" :"+f+"\n"
        outputString+="List of unique amount values in "+str(x)+" :"+str(dictionaryOld.keys())+"\n"
        outputString +="No. of unique amount values in "+str(y)+" :"+g+"\n"
        outputString+="List of unique amount values in "+str(y)+" :"+str(dictionaryNew.keys())+"\n"
        outputStringShort +="\nNo. of unique amount values in "+str(x)+" :"+f+"\n"
        outputStringShort+="List of unique amount values in "+str(x)+" :"+str(dictionaryOld.keys())+"\n"
        outputStringShort +="No. of unique amount values in "+str(y)+" :"+g+"\n"
        outputStringShort+="List of unique amount values in "+str(y)+" :"+str(dictionaryNew.keys())+"\n"


        for key, value in dictionaryOld.items():
            for key2,value2 in dictionaryNew.items():
                if key2 in [key]:
                    findMatch(value,value2,key)

        generateOutput()

    else:
        usage()


#This function prints the output to Files
def generateOutput():
    global x,y,outputString,outputStringShort
    print("\n"*4,"#"*10,"Output Generated","#"*10)

    #name= input('Enter detailed output file-name:')+'.txt'
    name = 'outputDetailed.txt'
    #name= input('Enter short  output file-name:')+'.txt'
    name2 = 'outputCompact.txt'

    print("\n\noutputDetailed.txt\noutputCompact.txt\n")
    file = open(name,'w')
    file.write(outputString)
    file.close()
    file = open(name2,'w')
    file.write(outputStringShort)
    file.close()


#This function accepts file input and returns a cleaned up Dictionary
def cleanUp(file,name):
    global outputString
    global outputStringShort
    dictList=[]   #list of dictionaries in a file
    for line in file:

        if re.search(r"(0100\|PBM)(.)+", line, re.I|re.M):
            line= line.split('|')
            #line.remove(line[0])
            lineDictionary = createDictionary(line)
            dictList.append(lineDictionary)
    Total = len(dictList)
    print("Total requests in ",name,": ",Total,"\n")
    outputString+="Total requests in "+name+": "+str(Total)+"\n"
    outputStringShort+="Total requests in "+name+": "+str(Total)+"\n"

    #This creates a amount based dictionary
    amountDictionary = {}   #amount based dictionary of a file
    for i in dictList:
        if "4" in i:
            if i.get("4") in amountDictionary:
                a = i.get("4")
                b = amountDictionary.get(i.get("4"))
                b.append(i)
                amountDictionary.update({a:b})
            else:
                a=i.get("4")
                b=[]
                b.append(i)
                amountDictionary.update({a:b})

    return amountDictionary


def remove63format(var):
    a = var.replace("!","")
    v = a.index("[")
    w = a.index("]")
    l = w-v-1
    m = 4-l
    a = a.replace("[","0"*m,1)
    a = a.replace("]","",1)
    if "[" in a:
        a = remove63format(a)
    return a

#This function accepts a list of strings and returns a dictionary value
def createDictionary(line):
    dictionaryVariable = {}
    for i in line:
        #var[0] = key
        #var[1] = value
        var = i.split(':')
        var[0]=var[0].lstrip('0')

        #converting PBM to lower case
        pbm = re.search(r'PBM',var[0],re.M|re.I)
        if pbm:
            var[0]=var[0].lower()
        if "[" in str(var[0]):
            z=str(var[0]).index("[")
            a=str(var[0])[:z]
            var[0] = a

        if var[0] in ["63"] and "[" in var[1]:
            var[1] = remove63format(str(var[1]))


        if len(var) > 1 :
            var[1]=var[1].strip(" ")
            var[1]=var[1].strip("\n")
			var[1]=var[1].strip("\r")
            dictionaryVariable.update({str(var[0]) : str(var[1])})
    zombie=0
    for i in dictionaryVariable:
        a=str(i).strip(" ")
        if " " in a:
            zombie+=1
            break

    if zombie > 0:
        del dictionaryVariable[i]
        #print("#removedKey  ",i)
    return dictionaryVariable

#Accepts lists of dictionaries for a particular amount
def findMatch(a,b,amount):
    global outputString
    global outputStringShort
    global x
    global y
    outputString+="\n\n"+"========"*80+"\n\nFor Amount -- "+str(amount)
    outputStringShort+="\n\n"+"========"*80+"\n\nFor Amount -- "+str(amount)


    if len(a) > 1:
        outputString+="\n"+"###WARNING - Duplicate entries for amount "+str(amount)+" in "+str(x)+": "+str(len(a))
        outputStringShort+="\n"+"###WARNING - Duplicate entries for amount "+str(amount)+" in "+str(x)+": "+str(len(a))
        #print("###WARNING - Duplicate entries for amount ",amount," in ",x,": ",len(a))
    if len(b) > 1:
        outputString+="\n"+"###WARNING - Duplicate entries for amount "+str(amount)+" in "+str(y)+": "+str(len(b))
        outputStringShort+="\n"+"###WARNING - Duplicate entries for amount "+str(amount)+" in "+str(y)+": "+str(len(b))
        #print("###WARNING - Duplicate entries for amount ",amount," in ",y,": ",len(b))
    outputString+="\n"+"Total comparisons :"+str(len(a)*len(b))
    outputStringShort+="\n"+"Total comparisons :"+str(len(a)*len(b))
    #print("Total comparisons :",len(a)*len(b))
    comparisons = len(a)*len(b)
    for i in a:
        for j in b:
            findFieldMatch(i,j,comparisons)




#Accepts two dictionaries -compares all fields and prints results
def findFieldMatch(dictionary1,dictionary2,comparisons):
    keysNotFound1 = []
    keysNotFound2 = []
    keysLengthMismatch = []
    keysExactMatch = []
    keysExactNoMatch = []
    global outputString
    global outputStringShort
    global x
    global y
    outputString+="\n"+"-"*20
    outputString+="\n"+str(dictionary1)
    outputString+="\n"+str(dictionary2)
    outputString+="\n"+"-"*20
    if comparisons == 1:
        outputStringShort+="\n"+"-"*20
        outputStringShort+="\n"+str(dictionary1)
        outputStringShort+="\n"+str(dictionary2)
        outputStringShort+="\n"+"-"*20
    #print("-"*20)
    #print(dictionary1)
    #print(dictionary2)
    #print("-"*20)


    for key in dictionary1:
        if key in dictionary2:
            a = str(dictionary1.get(key))
            b = str(dictionary2.get(key))
            a = a.strip(" ")
            b = b.strip(" ")
            if len(a) == len(b):
                if a in [b]:
                    keysExactMatch.append(key)
                else:
                    keysExactNoMatch.append(key)
            else:
                keysLengthMismatch.append(key)
        else:
            keysNotFound1.append(key)

    for key in dictionary2:
        if key in dictionary1:
            a=1
        else:
            keysNotFound2.append(key)
    outputString+="\n"+"Keys Not found in "+str(y)+": "+str(keysNotFound1)
    outputString+="\n"+"Keys Not found in "+str(x)+": "+str(keysNotFound2)
    outputString+="\n"+"Keys with a length mismatch:"+str(keysLengthMismatch)
    if comparisons==1:
        outputStringShort+="\n"+"Keys Not found in "+str(y)+": "+str(keysNotFound1)
        outputStringShort+="\n"+"Keys Not found in "+str(x)+": "+str(keysNotFound2)
        outputStringShort+="\n"+"Keys with a length mismatch:"+str(keysLengthMismatch)

    #print("Keys Not found in file2:",keysNotFound1)
    #print("Keys Not found in file1:",keysNotFound2)
    #print("Keys with a length mismatch:",keysLengthMismatch)
    for i in keysLengthMismatch:
        #print("\nKey-",i," :","\nfile1:",dictionary1.get(i),"\nfile2:",dictionary2.get(i))
        outputString+="\n"+str(i)+" :"+"\n "+str(x)+": "+str(dictionary1.get(i))+"\n "+str(y)+": "+str(dictionary2.get(i))
        if comparisons==1:
            outputStringShort+="\n"+str(i)+" :"+"\n "+str(x)+": "+str(dictionary1.get(i))+"\n "+str(y)+": "+str(dictionary2.get(i))
    #print("EXACT Match keys:",keysExactMatch)
    outputString+="\n\nEXACT Match keys:"+str(keysExactMatch)+"\n"
    if comparisons==1:
        outputStringShort+="\n\nEXACT Match keys:"+str(keysExactMatch)+"\n"
    #print("Length Match but Exact NO Match keys:",keysExactNoMatch)
    outputString+="\nLength Match but Exact NO Match keys:"+str(keysExactNoMatch)
    if comparisons==1:
        outputStringShort+="\nLength Match but Exact NO Match keys:"+str(keysExactNoMatch)
    for i in keysExactNoMatch:
        #print("\nKey-",i," :","\nfile1:",dictionary1.get(i),"\nfile2:",dictionary2.get(i))
        outputString+="\n"+str(i)+" :"+"\n "+str(x)+": "+str(dictionary1.get(i))+"\n "+str(y)+": "+str(dictionary2.get(i))
        if comparisons==1:
            outputStringShort+="\n"+str(i)+" :"+"\n "+str(x)+": "+str(dictionary1.get(i))+"\n "+str(y)+": "+str(dictionary2.get(i))


if __name__ == '__main__':
    globalVariables()
    main()




