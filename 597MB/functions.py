class verilogFuncs:
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

class prepareCnf:
    def __init__(self,fcnf):
        self.fcnf = fcnf
    def openDot(self,numberOfVariables,numberOfClauses,regsDict,roll):
        self.numberOfVariables = numberOfVariables
        self.fcnf.truncate(0)
        self.fcnf.write(f"p cnf {(self.numberOfVariables-1)*roll} {numberOfClauses*roll}\n")
        self.fcnf.write("c The initial condition is 0 for all state bits\n")
        for key in regsDict:
            self.fcnf.write(f"{regsDict[key]} 0\n")
    def write(self,clauses,roll=1):
        #print(clauses)
        #print(targetState)
        numberOfactualVar = self.numberOfVariables -1
        i=0
        while i<=(roll-1):
            self.fcnf.write(f"c Rolling #{i+1}\n")
            for clause in clauses:
                if clause[0] == "And":
                    self.fcnf.write("c The AND gate ...\n")
                    self.fcnf.write(f"{clause[2]+ i*numberOfactualVar} -{clause[1]+ i*numberOfactualVar} 0\n") #(aV-x)
                    self.fcnf.write(f"{clause[3]+ i*numberOfactualVar} -{clause[1]+ i*numberOfactualVar} 0\n") #(bV-x)
                    self.fcnf.write(f"-{clause[2]+ i*numberOfactualVar} -{clause[3]+ i*numberOfactualVar} {clause[1]+ i*numberOfactualVar} 0\n") # (-aV-bVx)
                if clause[0] == "not":
                    self.fcnf.write("c The INV gate ...\n")
                    self.fcnf.write(f"-{clause[2]+ i*numberOfactualVar} -{clause[1]+ i*numberOfactualVar} 0\n") #(-aV-x)
                    self.fcnf.write(f"{clause[2]+ i*numberOfactualVar} {clause[1]+ i*numberOfactualVar} 0\n") #(aVx)
                if clause[0]=="N":
                        clause[1] = clause[1]+ i*numberOfactualVar
            i +=1
        self.fcnf.write("c The Target State...\n")
        for clause in clauses:
                if clause[0]=="N":
                    if clause[2] == 0:
                        self.fcnf.write(f"-{clause[1] } 0\n")
                    if clause[2] == 1:
                        self.fcnf.write(f"{clause[1]} 0\n")
    def writeTransition(self,sArray,NSArray,roll=1):
        numberOfactualVar = self.numberOfVariables -1
        i=1
        if roll > 1:
            self.fcnf.write("c Defining Transition relation\n")
            while i<=(roll):
                for KeyS in sArray:
                    for KeyN in NSArray:
                        if KeyN[len(KeyN)-1] == KeyS[len(KeyS)-1] and KeyN[0] == "N":
                            #print(f" {NSArray[KeyN] } {sArray[KeyS]+ i*numberOfactualVar}")
                            self.fcnf.write(f"-{NSArray[KeyN]} {sArray[KeyS]+ i*numberOfactualVar} 0\n")
                            self.fcnf.write(f"{NSArray[KeyN]} -{sArray[KeyS]+ i*numberOfactualVar} 0\n")
                            NSArray[KeyN] = numberOfactualVar + NSArray[KeyN]
                            break
                i+=1
        else:
            return

        
