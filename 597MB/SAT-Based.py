import os
import sys

f = sys.argv[1]
target= sys.argv[3]
roll = int(sys.argv[2])

#target = "11"
#roll = 2
SArray =["S" + str(i) for i in range(32)]
NSArray = ["NS" + str(i) for i in range(32)]
targetState = []
for bit in reversed(target):
	targetState.append(bit)
inputs = []
regs = []
outputs = []
wires = []
def  parser(file): #function to parse the verilog file to create a word array

        wordArr = [] #an array of characters that appear in sequence
        wordArrsave = []
        count = 0
        index = 0
        with open(file, 'r') as f:
            for line in f:
                for word in line:
                    if word == ' ' or word == '\n' or word == '	' or word==',' or word=="(" or word==")": #creating a line of demarkation to seperate characters in sequence
                        command = ''.join(wordArr) #joining those characters into a str word that represents some kind of command
                        check = 0
                        if ';' in command and len(command)>1:
                            check =1
                            if command in wordArrsave:
                                wordArrsave.remove(command)
                                index -=1
                            command = command.replace(';',"")
                            wordArrsave.append(command)
                            if wordArrsave[index-1] !=None and wordArrsave[index-1] == ")":
                                wordArrsave[index] = ")"
                                wordArrsave[index-1]=command
                            index+=1
                            wordArrsave.append(';')
                            index+=1
                        if check == 0:
                            wordArrsave.append(command) #appending that command to my list of words that I will refer back to later
                            index +=1
                        wordArr = []
                        count +=1
                    else:
                        wordArr.append(word)

        #-----------------------Preparing the command array to leave only relevant information from the verilog file ----------------------------------------
        while '' in wordArrsave: #removing empty strings from the list
            wordArrsave.remove('')
        return wordArrsave

wordArrsave = parser(f)
cnfFile = open("example1.dimacs","w")
numberOfClauses = 0
numberOfVariables = 0
clauses = []
inputs = []
outputs = []
savedPS = []
savedNS = []

def initialize(varsDict,count,numC,numPS,roll):
	cnfFile.write(f"p cnf {count} {(numC*roll)  +numPS + len(target) + 2*roll}\n")
	cnfFile.write("c initializing present state to 0 .......................................--------------------------------\n")
	for key in varsDict:
		if key in SArray:
			cnfFile.write(f"-{varsDict[key]} 0 \n")
def andGate(varsDict,clause,roll):
	for key in varsDict:
		for index,item in enumerate(clause):
			if key == item:
				clause[index] = varsDict[key]
	cnfFile.write(f"{clause[2] + (roll*count)} -{clause[1] +(roll*count)} 0\n")
	cnfFile.write(f"{clause[3] + (roll*count)} -{clause[1] + (roll*count)} 0\n")
	cnfFile.write(f"-{clause[2] + (roll*count)} -{clause[3] + (roll*count)} {clause[1]+ (roll*count)} 0\n")
	return clause
def notGate(varsDict,clause,roll):
	for key in varsDict:
		for index,item in enumerate(clause):
			if key == item:
				clause[index] = varsDict[key]
	cnfFile.write(f"-{clause[2] + (roll*count)} -{clause[1] + (roll*count)} 0\n")
	cnfFile.write(f"{clause[2] + (roll*count)} {clause[1] + (roll*count)} 0\n")
	return clause
def targetState(target,varsDict,roll):
	cnfFile.write("c Target state ----------------------------\n")
	target = target[::-1]
	i = 0
	while i<=len(target) -1:
		for key in varsDict: 
			if key in NSArray and int(key[2:]) == i:
				if target[i] == "0":
					cnfFile.write(f"-{varsDict[key]+ ((roll-1)*count) } 0\n")
					break
				if target[i] =="1":
					cnfFile.write(f"{varsDict[key]+ ((roll-1)*count)} 0\n")
					break
		i+=1

varsA = []
for index,word in enumerate(wordArrsave):
	if word =="//": #checking to see if part of the code was commented 
		while wordArrsave[index] !=";":
			wordArrsave.pop(index)
	if word == "input" or word=="output" or word =="wire" or word =="reg":
		index2 = index +1
		while wordArrsave[index2] != ";":
			varsA.append(wordArrsave[index2])
			index2 +=1
	if word=="and":
		output1 = wordArrsave[index+2]
		input1 = wordArrsave[index+3]
		input2 = wordArrsave[index+4]
		clauses.append(["And",output1,input1,input2])
	if word=="not":
		output1 = wordArrsave[index+2]
		input1 = wordArrsave[index+3]
		clauses.append(["not",output1,input1])
varsDict = {}
count = 1
varsA.remove("clock")
for item in varsA:
	varsDict[item] = count
	count +=1
count = len(varsA)
numC=0
for item in clauses:
	if item[0] == "And":
		numC +=3
	if item[0] == "not":
		numC+=2
numPS = 0
for key in varsDict:
	if key in SArray:
		numPS +=1
initialize(varsDict,len(varsA),numC,numPS,roll)
i = 0
while i<(roll):
	cnfFile.write(f"c Rolling number {i+1}------------------------------------------------------------------------------------\n")
	for index,clause in enumerate(clauses):
		if clause[0] == "And":
			cnfFile.write("c And Gate....................................\n")
			clauses[index] = andGate(varsDict,clause,i)
		if clause[0] == "not":
			cnfFile.write("c not Gate....................................\n")
			notGate(varsDict,clause,i)
	i +=1
targetState(target,varsDict,roll)

relation = []
for key1 in varsDict:
    for key2 in varsDict:
        if key1 in SArray and key2 in NSArray:
            if key1[1:] == key2[2:]:
                relation.append([varsDict[key2],varsDict[key1]])
i = 0
cnfFile.write("c Transitions ------------------------------------------------------------------------------------------------\n")
while i<(roll-1):
	for item in relation:
		cnfFile.write(f"-{item[0] + i*count} {item[1] + (i+1)*count} 0\n ")
		cnfFile.write(f"{item[0] + i*count} -{item[1] + (i+1)*count} 0\n ")
	i +=1
cnfFile.close()
cmd = 'time minisat example1.dimacs output.txt'
os.system(cmd)
