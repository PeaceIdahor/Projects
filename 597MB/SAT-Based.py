import sys
from functions import verilogFuncs
from functions import prepareCnf
"""
f = sys.argv[1]
target= sys.argv[3]
roll = int(sys.argv[2])
"""
target = "10"
roll = 1
print(roll)
targetState = []
for bit in reversed(target):
	targetState.append(bit)
inputs = []
regs = []
outputs = []
wires = []
wordArrsave = verilogFuncs.parser("ex1.v")
cnfFile = open("example1.dimacs","a")
numberOfClauses = 0
numberOfVariables = 0
clauses = []
for index,word in enumerate(wordArrsave):
	if word =="//": #checking to see if part of the code was commented 
		while wordArrsave[index] !=";":
			wordArrsave.pop(index)
	rightSide=[]
	if word == "reg": # the only part I care about are the assign statement
		index2 = index+1
		while wordArrsave[index2] != ";": #getting the rightside of the assign statement
			regs.append(wordArrsave[index2])
			index2 +=1
	elif word == "input":
		index2 = index +1
		while wordArrsave[index2] != ";": #getting the rightside of the assign statement
			inputs.append(wordArrsave[index2])
			index2 +=1
	elif word == "output":
		index2 = index +1
		while wordArrsave[index2] != ";": #getting the rightside of the assign statement
			outputs.append(wordArrsave[index2])
			index2 +=1

	elif word == "wire":
		index2 = index +1
		while wordArrsave[index2] != ";": #getting the rightside of the assign statement
			wires.append(wordArrsave[index2])
			index2 +=1
	elif word == "and" or word=="not":
		if word=="and":
			output1 = wordArrsave[index+2]
			input1 = wordArrsave[index+3]
			input2 = wordArrsave[index+4]
			clauses.append(["And",output1,input1,input2])
		if word=="not":
			output1 = wordArrsave[index+2]
			input1 = wordArrsave[index+3]
			clauses.append(["not",output1,input1])

inputsDict = {}
regsDict = {}
outputsDict = {}
wiresDict = {}

cnfVar = 0
for item in inputs:
	inputsDict[item] = cnfVar
	cnfVar +=1
	numberOfVariables +=1
for item in regs:
	regsDict[item] = cnfVar
	cnfVar +=1
	numberOfVariables +=1
for item in wires:
	wiresDict[item] = cnfVar
	cnfVar +=1
	numberOfVariables +=1
for item in outputs:
	outputsDict[item] = cnfVar
	cnfVar +=1
	numberOfVariables +=1
#print(inputsDict)
#print(regsDict)
#print(outputsDict)
#print(wiresDict)
#print(wordArrsave)
for arrays in clauses:
	numberOfClauses +=1
for index,clause in enumerate(clauses):
	for index2,item in enumerate(clause):
		for key in inputsDict:
			if key == item:
				clauses[index][index2] = inputsDict[key]
				break
		for key in regsDict:
			if key == item:
				clauses[index][index2] = regsDict[key]
				break
		for key in outputsDict:
			if key == item:
				clauses[index][index2] = outputsDict[key]
				break
		for key in wiresDict:
			if key == item:
				clauses[index][index2] = wiresDict[key]
				if key[0] == "N":
					index3 = int(key[len(key)-1])
					clauses.append(["N",wiresDict[key],int(targetState[index3])])
print(clauses)

justAVar = prepareCnf(cnfFile)
justAVar.openDot(numberOfVariables,numberOfClauses,regsDict,roll)

justAVar.write(clauses,int(roll))
justAVar.writeTransition(regsDict,wiresDict,roll)
