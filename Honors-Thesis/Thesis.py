"""
This is the property of Peace Idahor
"""
import sys
#-------------------------Importing Helper Functions --------------------------------------------------------------------------------------------------------------------
from thesisfunctions import verilogFuncs
from thesisfunctions import prepareDot
import os
import re 
import argparse

parser = argparse.ArgumentParser(description='Process some inputs.')
parser.add_argument('-mode', choices=['b', 'm'], help='Choose mode: B for Boolean, m for module', required=True)
parser.add_argument('-debug', choices=['y', 'n'], default='n', help='Choose debug mode: y for yes, n for no', required=False)
parser.add_argument('-spi', '--specify_inputs', type=str, default='n', choices=['y', 'n'], help='specify inputs (y/n)')
parser.add_argument('-f', '--file_path', type=str, required=True, help='specify the path to the Verilog file')

# create an argument group for the lib argument
lib_group = parser.add_argument_group(title='library file options', description='required only if mode is m')
lib_group.add_argument('-lib', metavar='lib', type=str, required=False, help='Specify the library file path')
lib_group.add_argument('-abs', '-a', choices=['h', 'l'], default='l', help='h for high, l for low. Required if mode is m')
# set the required attribute of the argument group based on the mode flag
if parser.parse_args().mode == 'm':
	lib_group.required = True
else:
	lib_group.required = False


args = parser.parse_args()
operationsA = []
"""
This returnOut function does most of the translating of the verilog. It is a recursive function that receives as 
inputs,
Array:  An array containing the operation performed in the assign statement
indexMaster: A number used to differenciate between different operations of the same type
outputE: the result of the strip function showing what the output of the returnOut function should look like
outputN: the variable the output of the assign statement is assigned to

A Good thing to do is print out, OperationsA, It shows you the operations being performed in the verilog script
"""
def returnOut(Array,indexMaster,outputE,outputN=""):
	if len(Array) == 1: # if Array contains only 1 item
		for indexItem,items in enumerate(operationsA): # iterate over operationsA
			if items[2] == Array[0]: # if the third item in the nested list items of operationsA is equal to Array[0]
				operationsA[indexItem][2] = outputN # update the third item of items in operationsA with outputN
				outputA.append(outputN) # add outputN to the end of outputA list
				outputA.remove(Array[0]) # remove the first item in Array from outputA list

	if "(" in Array: # if '(' is present in Array
		openind = [] # initialize an empty list for storing the opening brackets' index
		closeind = [] # initialize an empty list for storing the closing brackets' index
		for index,item in enumerate(Array): # iterate over Array
			if item =="(": # if the item is opening bracket
				openind.append(index) # add the index of the opening bracket to openind list
			if item ==")": # if the item is closing bracket
				closeind.append(index) # add the index of the closing bracket to closeind list
		i = len(openind) # initialize i with the length of openind
		while((i - len(openind))<=i): # while the difference between i and len(openind) is less than or equal to i
			indexMaster +=1 # increment the indexMaster by 1
			if "(" in Array: # if '(' is present in Array
				sig = 0 # initialize sig with 0
				sig1=0
				for i in range(len(openind)-1):
					if i+1 !=None:
						if openind[i]+1 == openind[i+1]:
							sig1=1
				if sig1==1:
					lp = openind[len(openind)-1]
					rp = closeind[0]
					rightSide = Array[lp+1:rp]
				else:
					lp = openind[len(openind)-1] # get the last index of openind list
					rp = closeind[len(closeind)-1] # get the first index of closeind list
					rightSide = Array[lp+1:rp] # get the items between lp+1 and rp from Array and assign it to rightSide
			else: # if '(' is not present in Array
				sig = 1 # initialize sig with 1
				rightSide = Array # assign Array to rightSide'

			operationin,Array2,out = returnOut(rightSide,indexMaster,outputE,outputN) # call returnOut function with arguments rightSide, indexMaster, outputE, outputN and store the returned values in operationin, Array2, and out respectively
			bufferA.append(out) # add out to bufferA list
			if sig == 0: # if sig is 0
				while rp >= lp: # while rp is greater than or equal to lp
					Array.pop(rp) # remove the item at index rp from Array
					rp -=1 # decrement the rp by 1
				Array.insert(lp,out) # insert out at index lp in Array
			openind = [] # initialize an empty list for storing the opening brackets' index
			closeind = [] # initialize an empty list for storing the closing brackets' index
			for index,item in enumerate(Array): # iterate over Array
				if item =="(": # if the item is opening bracket
					openind.append(index) # add the index of the opening bracket to openind list
				if item ==")": # if the item is closing bracket
					closeind.append(index) # add the index of the closing bracket to closeind list
			if len(openind)==0 and len(Array) !=1 : # if there are no opening brackets and the length of Array is not 1
				for item in Array: # iterate over Array
					if item == "&" or item == "|" or item =="^": # if item is either
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
					if item== "~" and len(Array)==2:
						operationin,Array2,out = returnOut(Array,indexMaster,outputE,outputN)
			if out == outputE:
				try:
					bufferA.remove(out)
				except ValueError:
					bufferA.remove(out+ "n")
				return out
			
	else:
		if "&" in Array and "~" not in Array:
			operationin = "And" + f"/{indexMaster}" # Add the index to the operation to create a specific ID for the operation
			out= f"{Array[0]}" + "&" + f"{Array[2]}" #the output of this and boolean function
			inputA.append(Array[0]) #appending the inputs to the boolean operation to my inputs Array
			if Array[0] in outputA: # is the input to the boolan operation is also an output to another boolean operation, then I add it to my buffer array, meaning it is an edge between two operation blocks
				bufferA.append(Array[0])
			inputA.append(Array[2])
			if Array[2] in outputA:
				bufferA.append(Array[2])
			Array.pop(Array.index("&"))
			bufferA.append(out)
			if out == outputE: #checking to see if the output of the boolean operation, is the output sent into the function, If it is, I add it to my output array
				outputA.append(outputN)
				operationsA.append([operationin,Array,outputN])
			else:
				operationsA.append([operationin,Array,out])
			return operationin,Array,out
		"""
		Basically the same idea is replicated for different boolean operations
		"""
		if "|" in Array and "~" not in Array:
			operationin = "or" + f"/{indexMaster}"
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
			operationin = "xor" + f"/{indexMaster}"
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
			if len(Array) > 2 and ("&" not in Array and "|" not in Array and "^" not in Array):
				op = 2
				left_side = Array[op- 1]
				right_side = Array[op + 1]
				Array = [Array[0], left_side+Array[op]+right_side]
			operationin = "not" + f"/{indexMaster}" # Check if the tilde character is present in the input array
			indexMaster += 1 # Create a string variable to represent the logical "not" operation being performed	
			indexV = Array[Array.index("~")+1] 	# Increment indexMaster to keep track of the number of operations performed
			Arrayin = [indexV] 		# Extract the index of the variable being negated
			out= "~" + f"{indexV}"# Create a new list containing only the variable being negated, and create a new string variable to represent the output
			if out in bufferA and out not in notTrack:
				if out+"n" in bufferA:
					# Check if the output of the not operation is in the buffer array
					operationin = notTrack[out]
					# If it is, this means the operation has been visited before, so retrieve the previous index from the notTrack dictionary
				else:
					bufferA.append(out + "n")
					# If it hasn't been visited before, add it to the buffer array
					notTrack[out +"n"] = operationin
					# Add it to the notTrack dictionary	
			else:
				if out in bufferA:
					# Check if the output of the not operation is in the buffer array
					operationin = notTrack[out]
					# If it is, this means the operation has been visited before, so retrieve the previous index from the notTrack dictionary
				else:
					bufferA.append(out)
					# If it hasn't been visited before, add it to the buffer array
					notTrack[out] = operationin
					# Add it to the notTrack dictionary	
			notDict.append([out,indexMaster])
			# Append the output and its index to the notDict list
			inputA.append(indexV)
			# Append the index of the variable being negated to the inputA list
			if indexV in outputA:
				bufferA.append(indexV)
				# If the negated variable is already in the outputA list, append it to the bufferA list
			Array.pop(Array.index("~"))
			# Remove the tilde character from the input array
			operationsA.append([operationin,Arrayin,out])
			# Append the operation, input, and output to the operationsA list
			
			if len(Array) >1:
				indexf = Array.index(indexV)
				Array.pop(indexf)
				Array.insert(indexf,out)
				# If there are still elements in the input array, replace the negated variable with the output variable
				out = returnOut(Array,indexMaster,outputE,outputN)
				return out
			if out == outputE:
				outputA.append(outputN)
				# If the output variable is the same as the expected output, append the negated variable to the outputA list
				operationsA.append([operationin,Array,outputN])
			else:
				operationsA.append([operationin,Array,out])
				# Otherwise, append the operation, input, and output to the operationsA list
			return operationin,Array,out

		if "~&"	 in Array:
			operationin = "Nand" + f"/{indexMaster}"
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
			operationin = "Nor" + f"/{indexMaster}"
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
			operationin = "Xnor" + f"/{indexMaster}"
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
This function gives an initial view of the resulting output of each assign statement in it's simplest form
So given an assign statement such as
assign c = b & f;
the strip function returns b&f
if given c = (b & f) &g;
it returns b&f&g

"""
def strip(array):
	while "(" in array:
		array.remove("(")
	while ")" in array:
		array.remove(")")
	return ''.join(array)

"""
This is when the input file is a gate level verilog script but I want to flatten it out and get a boolean representation. 
For each array it translate the array into the boolean representation and calls the return out function.
I reccomend printing out the clauses array for more clarity. 
"""
exprarr = []
import re
def parse_expression(expr):
    result = []
    current_str = ''
    for char in expr:
        if char in ['(', ')', '&', '|', '~']:
            if current_str:
                result.append(current_str)
                current_str = ''
            result.append(char)
        else:
            current_str += char
    if current_str:
        result.append(current_str)
    return result

def returnOutB(array):
	operations = ["&","|","^"]
	operation = array[0].split('/')[0]
	operationIndex = array[0].split('/')[1]
	for key in libDict:
		if key == operation:
			expr = libDict[key]
			expr = expr.replace('*', '&').replace('+', '|').replace('!', '~')
			expr = expr[2:]
			for i in range(len(expr)-1):
				if expr[i] == "|" or expr[i] =="&" or expr[i] == "^" :
					if (expr[i-2] !="(" or expr[i+2] != ")") and 2+i != len(expr)-1:
						exprlist = re.findall(r'\(|\)|[~&\|]|[\w_]+|~\w+', expr)
						for j in range(len(exprlist)-1):
							if exprlist[j] == "~":
								exprlist[j] = "~" + exprlist[j+1]
								exprlist = exprlist[:j+1] + exprlist[j+2:]
								if "~" not in exprlist:
									break
						exprlist2 = []
						count = sum(any(op in s for op in operations) for s in exprlist)
						for i in range(len(exprlist)-1):
							if exprlist[i] in operations :
								if i-2 >= 0 and i+2 <len(exprlist) and exprlist[i-2] in operations and exprlist[i+2] in operations:
									exprlist2.append(exprlist[i])
									continue
								elif exprlist[i-2] in operations and (i+2 < len(exprlist)) and exprlist[i+2] not in operations and count%2 ==0:
									exprlist2.insert(0,exprlist[0])
									exprlist2.append(exprlist[i])
									exprlist2.append(exprlist[i+1])
									exprlist2.append(")")
								else:
									exprlist2.append("(")
									exprlist2.append(exprlist[i-1])
									exprlist2.append(exprlist[i])
									exprlist2.append(exprlist[i+1])
									exprlist2.append(")")
						expr = ''.join(exprlist2)
						break

			for item in array[1]:
				for key in varDict:
					if key.split("/")[1] == operationIndex:
						if varDict[key] == item:
							key_prefix = key.split("/")[0][1:]
							item = item.replace('\\', r'\\') # escape the item string
							expr = re.sub(r'\b{}\b'.format(key_prefix), item, expr)
	outputE = strip(list(expr))
	outputN = array[2]
	exprinput = parse_expression(expr)
	print(expr)
	returnOut(exprinput,int(operationIndex),outputE,outputN)
	return

#---------------------------------------------------------Given a gate level verilog script-----------------------------------------------------------------------------------------------------------
if args.mode == 'm':
	lib = args.lib
	f = args.file_path
	inputs = []
	regs = []
	outputs = []
	wires = []


	wordArrsave = verilogFuncs.parser(f)
	wordArrsave2 = verilogFuncs.parser2(lib)
	dotFile = open("Translate.dot","a")
	dotfile = prepareDot(dotFile)
	dotfile.openDot()#opening a dot file
	numberOfClauses = 0
	numberOfVariables = 0
	libDict = {}
	varDict = {}
	clauses = []
	inputA = []
	outputA = []
	bufferA = []
	varsA = []
	notDict = []
	notTrack = {}
	inputPrimary = []
	"""
	This is pretty intuitive, but I am going through the wordArrsave2 and looking for key words indicating presence of 
	important information.
		"""
	for index,word in enumerate(wordArrsave2):
		if word == "GATE":
			libDict[wordArrsave2[index+1]] = wordArrsave2[index+3] # creates a dictionary where the key is the gate and the value is its corresponding Verilog HDL code

	for index, word in enumerate(wordArrsave):
		if word == "//": # checking to see if part of the code was commented 
			while wordArrsave[index] != ";":
				wordArrsave.pop(index) # removes the commented section from the wordArrsave
		if word == "input" or word == "output" or word == "wire" or word == "reg":
			index2 = index + 1
			while wordArrsave[index2] != ";":
				varsA.append(wordArrsave[index2]) # collects the names of the variables in varsA
				index2 += 1
		if word == "input":
			indexInput = index +1
			while wordArrsave[indexInput] != ";":
				inputPrimary.append(wordArrsave[indexInput]) # collects the names of the input variables in inputPrimary
				indexInput +=1
		for key in libDict:
			if key == word:
				line = []
				index2 = index
				while wordArrsave[index2] != ";":
					if '.' in wordArrsave[index2]:
						varDict[wordArrsave[index2] + f'/{index}'] = wordArrsave[index2+1] # creates a dictionary where the key is the variable name and the value is the corresponding bitwidth
					else:
						line.append(wordArrsave[index2]) # collects the elements of the current line in line
					index2 +=1
				for item in line[2:-1]:
					inputA.append(item) # collects the inputs of the gate in inputA
				outputA.append(line[len(line)-1]) # collects the output of the gate in outputA
				name = line[0]+f'/{index}'
				clauses.append([name,line[2:-1],line[len(line)-1]]) # collects the clause in clauses, which is the name of the gate, its inputs, and its output
	if args.abs == "h": # if yes, set Abst flag to 1 and print message
		Abst = 1
	elif args.abs == "l": # if no, set Abst flag to 0 and print message
		Abst=0

	if Abst == 1: # if Abst flag is set to 1, run the following code
		for array in clauses: # iterate through each clause in the clauses list
			for item in array[1]: # iterate through each input variable in the clause
				if item in outputA: # if the input variable is also an output variable, add it to the bufferA list
					bufferA.append(item)
		dotfile.setup(inputA,bufferA,outputA) # set up the dotfile using inputA, bufferA and outputA lists
		verilogFuncs.processVisual(bufferA,clauses,inputA) # process the visual using bufferA, clauses, and inputA lists

		if args.debug == "y": # if yes, set labelon flag to 1 and print message
			labelon = 1
		elif args.debug == "n": # if no, set labelon flag to 0 and print message
			labelon=0
		# Creating an empty dictionary to store the specified input values
		inputSpecifiedArray = {}

		# Prompting the user to specify inputs
		# Checking if the user wants to specify inputs
		if args.specify_inputs == "y":
			inputon = 1
			
			# Prompting the user to specify a value for each input variable
			for item in inputPrimary:
				inputSpecified = input(f"{item}: ")
				
				# Checking if the input value is valid (0 or 1)
				if inputSpecified =="0" or inputSpecified == "1":
					inputSpecifiedArray[item] = inputSpecified
				else:
					raise Exception("Input must be 0 or 1")

		# Checking if the user does not want to specify inputs
		elif args.specify_inputs == "n":
			inputon = 0

		# Checking if the user has specified inputs
		if inputon == 1:
			for array in clauses:
				returnOutB(array)
			verilogFuncs.simulation(operationsA,inputSpecifiedArray)
			
			# Updating the clauses list with the specified input values
			for index, array1 in enumerate(clauses):
				for array2 in operationsA:
					if array1[2] == array2[2]:
						clauses[index].append([])
						clauses[index].append([])
						clauses[index][4] = array2[4]
			for index, array in enumerate(clauses):
				for item in array[1]:
					clauses[index][3].append(0)
			for index1, array1 in enumerate(clauses):
				for index2, array2 in enumerate(operationsA):
					for item in array1[1]:
						if item in array2[1]:
							clauses[index1][3][array1[1].index(item)] = array2[3][array2[1].index(item)]

		# Writing visuals to the dotfile and closing it
		verilogFuncs.writeVisuals(dotFile,clauses,bufferA,labelon,inputon)
		dotfile.endFile()
	else:
		# Iterate over clauses and return the outputs of the clauses in the bufferA list
		for array in clauses:
			returnOutB(array)
		for array in operationsA:
			for array2 in operationsA:
				if array[0] == array2[0] and array[1]==array2[1] and array[2] !=array2[2]:
					if array[2] not in outputA:
						operationsA.remove(array)
		# Setup the dotfile with inputA, bufferA, and outputA lists
		dotfile.setup(inputA, bufferA, outputA)

		# Process the visuals by passing bufferA, operationsA, and inputA to verilogFuncs.processVisual function
		verilogFuncs.processVisual(bufferA, operationsA, inputA)

		if args.debug == "y": # if yes, set labelon flag to 1 and print message
			labelon = 1
		elif args.debug == "n": # if no, set labelon flag to 0 and print message
			labelon=0
		# Initialize an empty dictionary called inputSpecifiedArray
		inputSpecifiedArray = {}

		# Prompt the user to specify inputs and update the inputSpecifiedArray dictionary accordingly
		if args.specify_inputs == "y":
			inputon = 1
			for item in inputPrimary:
				inputSpecified = input(f"{item}: ")
				if inputSpecified == "0" or inputSpecified == "1":
					inputSpecifiedArray[item] = inputSpecified
				else:
					raise Exception("Input must be 0 or 1")
		elif args.specify_inputs == "n":
			inputon = 0

		# If inputon is 1, simulate the operationsA with the specified input values
		if inputon == 1:
			verilogFuncs.simulation(operationsA, inputSpecifiedArray)

		# Write the visuals using dotFile, operationsA, bufferA, labelon, and inputon
		verilogFuncs.writeVisuals(dotFile, operationsA, bufferA, labelon, inputon)

		# Close the dotfile
		dotfile.endFile()
#---------------------------------------------------------------------------------------------------Given a boolean level verilog script----------------------------------------------------------------------------------------------------
elif args.mode == 'b':
	
	f = args.file_path
	wordArrsave = verilogFuncs.parser3(f) #extracting important information from my verilog file
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
	This for loop is used to search for assign statements and then call the returnOut function with the previously 
	specified perameters.
	It also ignores any commented lined in the verilog script.
	You can comment lines of verilog, but you cannot add commented lines that are not verilog
	"""
	for index,word in enumerate(wordArrsave):
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

	if args.debug == "y": # if yes, set labelon flag to 1 and print message
		labelon = 1
	elif args.debug == "n": # if no, set labelon flag to 0 and print message
		labelon=0
	#getting actual inputs from the user in terms of 0 or 1
	inputSpecifiedArray = {}
	if args.specify_inputs == "y":
		inputon = 1
		for item in inputPrimary:
			inputSpecified = input(f"{item}: ")
			if inputSpecified =="0" or inputSpecified == "1":
				inputSpecifiedArray[item] = inputSpecified
			else:
				raise Exception("Input must be 0 or 1")
	elif args.specify_inputs == "n":
		inputon = 0
	dotfile.setup(inputA,bufferA,outputA)
	#calling the visual representation functions that write to the dot file
	verilogFuncs.processVisual(bufferA,operationsA,inputA)
	if inputon ==1:
		verilogFuncs.simulation(operationsA,inputSpecifiedArray)
	operationsDict = {}
	verilogFuncs.writeVisuals(dotFile,operationsA,bufferA,labelon,inputon)
	dotfile.endFile() #closing the dotfile
else:
	raise Exception("Sorry Boolean or Gate level verilog only")
