class verilogFuncs:
    def  parser(f): #function to parse the verilog file to create a word array
        wordArr = [] #an array of characters that appear in sequence
        wordArrsave = []
        count = 0
        index = 0
        for line in f:
            for word in line:
                if word == ' ' or word == '\n' or word == '	' or word==',': #creating a line of demarkation to seperate characters in sequence
                    command = ''.join(wordArr) #joining those characters into a str word that represents some kind of command
                    check = 0
                    if '(' in command:
                        check = 1
                        if command in wordArrsave:
                            wordArrsave.remove(command)
                            index -=1
                        command = command.replace('(',"")
                        wordArrsave.append('(')
                        index+=1
                        wordArrsave.append(command)
                        index+=1
                    if '!' in command:
                        check = 1
                        if command in wordArrsave:
                            wordArrsave.remove(command)
                            index -=1
                        command = command.replace('!',"")
                        wordArrsave.append('!')
                        index+=1
                        wordArrsave.append(command)
                        index+=1
                    if '//' in command:
                        check =1
                        if command in wordArrsave:
                            wordArrsave.remove(command)
                            index -=1
                        command = command.replace('//',"")
                        wordArrsave.append('//')
                        index +=1
                        wordArrsave.append(command)
                        index +=1
                    if ')' in command:
                        check =1
                        if command in wordArrsave:
                            wordArrsave.remove(command)
                            index -=1
                        command = command.replace(')',"")
                        wordArrsave.append(command)
                        index +=1
                        wordArrsave.append(')')
                        index +=1
                    if ';' in command:
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
    def processVisual(bufferA,operationsA,inputA):
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
    def writeVisuals(fDot,operationsA,bufferA):
        dotfile = prepareDot(fDot)
        for arrays in operationsA:
            dotfile.writeNode(arrays[0],"square")
            if arrays[2] not in bufferA:
                dotfile.writeNode(arrays[2],"triangle")
            for items in arrays[1]:
                if items not in bufferA:
                    dotfile.writeNode(items,"invtriangle")
        for index,arrays in enumerate(operationsA):
            for items in arrays[1]:
                if items in bufferA:
                    for itemx in operationsA:
                        if itemx[2] == items:
                            dotfile.writeEdgeNode(itemx[0],arrays[0],items)
                else:
                    dotfile.writeEdgeNode(items,arrays[0])
            if arrays[2] not in bufferA:
                dotfile.writeEdgeNode(arrays[0],arrays[2])
class prepareDot:
    def __init__(self,fDot):
        self.fDot = fDot
    def openDot(self):
        self.fDot.truncate(0)
        self.fDot.write("digraph test{\n")
    def setup(self,inputA,bufferA,outputA): #function to prepare dot file
        #fDot.write('splines="ortho"\n')
        self.fDot.write('subgraph inputs{ rank="same"')
        for item in inputA:
            if item not in bufferA:
                if "(" in item:
                    item = item.replace("(","")
                if ")" in item:
                    item = item.replace(")","")
                self.fDot.write(f' "{item}" ')
        self.fDot.write('}\n')

        self.fDot.write('subgraph outputs{rank="same"')
        for item in outputA:
            if item not in bufferA:
                if "(" in item:
                    item = item.replace("(","")
                if ")" in item:
                    item = item.replace(")","")
                self.fDot.write(f' "{item}" ')
        self.fDot.write('}\n')
    def writeNode(self,inN,shape):
        self.fDot.write(f'"{inN}" [shape={shape}]\n')

    def writeEdgeNode(self,inN,outN="",label=""): 
        if label == "":
            self.fDot.write(f'"{inN}" -> "{outN}" \n')
        else:
            self.fDot.write(f'"{inN}" -> "{outN}" [label="{label}"]\n')
    def createSubgraph(self,input):
        self.fDot.write("subgraph{\nrand=same;")
        for item in input:
            self.fDot.write(f"{item};")
        self.fDot.write("\n}")
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
    def endFile(self):
        self.fDot.write("}")
