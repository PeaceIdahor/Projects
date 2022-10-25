
f = open("verilogTest2.v")
wordArr = [] #an array of characters that appear in sequence
wordArrsave = []
count = 0

for line in f:
	for word in line:
		if word == ' ' or word == '(' or word == ')' or word == '\n' or word == '	' or word==',' : #creating a line of demarkation to seperate characters in sequence
			command = ''.join(wordArr) #joining those characters into a str word that represents some kind of command
			if '!' in command:
				command = command.replace('!',"")
				wordArrsave.append('!')
				wordArrsave.append(command)
			if '//' in command:
				command = command.replace('//',"")
				wordArrsave.append('//')
				wordArrsave.append(command)
			if ';' in command:
				command = command.replace(';',"")
				wordArrsave.append(command)
				wordArrsave.append(';')
			else:
				wordArrsave.append(command) #appending that command to my list of words that I will refer back to later
			wordArr = []
			count +=1
		else:
			wordArr.append(word)

#-----------------------Preparing the command array to leave only relevant information from the verilog file ----------------------------------------
while '' in wordArrsave: #removing empty strings from the list
	wordArrsave.remove('')


fDot = open("Translate.dot","a")
fDot.truncate(0)
fDot.write("digraph test{\n")
called=0

#this is my function for writing two nodes connected by an edge to the dot file
def writeNode(inN,shape):
	fDot.write(f'"{inN}" [shape={shape}]\n')

def writeEdgeNode(inN,outN="",label=""): 
	if label == "":
		fDot.write(f'"{inN}" -> "{outN}" \n')
	else:
		fDot.write(f'"{inN}" -> "{outN}" Label={label}\n')
def createSubgraph(input):
	fDot.write("subgraph{\nrand=same;")
	for item in input:
		fDot.write(f"{item};")
	fDot.write("\n}")


outputArr = []
bufferArr = []
inputArr = []

outputD = {}
bufferD = {}
inputD = {}
#trying to get the amounts of outputs defined in the v file
count1=0

"""
in this functiono I am geting the right and leftside of the inputs 
Then I am writing each input to the dot file 
"""
"""
def getValue(operationin,rightSide,outputN):
	rightside2 = []
	leftside2 = []
	index = 0
	operation = operationin+f"_{count}"
	outputD.append(outputN)
	while inputs[index]!=operationin:
		rightside2.append(inputs[index])
		index +=1
	index2 = index + 1
	while inputs[index2] !=";":
		leftside2.append(inputs[index2])
		#inputArr.append(inputs[index2])
		index2 +=1
	writeNode(operation,"square")
	for item in rightside2:
		if item not in outputD:
			writeNode(item,"invtriangle")
			writeEdgeNode(item,operation)
	for item in leftside2:
		if item not in outputD:
			writeNode(item, "invtriangle")
			writeEdgeNode(item,operation)
	if count == count1:
		writeNode(outputN,"triangle")
		writeEdgeNode(operation,outputN)
"""

def getValue(operationin,rightSide,outputN):
	operationin = operationin + f"_{outputD[outputN]}"
	outputN = outputN + f"_{outputD[outputN]}"
	writeNode(operationin,"square")
	for item in rightSide:
		if item in inputD and item not in bufferD:
			item = item + f"_{inputD[item]}"
			writeNode(item,"invtriangle")
			writeEdgeNode(item,operationin)
		if item in inputD and item in bufferD:
			item = item + f"_{outputD[item]}"
			writeEdgeNode(item,operationin)
	writeNode(outputN,"triangle")
	print(operationin)
	print(outputN)
	#check to see if the outputN is in the buffer dict before creating an edge to that node
	#then connect the edge to the output of that buffer node and not the buffer itself
	#make the buffer name the label of the edge from the current node to the actual output node
	writeEdgeNode(operationin,outputN)

"""
In this section I am going through my words array and checking for assign statements
then I am saving the values before sending it to the get value funciton
"""

#the countequal var is to check to see if I have the last output so it can be represented properly

count = 0
for index,word in enumerate(wordArrsave):
	indexMaster = index
	if word =="//": #checking to see if part of the code was commented 
		while wordArrsave[index] !=";":
			wordArrsave.pop(index)
	rightSide=[]
	if word == "assign":
		outputD[wordArrsave[index+1]] = indexMaster
		outputN = wordArrsave[index+1]
		index2=index+3
		while wordArrsave[index2] != ";":
			rightSide.append(wordArrsave[index2])
			index2 +=1
		rightSide.append(";")
	for index,item in enumerate(rightSide):
		if item == "&": 
			count+=1
			index2 = rightSide.index("&")
			rightSide.pop(index2)
			index2 = rightSide.index(";")
			rightSide.pop(index2)
			for item in rightSide:
				if item in outputD:
					inputD[item] = indexMaster
					bufferD[item] = indexMaster
				else:
					inputD[item] = indexMaster
			getValue("&",rightSide,outputN)
			#getValue("~",rightSide,outputN,count)
	if word =="endmodule":
		fDot.write("}")
#trying to figure out how to iterate through the dictionary and call the get value fuction with the items in the dictionary after all the values
#in the verilog file has been parsed
print(inputD)
print(bufferD)
print(outputD)
#print(inputArr)
#print(bufferArr)
#print(outputArr)

