from operator import indexOf
from tkinter import SOLID
from tkinter.ttk import Style
import pydot
import sys


graph = pydot.Dot("my_graph", graph_type="graph", bgcolor="white", splines='ortho', rankdir='TD')

#-----------------------creating subgraphs to contain my inputs and my outputs so that they have the same rank--------------------------------
out = pydot.Cluster('Output',label='Output', rank="same", style="invis")
graph.add_subgraph(out)
inputs = pydot.Cluster('Input',label='Input', rank="same", style="invis")
graph.add_subgraph(inputs)
#---------------------- Initializing the gates and the input and output blocks ---------------------------------------------
def input(item):
	input = pydot.Node(f"{item}",label=f"{item}",shape="invtriangle", fontsize= 10)
	inputs.add_node(input)
def output(item):
	output = pydot.Node(f"{item}",label=f"{item}",shape="invtriangle", fontsize= 10, rank="same")
	out.add_node(output)
def andGate(num):
	andGate = pydot.Node(f"andGate{num}",label="and",shape="square")
	graph.add_node(andGate)
def orGate(num):
	orGate = pydot.Node(f"orGate{num}",label="or",shape="square")
	graph.add_node(orGate)
def xorGate(num):
	xorGate = pydot.Node(f"xorGate{num}",label="xor",shape="square")
	graph.add_node(xorGate)
def nandGate(num):
	nandGate = pydot.Node(f"nandGate{num}",label="nand",shape="square")
	graph.add_node(nandGate)
def notGate(num):
	notGate = pydot.Node(f"notGate{num}",label="not",shape="square")
	graph.add_node(notGate)
def norGate(num):
	norGate = pydot.Node(f"norGate{num}",label="nor",shape="square")
	graph.add_node(norGate)
def xnorGate(num):
	xnorGate = pydot.Node(f"xnorGate{num}",label="xnor",shape="square")
	graph.add_node(xnorGate)
def buffer(num):
	buffer = pydot.Node(f"buffer{num}",label = f"{num}" ,shape="line",color = "white")
	graph.add_node(buffer)
#------------------------------Iterating thought the verilog file passed in as input to the script ------------------------------------------------
f = open(sys.argv[1],"r")
wordArr = [] #an array of characters that appear in sequence
wordArrsave = []
count = 0


for line in f:
	for word in line:
		if word == ' ' or word == '(' or word == ')' or word == '\n' or word == '	' or word==',' : #creating a line of demarkation to seperate characters in sequence
			command = ''.join(wordArr) #joining those characters into a str word that represents some kind of command
			#print(command)
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

# initializing and appending my input and output arrays to be used later -------------------------------------------
inputArr = [] #getting the inputs to the verilog module
outputArr = [] #getting the outputs to the verilog module
bufferArr = [] #getting intermediate saved variables
for index,command in enumerate(wordArrsave):
	if command == "input":
		index1 = index+1
		while(wordArrsave[index1] != 'output'):
			inputArr.append(wordArrsave[index1])
			index1 +=1
		#print(inputArr)
	if command == "output":
		index1 = index+1
		while(wordArrsave[index1] != ';'):
			outputArr.append(wordArrsave[index1])
			index1 +=1
		#print(outputArr)
	
count2 = 1 #creating unique input blocks that allow for multiple input blocks
count3 = 1
#---------------------Checking the command array for certian commands and drawing the dot representation of the file ---------------------------
for index,command in enumerate(wordArrsave):
	if command == "assign": # checking to see if I get the assign command, which would indicate the presence of a equation
		subArr = [] # creating a subarray to contain the elements that appear in that equation
		index1 = index
#--------------------------------Populating the subarray ---------------------------------------------------------------------------------------
		while wordArrsave[index1] != ';':
			subArr.append(wordArrsave[index1])
			index1 +=1
#------------------------------------in this section i check to see if I get a certain command and try to build the corresponing node and edges to fufill the equation ---------------------------------------------------
		if '|' in subArr:
			orGate(count2)
			if subArr[1] in outputArr:
				output(subArr[1])
				graph.add_edge(pydot.Edge(f"orGate{count2}",f"{subArr[1]}", color="black", style=SOLID))
			else:
				bufferArr.append(subArr[1])
				buffer(subArr[1])
				graph.add_edge(pydot.Edge(f"orGate{count2}",f"buffer{subArr[1]}", color="black", style=SOLID))
			for item in subArr:
				if item in inputArr and item not in bufferArr:
					count3 +=1
					input(item)
					graph.add_edge(pydot.Edge(f"{item}",f"orGate{count2}", color="black", style=SOLID))
				if item in inputArr and item in bufferArr and item !=subArr[1]:
					count3 +=1
					graph.add_edge(pydot.Edge(f"buffer{item}",f"orGate{count2}", color="black", style=SOLID))
			count2 +=1
		elif '&' in subArr:
			andGate(count2)
			if subArr[1] in outputArr:
				output(subArr[1])
				graph.add_edge(pydot.Edge(f"andGate{count2}",f"{subArr[1]}", color="black", style=SOLID))
			else:
				bufferArr.append(subArr[1])
				buffer(subArr[1])
				graph.add_edge(pydot.Edge(f"andGate{count2}",f"buffer{subArr[1]}", color="black", style=SOLID))
			for item in subArr:
				if item in inputArr and item not in bufferArr:
					count3 +=1
					input(item)
					graph.add_edge(pydot.Edge(f"{item}",f"andGate{count2}", color="black", style=SOLID))
				if item in inputArr and item in bufferArr and item !=subArr[1]:
					count3 +=1
					graph.add_edge(pydot.Edge(f"buffer{item}",f"andGate{count2}", color="black", style=SOLID))
			count2 +=1
		elif '^' in subArr:
			xorGate(count2)
			if subArr[1] in outputArr:
				output(subArr[1])
				graph.add_edge(pydot.Edge(f"xorGate{count2}",f"{subArr[1]}", color="black", style=SOLID))
			else:
				bufferArr.append(subArr[1])
				buffer(subArr[1])
				graph.add_edge(pydot.Edge(f"xorGate{count2}",f"buffer{subArr[1]}", color="black", style=SOLID))
			for item in subArr:
				if item in inputArr and item not in bufferArr:
					count3 +=1
					input(item)
					graph.add_edge(pydot.Edge(f"{item}",f"xorGate{count2}", color="black", style=SOLID))
				if item in inputArr and item in bufferArr and item !=subArr[1]:
					count3 +=1
					graph.add_edge(pydot.Edge(f"buffer{item}",f"xorGate{count2}", color="black", style=SOLID))
			count2 +=1
		elif '~' in subArr:
			notGate(count2)
			if subArr[1] in outputArr:
				output(subArr[1])
				graph.add_edge(pydot.Edge(f"notGate{count2}",f"{subArr[1]}", color="black", style=SOLID))
			else:
				bufferArr.append(subArr[1])
				buffer(subArr[1])
				graph.add_edge(pydot.Edge(f"notGate{count2}",f"buffer{subArr[1]}", color="black", style=SOLID))
			for item in subArr:
				if item in inputArr and item not in bufferArr:
					count3 +=1
					input(item)
					graph.add_edge(pydot.Edge(f"{item}",f"notGate{count2}", color="black", style=SOLID))
				if item in inputArr and item in bufferArr and item !=subArr[1]:
					count3 +=1
					graph.add_edge(pydot.Edge(f"buffer{item}",f"notGate{count2}", color="black", style=SOLID))
			count2 +=1
		elif '~|' in subArr:
			norGate(count2)
			if subArr[1] in outputArr:
				output(subArr[1])
				graph.add_edge(pydot.Edge(f"norGate{count2}",f"{subArr[1]}", color="black", style=SOLID))
			else:
				bufferArr.append(subArr[1])
				buffer(subArr[1])
				graph.add_edge(pydot.Edge(f"norGate{count2}",f"buffer{subArr[1]}", color="black", style=SOLID))
			for item in subArr:
				if item in inputArr and item not in bufferArr:
					count3 +=1
					input(item)
					graph.add_edge(pydot.Edge(f"{item}",f"norGate{count2}", color="black", style=SOLID))
				if item in inputArr and item in bufferArr and item !=subArr[1]:
					count3 +=1
					graph.add_edge(pydot.Edge(f"buffer{item}",f"norGate{count2}", color="black", style=SOLID))
			count2 +=1
		elif '~^' in subArr or '^~' in subArr:
			xnorGate(count2)
			if subArr[1] in outputArr:
				output(subArr[1])
				graph.add_edge(pydot.Edge(f"xnorGate{count2}",f"{subArr[1]}", color="black", style=SOLID))
			else:
				bufferArr.append(subArr[1])
				buffer(subArr[1])
				graph.add_edge(pydot.Edge(f"xnorGate{count2}",f"buffer{subArr[1]}", color="black", style=SOLID))
			for item in subArr:
				if item in inputArr and item not in bufferArr:
					count3 +=1
					input(item)
					graph.add_edge(pydot.Edge(f"{item}",f"xnorGate{count2}", color="black", style=SOLID))
				if item in inputArr and item in bufferArr and item !=subArr[1]:
					count3 +=1
					graph.add_edge(pydot.Edge(f"buffer{item}",f"xnorGate{count2}", color="black", style=SOLID))
			count2 +=1
		else:
			input(item)
			if subArr[1] in outputArr:
				output(count2)
				graph.add_edge(pydot.Edge(f"{item}",f"output{count2}", color="black",label=subArr[1], style=SOLID))
		
	if command == "wire":
		print(wordArrsave[index+1])
		inputArr.append(wordArrsave[index+1])


graph.write_png("output.png")
