import sys
from functions import verilogFuncs
from functions import prepareCnf
import os

f = sys.argv[1]
target= sys.argv[3]
roll = int(sys.argv[2])

#target = "00"
#roll = 2

targetState = []
for bit in reversed(target):
	targetState.append(bit)
inputs = []
regs = []
outputs = []
wires = []
wordArrsave = verilogFuncs.parser(f)
cnfFile = open("example1.dimacs","w")
numberOfClauses = 0
numberOfVariables = 0
clauses = []
inputs = []
outputs = []
savedPS = []
savedNS = []

def initialize(varsDict,count,numC,numPS,roll):
	#cnfFile.write(f"p cnf {count} {(numC*roll)  +numPS + len(target)}\n")
	cnfFile.write("c initializing present state to 0 .......................................\n")
	for key in varsDict:
		if key[0]== "S":
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
			if key[0] =="S" and int(key[len(key)-1]) == i:
				if target[i] == "0":
					cnfFile.write(f"-{varsDict[key]+ ((roll-1)*count) } 0\n")
					break
				if target[i] =="1":
					cnfFile.write(f"{varsDict[key]+ ((roll-1)*count)} 0\n")
		i+=1


for index,word in enumerate(wordArrsave):
	if word =="//": #checking to see if part of the code was commented 
		while wordArrsave[index] !=";":
			wordArrsave.pop(index)
	rightSide=[]
	if word == "and" or word=="not":
		if word=="and":
			output1 = wordArrsave[index+2]
			input1 = wordArrsave[index+3]
			input2 = wordArrsave[index+4]
			clauses.append(["And",output1,input1,input2])
			if input1 not in inputs:
				inputs.append(input1)
			if input2 not in inputs:
				inputs.append(input2)
			if output1 not in outputs:
				outputs.append(output1)
		if word=="not":
			output1 = wordArrsave[index+2]
			input1 = wordArrsave[index+3]
			clauses.append(["not",output1,input1])
			if input1 not in inputs:
				inputs.append(input1)
			if output1 not in outputs:
				outputs.append(output1)
varsDict = {}
count = 1
varsA = inputs + outputs
my_set = set(varsA)
varsA = list(my_set)


for item in varsA:
	varsDict[item] = count
	count +=1
count = count -1
numC=0
for item in clauses:
	if item[0] == "And":
		numC +=3
	if item[0] == "not":
		numC+=2
numPS = 0
for key in varsDict:
	if key[0] == "S":
		numPS +=1

initialize(varsDict,count,numC,numPS,roll)
i = 0
while i<(roll):
	cnfFile.write(f"c Rolling number {i+1}------------------------\n")
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
        if key1[0] == "S" and key2[0] =="N":
            if key1[-1] == key2[-1]:
                relation.append([varsDict[key2],varsDict[key1]])
i = 0
print(varsDict)
cnfFile.write("c Transitions -------------------------------------------------\n")
while i<(roll-1):
	for item in relation:
		cnfFile.write(f"-{item[0] + i*count} {item[1] + (i+1)*count} 0\n ")
		cnfFile.write(f"{item[0] + i*count} -{item[1] + (i+1)*count} 0\n ")
	i +=1



cnfFile.close()
cmd = 'minisat example1.dimacs output.txt'
os.system(cmd)
