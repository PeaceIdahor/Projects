from functions import verilogFuncs
from functions import prepareDot,simulationInput
import sys
f = sys.argv[1]
wordArrsave = verilogFuncs.parser(f) #extracting important information from my verilog file


#wordArrsave = verilogFuncs.parser("f2-aig.v")
dotFile = open("Translate.dot","a")
dotfile = prepareDot(dotFile)
dotfile.openDot()#opening a dot file

#outputA,outinA,bufferA,buffinA,inputA,inpinA = verilogFuncs.populateA(wordArrsave)
inputA = []
inputPrimary = []
bufferA = [] #buffer array containing the intermediates values that are not inputs or outputs
outputA = []
operationsA = [] #array containing all the operations and the inputs and outputs to those operations
notDict = []
notTrack = {}
"""
This function gives an initial view of the resulting output of each assign statement in it's simplest form
So given an assign statement such as
assign c = b & f;
the strip function returns b&f
"""
def strip(array):
	while "(" in array:
		array.remove("(")
	while ")" in array:
		array.remove(")")
	return ''.join(array)

"""
This returnOut function does most of the translating of the verilog. It is a recursive function that receives as 
inputs,
Array:  An array containing the operation performed in the assign statement
indexMaster: A number used to differenciate between different operations of the same type
outputE: the result of the strip function showing what the output of the returnOut function should look like
outputN: the variable the output of the assign statement is assigned to
"""
def returnOut(Array,indexMaster,outputE,outputN=""):
	if len(Array) == 1:
		for indexItem,items in enumerate(operationsA):
			if items[2] == Array[0]:
				operationsA[indexItem][2] = outputN
				outputA.append(outputN)
				outputA.remove(Array[0])
	if "(" in Array:
		openind = []
		closeind = []
		for index,item in enumerate(Array):
			if item =="(":
				openind.append(index)
			if item ==")":
				closeind.append(index)
		i = len(openind)
		while((i - len(openind))<=i):
			indexMaster +=1
			if "(" in Array:
				sig = 0
				lp = openind[0]
				rp = closeind[0]
				rightSide = Array[lp+1:rp]
			else:
				sig = 1
				rightSide = Array
			operationin,Array2,out = returnOut(rightSide,indexMaster,outputE,outputN)
			bufferA.append(out)
			if sig == 0:
				while rp >= lp:
					Array.pop(rp)
					rp -=1
				Array.insert(lp,out)
			openind = []
			closeind = []
			for index,item in enumerate(Array):
				if item =="(":
					openind.append(index)
				if item ==")":
					closeind.append(index)
			if len(openind)==0 and len(Array) !=1 :
				for item in Array:
					if item == "&" or item == "|" or item =="^":
						indexMaster +=1
						lp = Array.index(item)-1
						rp = Array.index(item)+2
						rightSide = Array[lp:rp]
						operationin,Array2,out = returnOut(rightSide,indexMaster,outputE,outputN)
						rp2 = rp-1
						while (rp2) >= lp:
							Array.pop(rp2)
							rp2 -=1
						Array.insert(lp,out)
			if out == outputE:
				bufferA.remove(out)
				#outputA.append(out)
				#operationsA.append([operationin,Array2,outputN])
				return out
			
	else:
		if "&" in Array and "~" not in Array:
			operationin = "And" + f"_{indexMaster}"
			out= f"{Array[0]}" + "&" + f"{Array[2]}"
			inputA.append(Array[0])
			if Array[0] in outputA:
				bufferA.append(Array[0])
			inputA.append(Array[2])
			if Array[2] in outputA:
				bufferA.append(Array[2])
			Array.pop(Array.index("&"))
			bufferA.append(out)
			if out == outputE:
				outputA.append(outputN)
				operationsA.append([operationin,Array,outputN])
			else:
				operationsA.append([operationin,Array,out])
			return operationin,Array,out
		if "|" in Array and "~" not in Array:
			operationin = "or" + f"_{indexMaster}"
			out= f"{Array[0]}" + "|" + f"{Array[2]}"
			inputA.append(Array[0])
			if Array[0] in outputA:
				bufferA.append(Array[0])
			inputA.append(Array[2])
			if Array[2] in outputA:
				bufferA.append(Array[2])
			Array.pop(Array.index("|"))
			bufferA.append(out)
			if out == outputE:
				outputA.append(outputN)
				operationsA.append([operationin,Array,outputN])
			else:
				operationsA.append([operationin,Array,out])
			return operationin,Array,out
		if "^" in Array and "~" not in Array:
			operationin = "xor" + f"_{indexMaster}"
			out= f"{Array[0]}" + "^" + f"{Array[2]}"
			inputA.append(Array[0])
			if Array[0] in outputA:
				bufferA.append(Array[0])
			inputA.append(Array[2])
			if Array[2] in outputA:
				bufferA.append(Array[2])
			Array.pop(Array.index("^"))
			bufferA.append(out)
			if out == outputE:
				outputA.append(outputN)
				operationsA.append([operationin,Array,outputN])
			else:
				operationsA.append([operationin,Array,out])
			return operationin,Array,out	
		if "~" in Array:
			operationin = "not" + f"_{indexMaster}"
			indexMaster +=1
			indexV = Array[Array.index("~")+1]
			Arrayin = [indexV]
			out= "~" + f"{indexV}"
			if out in bufferA:
				operationin = notTrack[out]
			else:
				bufferA.append(out)
				notTrack[out] = operationin 
			notDict.append([out,indexMaster])
			inputA.append(indexV)
			if indexV in outputA:
				bufferA.append(indexV)
			Array.pop(Array.index("~"))
			"""
			Trying to fix the bug where multiple lines are created to a node
			"""
			operationsA.append([operationin,Arrayin,out])
			if len(Array) >1:
				#bufferA.append(out)
				indexf = Array.index(indexV)
				Array.pop(indexf)
				Array.insert(indexf,out)
				out = returnOut(Array,indexMaster,outputE,outputN)
				return out
			if out == outputE:
				outputA.append(outputN)
				operationsA.append([operationin,Array,outputN])
			else:
				operationsA.append([operationin,Array,out])
			return operationin,Array,out	
		if "~&"	 in Array:
			operationin = "Nand" + f"_{indexMaster}"
			out= f"{Array[0]}" + "~&" + f"{Array[2]}"
			inputA.append(Array[0])
			if Array[0] in outputA:
				bufferA.append(Array[0])
			inputA.append(Array[2])
			if Array[2] in outputA:
				bufferA.append(Array[2])
			Array.pop(Array.index("~&"))
			bufferA.append(out)
			if out == outputE:
				outputA.append(outputN)
				operationsA.append([operationin,Array,outputN])
			else:
				operationsA.append([operationin,Array,out])
			return operationin,Array,out		
		if "~|" in Array:
			operationin = "Nor" + f"_{indexMaster}"
			out= f"{Array[0]}" + "~|" + f"{Array[2]}"
			inputA.append(Array[0])
			if Array[0] in outputA:
				bufferA.append(Array[0])
			inputA.append(Array[2])
			if Array[2] in outputA:
				bufferA.append(Array[2])
			Array.pop(Array.index("~|"))
			bufferA.append(out)
			if out == outputE:
				outputA.append(outputN)
				operationsA.append([operationin,Array,outputN])
			else:
				operationsA.append([operationin,Array,out])
			return operationin,Array,out	
		if "~^" in Array:
			operationin = "Xnor" + f"_{indexMaster}"
			out= f"{Array[0]}" + "~^" + f"{Array[2]}"
			inputA.append(Array[0])
			if Array[0] in outputA:
				bufferA.append(Array[0])
			inputA.append(Array[2])
			if Array[2] in outputA:
				bufferA.append(Array[2])
			Array.pop(Array.index("~^"))
			bufferA.append(out)
			if out == outputE:
				outputA.append(outputN)
				operationsA.append([operationin,Array,outputN])
			else:
				operationsA.append([operationin,Array,out])
			return operationin,Array,out

"""
This for loop is used to search for assign statements and then call the returnOut function with the previously 
specified perameters.
It also ignores any commented lined in the verilog script.
You can comment lines of verilog, but you cannot add commented lines that are not verilog
"""
for index,word in enumerate(wordArrsave):
	if word =="//": #checking to see if part of the code was commented 
		while wordArrsave[index] !=";":
			wordArrsave.pop(index)
	rightSide=[]
	if word == "assign": # the only part I care about are the assign statements
		indexMaster = index #get the index of the assign statement
		index2=index+3
		outputN = wordArrsave[index + 1]
		while wordArrsave[index2] != ";": #getting the rightside of the assign statement
			rightSide.append(wordArrsave[index2])
			index2 +=1
		rightside2 = rightSide.copy()
		outputE = strip(rightside2)
		Array = returnOut(rightSide,indexMaster,outputE,outputN)
	if word == "input":
		indexInput = index +1
		while wordArrsave[indexInput] != ";":
			inputPrimary.append(wordArrsave[indexInput])
			indexInput +=1
		#returnOut(Array,indexMaster)

#checking to see if the visual representation is in debug mode or not
print(inputA)
val = input("Debug mode on ? [y/n] :")

if val == "y" or val == "Y":
	labelon = 1
	print("Debug Mode on")
elif val == "n" or val == "N":
	labelon=0
	print("Debug Mode off")
else:
	raise Exception("Sorry Y or N only")

#getting actual inputs from the user in terms of 0 or 1
inputSpecifiedArray = {}
specifyInputs = input("Specifying inputs? [y/n] :")
if specifyInputs == "y" or specifyInputs == "Y":
	inputon = 1
	for item in inputPrimary:
		inputSpecified = input(f"{item}: ")
		if inputSpecified =="0" or inputSpecified == "1":
			inputSpecifiedArray[item] = inputSpecified
		else:
			raise Exception("Input must be 0 or 1")
elif specifyInputs == "n" or specifyInputs == "N":
	inputon = 0
else:
	raise Exception("Sorry Y or N only")
def simulation(operationsA, inputSpecifiedArray):
	for index1,items in enumerate(operationsA):
		operationsA[index1].append([])
		operationsA[index1].append([])
		for inputs in items[1]:
			for key in inputSpecifiedArray:
				if inputs == key:
					operationsA[index1][3].append(inputSpecifiedArray[key])
					if operationsA[index1][0][0] == "A" and len(operationsA[index1][3])>1:
						inputSpecifiedArray[operationsA[index1][2]] = simulationInput.and_gate(operationsA[index1][3][0],operationsA[index1][3][1])
						operationsA[index1][4].append(inputSpecifiedArray[operationsA[index1][2]])
						break
					if operationsA[index1][0][0] == "n":
						inputSpecifiedArray[operationsA[index1][2]] = simulationInput.not_gate(operationsA[index1][3][0])
						operationsA[index1][4].append(inputSpecifiedArray[operationsA[index1][2]])
						break
rankDict = {}
OutputRank = {}
Rank = 1
for item in inputA:
	if item not in bufferA and Rank not in rankDict:
		rankDict[Rank] = [item]
	elif item not in bufferA and item not in rankDict[Rank]:
		rankDict[Rank].append(item)
	elif item not in bufferA and item in rankDict[Rank]:
		# do nothing since the item is already in the list for the current rank
		pass
	else:
		pass

for arrays in operationsA:
	rankDictCp = rankDict.copy()
	if len(arrays[1])==1:
		for key, value in rankDictCp.items():
			if arrays[1][0] in value and key+1 not in rankDictCp:
				rankDict[key+1] = []
				OutputRank[key+1] = []
				rankDict[key+1].append(arrays)
				OutputRank[key+1].append(arrays[2])
			elif arrays[1][0] in value and key+1 in rankDictCp:
				rankDict[key+1].append(arrays)
				OutputRank[key+1].append(arrays[2])
	if len(arrays[1])>1:
		for key, value in rankDictCp.items():
			if arrays[1][0] in value and arrays[1][1] in value:
				if key+1 in rankDictCp:
					rankDict[key+1].append(arrays)
					OutputRank[key+1].append(arrays[2])
				else:
					rankDict[key+1] = []
					OutputRank[key+1] = []
					rankDict[key+1].append(arrays)
					OutputRank[key+1].append(arrays[2])
Rank = max(rankDict) +1
for item in outputA:
	if item not in bufferA and Rank not in rankDict:
		rankDict[Rank] = [item]
	elif item not in bufferA and item not in rankDict[Rank]:
		rankDict[Rank].append(item)
	elif item not in bufferA and item in rankDict[Rank]:
		# do nothing since the item is already in the list for the current rank
		pass
	else:
		pass

dotfile.setup(rankDict)
#calling the visual representation functions that write to the dot file
verilogFuncs.processVisual(bufferA,operationsA,inputA)
if inputon ==1:
	simulation(operationsA,inputSpecifiedArray)
operationsDict = {}
"""
for index,arrays in enumerate(operationsA):
	if operationsA[index][0] in operationsDict:
		operationsA.pop(index)
	operationsDict[operationsA[index][0]] = 0
	"""


print(rankDict)
print(OutputRank)
verilogFuncs.writeVisuals(dotFile,operationsA,bufferA,labelon,inputon)
dotfile.endFile() #closing the dotfile


#print(wordArrsave)
#print(operationsA)
#print(inputSpecifiedArray)
#print(bufferA)
#print(inputPrimary)
