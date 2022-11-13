from operator import indexOf

f = open("verilogTest2.v")
wordArr = [] #an array of characters that appear in sequence
wordArrsave = []
count = 0

for line in f:
	for word in line:
		if word == ' ' or word == '\n' or word == '	' or word==',': #creating a line of demarkation to seperate characters in sequence
			command = ''.join(wordArr) #joining those characters into a str word that represents some kind of command
			if '!' in command:
				command = command.replace('!',"")
				wordArrsave.append('!')
				wordArrsave.append(command)
			elif '//' in command:
				command = command.replace('//',"")
				wordArrsave.append('//')
				wordArrsave.append(command)
			elif ';' in command:
				command = command.replace(';',"")
				wordArrsave.append(command)
				wordArrsave.append(';')
			elif '(' in command:
				command = command.replace('(',"")
				wordArrsave.append('(')
				wordArrsave.append(command)
			elif ')' in command:
				command = command.replace(')',"")
				wordArrsave.append(command)
				wordArrsave.append(')')
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
def setup():
	#fDot.write('splines="ortho"\n')
	fDot.write('subgraph inputs{ rank="same"')
	for item in inputA:
		if item not in bufferA:
			if "(" in item:
				item = item.replace("(","")
			if ")" in item:
				item = item.replace(")","")
			fDot.write(f' "{item}" ')
	fDot.write('}\n')

	fDot.write('subgraph outputs{rank="same"')
	for item in outputA:
		if item not in bufferA:
			if "(" in item:
				item = item.replace("(","")
			if ")" in item:
				item = item.replace(")","")
			print(item)
			fDot.write(f' "{item}" ')
	fDot.write('}\n')

def writeNode(inN,shape):
	fDot.write(f'"{inN}" [shape={shape}]\n')

def writeEdgeNode(inN,outN="",label=""): 
	if label == "":
		fDot.write(f'"{inN}" -> "{outN}" \n')
	else:
		fDot.write(f'"{inN}" -> "{outN}" [label="{label}"]\n')
def createSubgraph(input):
	fDot.write("subgraph{\nrand=same;")
	for item in input:
		fDot.write(f"{item};")
	fDot.write("\n}")
def add_values_in_dict(sample_dict, key, list_of_values):
    ''' Append multiple values to a key in 
        the given dictionary '''
    if key not in sample_dict:
        sample_dict[key] = list()
    sample_dict[key].extend(list_of_values)
    return sample_dict
def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs
outputA = []
outinA = []
bufferA = []
buffinA = []
inputA = []
inpinA = []
operationsA = []
operationsA2 = []
operinA =[]


#trying to get the amounts of outputs defined in the v file
count1=0

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
		outputA.append(wordArrsave[index+1])
		outinA.append(indexMaster)
		index2=index+3		
		while wordArrsave[index2] != ";":
			rightSide.append(wordArrsave[index2])
			index2 +=1
	for index,item in enumerate(rightSide):
		if item in outputA and item !="&" and item !="!" and item !="|" and item !="^":
			inputA.append(item)
			inpinA.append(indexMaster)
			bufferA.append(item)
			buffinA.append(indexMaster)
		else:
			if item !="&" and item !="!" and item !="|" and item !="^" and item !="(" and item !=")":
				if ";" not in item:
					inputA.append(item)
					inpinA.append(indexMaster)
			

setup()
"""
populating the operations array
"""

for index,word in enumerate(wordArrsave):
	if word =="//": #checking to see if part of the code was commented 
		while wordArrsave[index] !=";":
			wordArrsave.pop(index)
	rightSide=[]
	if word == "assign":
		indexMaster = index
		index2=index+3
		while wordArrsave[index2] != ";":
			rightSide.append(wordArrsave[index2])
			index2 +=1
	if "&" in rightSide:
		connections = []
		perenthesisA = []
		operationin = "And" + f"_{indexMaster}"
		out= outputA[outinA.index(indexMaster)]
		if "(" in rightSide and ")" in rightSide:
			rp = rightSide.index("(")
			lp = rightSide.index(")")
			while rp != lp-1:
				perenthesisA.append(rightSide[rp+1])
				rp +=1
		if "&" in perenthesisA:
			perenthesisA.pop(perenthesisA.index("&"))
			operationin = "And" + f"_{indexMaster}"
			#writeNode(operationin,"square")
			out= f"{perenthesisA[0]}" + "&" + f"{perenthesisA[1]}"
			bufferA.append(out)
			operationsA2.append([operationin,perenthesisA,out])
		elif len(perenthesisA) > 0 and "&" not in perenthesisA and "&" in rightSide:
			perenthesisA.pop(1)
			for item in operationsA2:
				if item[1] == perenthesisA:
					connections.append(item[2])
			indexes = list_duplicates_of(inpinA,indexMaster)
			for item in indexes:
				if inputA[item] not in perenthesisA:
					connections.append(inputA[item])
			operationsA2.append([operationin,connections,out])
		else:
			#writeNode(operationin,"square")
			indexes = list_duplicates_of(inpinA,indexMaster)
			for item in indexes:
				connections.append(inputA[item])
			operationsA2.append([operationin,connections,out])
	if "!" in rightSide:
		indexofItem = rightSide.index("!") + 1
		connections = [rightSide[indexofItem]]
		operationin = "Not" + f"_{indexMaster}"
		#writeNode(operationin,"square")
		indexes = list_duplicates_of(inpinA,indexMaster)
		out= rightSide[indexofItem] +"^"
		operationsA2.append([operationin,connections,out])
		for items in operationsA:
			if items[2] != out:
				for indexItem,item in enumerate(items[1]):
					if item == rightSide[indexofItem]:
						bufferA.append(out)
						items[1][indexItem]= out
	if "|" in rightSide:
		perenthesisA = []
		connections = []
		out= outputA[outinA.index(indexMaster)]	
		operationin = "Or" + f"_{indexMaster}"
		if "(" in rightSide and ")" in rightSide:
			rp = rightSide.index("(")
			lp = rightSide.index(")")
			while rp != lp-1:
				perenthesisA.append(rightSide[rp+1])
				rp +=1
		if "|" in perenthesisA:
			perenthesisA.pop(perenthesisA.index("|"))
			operationin = "Or" + f"_{indexMaster}"
			out= f"{perenthesisA[0]}" + "|" + f"{perenthesisA[1]}"
			operationsA2.append([operationin,perenthesisA,out])
		elif len(perenthesisA)> 0 and "|" not in perenthesisA and "|" in rightSide:
			perenthesisA.pop(1)
			for item in operationsA2:
				if item[1] == perenthesisA:
					connections.append(item[2])
			indexes = list_duplicates_of(inpinA,indexMaster)
			for item in indexes:
				if inputA[item] not in perenthesisA:
					connections.append(inputA[item])
			operationsA2.append([operationin,connections,out])
		else:
			indexes = list_duplicates_of(inpinA,indexMaster)
			out= outputA[outinA.index(indexMaster)]
			for item in indexes:
				connections.append(inputA[item])
			operationsA2.append([operationin,connections,out])
	if "^" in rightSide:
		perenthesisA = []
		connections = []
		out= outputA[outinA.index(indexMaster)]	
		operationin = "Xor" + f"_{indexMaster}"
		if "(" in rightSide and ")" in rightSide:
			rp = rightSide.index("(")
			lp = rightSide.index(")")
			while rp != lp-1:
				perenthesisA.append(rightSide[rp+1])
				rp +=1
		if "|" in perenthesisA:
			perenthesisA.pop(perenthesisA.index("|"))
			operationin = "Xor" + f"_{indexMaster}"
			out= f"{perenthesisA[0]}" + "^" + f"{perenthesisA[1]}"
			bufferA.append(out)
			operationsA2.append([operationin,perenthesisA,out])
		elif len(perenthesisA)> 0 and "^" not in perenthesisA and "^" in rightSide:
			perenthesisA.pop(1)
			for item in operationsA2:
				if item[1] == perenthesisA:
					connections.append(item[2])
			indexes = list_duplicates_of(inpinA,indexMaster)
			for item in indexes:
				if inputA[item] not in perenthesisA:
					connections.append(inputA[item])
			operationsA2.append([operationin,connections,out])
		else:
			indexes = list_duplicates_of(inpinA,indexMaster)
			out= outputA[outinA.index(indexMaster)]
			for item in indexes:
				connections.append(inputA[item])
			operationsA2.append([operationin,connections,out])
	
"""
adjusting the operations array 
"""
for index,word in enumerate(wordArrsave):
	if word =="//": #checking to see if part of the code was commented 
		while wordArrsave[index] !=";":
			wordArrsave.pop(index)
	rightSide=[]
	if word == "assign":
		indexMaster = index
		index2=index+3
		while wordArrsave[index2] != ";":
			rightSide.append(wordArrsave[index2])
			index2 +=1
	if "&" in rightSide:
		connections = []
		perenthesisA = []
		operationin = "And" + f"_{indexMaster}"
		out= outputA[outinA.index(indexMaster)]
		if "(" in rightSide and ")" in rightSide:
			rp = rightSide.index("(")
			lp = rightSide.index(")")
			while rp != lp-1:
				perenthesisA.append(rightSide[rp+1])
				rp +=1
		if "&" in perenthesisA:
			perenthesisA.pop(perenthesisA.index("&"))
			operationin = "And" + f"_{indexMaster}"
			#writeNode(operationin,"square")
			out= f"{perenthesisA[0]}" + "&" + f"{perenthesisA[1]}"
			bufferA.append(out)
			operationsA.append([operationin,perenthesisA,out])
		elif len(perenthesisA) > 0 and "&" not in perenthesisA and "&" in rightSide:
			perenthesisA.pop(1)
			for item in operationsA2:
				if item[1] == perenthesisA:
					connections.append(item[2])
			indexes = list_duplicates_of(inpinA,indexMaster)
			for item in indexes:
				if inputA[item] not in perenthesisA:
					connections.append(inputA[item])
			operationsA.append([operationin,connections,out])
		else:
			#writeNode(operationin,"square")
			indexes = list_duplicates_of(inpinA,indexMaster)
			for item in indexes:
				connections.append(inputA[item])
			operationsA.append([operationin,connections,out])
	if "!" in rightSide:
		indexofItem = rightSide.index("!") + 1
		connections = [rightSide[indexofItem]]
		operationin = "Not" + f"_{indexMaster}"
		#writeNode(operationin,"square")
		indexes = list_duplicates_of(inpinA,indexMaster)
		out= "!"+rightSide[indexofItem]
		operationsA.append([operationin,connections,out])
		for items in operationsA:
			if items[2] != out:
				for indexItem,item in enumerate(items[1]):
					if item == rightSide[indexofItem]:
						bufferA.append(out)
						items[1][indexItem]= out
	if "|" in rightSide:
		perenthesisA = []
		connections = []
		out= outputA[outinA.index(indexMaster)]	
		operationin = "Or" + f"_{indexMaster}"
		if "(" in rightSide and ")" in rightSide:
			rp = rightSide.index("(")
			lp = rightSide.index(")")
			while rp != lp-1:
				perenthesisA.append(rightSide[rp+1])
				rp +=1
		if "|" in perenthesisA:
			perenthesisA.pop(perenthesisA.index("|"))
			operationin = "Or" + f"_{indexMaster}"
			out= f"{perenthesisA[0]}" + "|" + f"{perenthesisA[1]}"
			bufferA.append(out)
			operationsA.append([operationin,perenthesisA,out])
		elif len(perenthesisA)> 0 and "|" not in perenthesisA and "|" in rightSide:
			perenthesisA.pop(1)
			for item in operationsA2:
				if item[1] == perenthesisA:
					connections.append(item[2])
			indexes = list_duplicates_of(inpinA,indexMaster)
			for item in indexes:
				if inputA[item] not in perenthesisA:
					connections.append(inputA[item])
			operationsA.append([operationin,connections,out])
		else:
			indexes = list_duplicates_of(inpinA,indexMaster)
			out= outputA[outinA.index(indexMaster)]
			for item in indexes:
				connections.append(inputA[item])
			operationsA.append([operationin,connections,out])
	if "^" in rightSide:
		perenthesisA = []
		connections = []
		out= outputA[outinA.index(indexMaster)]	
		operationin = "Xor" + f"_{indexMaster}"
		if "(" in rightSide and ")" in rightSide:
			rp = rightSide.index("(")
			lp = rightSide.index(")")
			while rp != lp-1:
				perenthesisA.append(rightSide[rp+1])
				rp +=1
		if "|" in perenthesisA:
			perenthesisA.pop(perenthesisA.index("|"))
			operationin = "Xor" + f"_{indexMaster}"
			out= f"{perenthesisA[0]}" + "^" + f"{perenthesisA[1]}"
			bufferA.append(out)
			operationsA.append([operationin,perenthesisA,out])
		elif len(perenthesisA)> 0 and "^" not in perenthesisA and "^" in rightSide:
			perenthesisA.pop(1)
			for item in operationsA2:
				if item[1] == perenthesisA:
					connections.append(item[2])
			indexes = list_duplicates_of(inpinA,indexMaster)
			for item in indexes:
				if inputA[item] not in perenthesisA:
					connections.append(inputA[item])
			operationsA.append([operationin,connections,out])
		else:
			indexes = list_duplicates_of(inpinA,indexMaster)
			out= outputA[outinA.index(indexMaster)]
			for item in indexes:
				connections.append(inputA[item])
			operationsA.append([operationin,connections,out])
#preparing to accept user inputs 
for index,item in enumerate(bufferA):
	if "(" in item:
		bufferA[index] = item.replace("(","")
	if ")" in item:
		bufferA[index]= item.replace(")","")
for index,item in enumerate(inputA):
	if "(" in item:
		inputA[index] = item.replace("(","")
	if ")" in item:
		inputA[index]= item.replace(")","")

for index1, arrays in enumerate(operationsA):
	for index2,items in enumerate(arrays):
		if isinstance(items,list):
			for index3,item in enumerate(items):
				if "(" in item:
					operationsA[index1][index2][index3] = item.replace("(","")
				if ")" in item:
					operationsA[index1][index2][index3] = item.replace(")","")
		else:
			if "(" in items:
				arrays[index2] = items.replace("(","")
			if ")" in items:
				arrays[index2] = items.replace(")","")
for items in inputA:
	if items in bufferA:
		inputA.pop(inputA.index(items))
Answer = input("Do You want to specify inputs? (yes/no):")
if Answer == "yes" or Answer =="yes" or Answer == "Y" or Answer == "y":
	DictValues = {}
	for items in inputA:
		DictValues[items] = int(input(f"Enter value for {items}:"))
		if DictValues[items] > 1:
			raise Exception("Values must be 1 or 0")
		else:
			continue
for arrays in operationsA:
	writeNode(arrays[0],"square")
	if arrays[2] not in bufferA:
		writeNode(arrays[2],"triangle")
	for items in arrays[1]:
		if items not in bufferA:
			writeNode(items,"invtriangle")
for arrays in operationsA:
	for items in arrays[1]:
		if items in bufferA:
			for itemx in operationsA:
				if itemx[2] == items:
					writeEdgeNode(itemx[0],arrays[0],items)
		else:
			writeEdgeNode(items,arrays[0])
	if arrays[2] not in bufferA:
		writeEdgeNode(arrays[0],arrays[2])
fDot.write("}")
