import pythonds as ds
import csv
import sys
from collections import deque

from pythonds.graphs import PriorityQueue
from pythonds.basic import Queue


class OSN:
    def __init__(self):
        self.network = Graph()
        self.MST = Graph()
        self.negative_network = Graph()
    def buildGraph(self,filename):# my method to read my excel file
        with open(filename, "r") as excel:# put it in read mode
            read = csv.reader(excel, delimiter=",") # i imported csv at the top of the file to be able to read the ecel file
            for row in read:
                firstname,Secondname,closeness = row# diconstruct the row into 3 sections, representing firts and second name
                start = firstname
                end = Secondname
                self.network.addEdge(start,end,int(closeness))# add a weighted edge going from the start to the end
                self.network.addEdge(end,start,int(closeness))# add a weighted edge going fromm end to start
#--------------------This code will be used later for my buildMST method-------------------
                self.negative_network.addEdge(start,end,-1*int(closeness))# creating an edge from start to end with negative weight
                self.negative_network.addEdge(end, start, -1*int(closeness))# creating an edge from end to start with negative weight
                # the key of the dictionary is the starting location
            firstRow = 1
    def reset(self):# this reset method is ment to reset my BFS
        for v in self.network:# for each vertice in the graph, set the color to white, and the pred to none
            v.pathweight = 0
            v.dist  = sys.maxsize
            v.pred = None
            v.color = "white"
# -------------this is my findDistance method used to find the distance between two vertices/ users in the graph
    def findDistance(self,user1, user2):# takes two perameters
        self.reset()# Call my reset function to make sure the graph is at default
        self.bfs(self.network,self.network.getVertex(user1))#calling my BFS method with self.network
        v = self.network.getVertex(user2)# geting the vertex at user 2
        friends = 0# initializing friends ti 0
        while v != None:
            vpred = v.getPred()#this is used to initialize vpred to the previous vertice, I actually want to  start from user2, and go to user 1
            if v.getId()==user1:# if i find user 1, end my program,i have found the distance
                break
            if vpred !=None:
                friends +=1# increment friends meaning adding 1 to the distance
            v = vpred
        return friends # return friends with would be the distance
# ------------------- This is the bfs code i got from class, i just made it a method so it's easy to use in this context
    def bfs(self,g, start):
        start.setDistance(0)
        start.setPred(None)
        vertQueue = ds.Queue()
        vertQueue.enqueue(start)
        while (vertQueue.size() > 0):
            currentVert = vertQueue.dequeue()
            for nbr in currentVert.getConnections():
                if (nbr.getColor() == 'white'):
                    nbr.setColor('gray')
                    nbr.setDistance(currentVert.getDistance() + 1)
                    nbr.setPred(currentVert)
                    vertQueue.enqueue(nbr)
            currentVert.setColor('black')
#----------- this is the prime function i got from class, i also made this a method so that it's easy to use
    def prim(self,G, start):
        pq = PriorityQueue()
        for v in G:
            v.setDistance(sys.maxsize)
            v.setPred(None)
        start.setDistance(0)
        pq.buildHeap([(v.getDistance(), v) for v in G])
        while not pq.isEmpty():
            currentVert = pq.delMin()
            for nextVert in currentVert.getConnections():
                newCost = currentVert.getWeight(nextVert)
                if nextVert in pq and newCost < nextVert.getDistance():
                    nextVert.setPred(currentVert)
                    nextVert.setDistance(newCost)
                    pq.decreaseKey(nextVert, newCost)
# ----------- This is my buildMST method that creates a maximum spanning tree------------
    def buildMST(self):
        start = self.network.getVertex("Lynch")# get the vertex of the first user
        self.prim(self.negative_network,start)# call my prime method, with the negative_network i made early in the code
        for v in self.negative_network: # for each vertex in my negative weight graph
            for friend in v.getConnections():# for each friend in the connections
                if friend == v.getPred():
                    self.MST.addEdge(friend.id,v.id,-v.getWeight(friend))# add a weighted for my spanning tree from my friend to the vertex
                    self.MST.addEdge(v.id, friend.id,-v.getWeight(friend))# add a weighted edge from my vertex to the friend
# --------------------this is my findPath method-----------------
    def findPath(self,user1,user2):# it accepts two perameters user1 and user2
        v1 = self.MST.getVertex(user1)# get the vertex at user 1
        v2 = self.MST.getVertex(user2)# get the vertex at user 2
        self.bfs(self.MST,v1)# call my bfs method
        path = []# create an empty list that i would add to as i go along
        path.append(v2.id)# append the first friend i see
        while v2.getPred():
            path.append(v2.getPred().id)# append the next friend to the path
            v2 = v2.getPred()
        path.reverse()# reverse it to get the result in the right order
        for v in self.MST:# for the vertex in the graph
        # this is basically my reset method, but i wanted to hard code this for more clarity
            v.dist = sys.maxsize
            v.pred = None
            v.color = "white"
        return " -> ".join(path)# return my path
#------------create a new bfs method that is going to be used for my findclosepath method
    def bfs2(self,g,start):
        start.setDistance(0)
        start.setPred(None)
        vertQueue = Queue()
        vertQueue.enqueue(start)
        while (vertQueue.size() > 0):
            currentVert = vertQueue.dequeue()
            for nbr in currentVert.getConnections():
                if (nbr.getColor() == 'white'):
                    nbr.setColor('gray')
                    nbr.setDistance(currentVert.getDistance() + 1)
                    friends = nbr.getConnections()
#-------------this is where my changes start-----------------------------------------------
                    for v in friends:# for each vertex in friends
                        if v.getDistance()==nbr.getDistance()-1:#if the distance of v is closer to nbr or the next vertex
                            if v.pathweight + v.getWeight(nbr) > nbr.pathweight:# see if the pathweight of
                                nbr.pathweight = v.pathweight + v.getWeight(nbr)#update the pathweight of nbr to the combination of v.pathweight and it's weight
                                nbr.setPred(v)
                    vertQueue.enqueue(nbr)#add nbr to the queue
            currentVert.setColor('black')
#-----------creating my findclosePath method----------------------
    def findClosePath(self,user1,user2):
        self.reset()# makeing sure to reset the bfs2 method
        vertex1 = self.network.getVertex(user1)# get the vertex of both users
        vertex2 = self.network.getVertex(user2)
        self.bfs2(self.network,vertex1)# call the bfs2 method i created
        path = []# initialize the path to an empty list
        weight = vertex2.pathweight# initialize the weight to the pathweight of vertex 2
        while vertex2 !=None:
            path.append(vertex2.id)# append vertex 2 to my path
            if vertex2==vertex1:# if i reached the end of my journey, break
                break
            vertex2 = vertex2.getPred()# go one up in the tree and set vertex 2 to the new vertex
        path.reverse()
        return " -> ".join(path)+' ('+str(weight)+')'
class Vertex:
    def __init__(self, key):
        self.id = key
        self.connectedTo = {}
        self.color = 'white'
        self.dist = sys.maxsize
        self.pred = None
        self.disc = 0
        self.fin = 0
        self.pathweight = 0

    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def setColor(self, color):
        self.color = color

    def setDistance(self, d):
        self.dist = d

    def setPred(self, p):
        self.pred = p

    def setDiscovery(self, dtime):
        self.disc = dtime

    def setFinish(self, ftime):
        self.fin = ftime

    def getFinish(self):
        return self.fin

    def getDiscovery(self):
        return self.disc

    def getPred(self):
        return self.pred

    def getDistance(self):
        return self.dist

    def getColor(self):
        return self.color

    def getConnections(self):
        return self.connectedTo.keys()

    def getWeight(self, nbr):
        return self.connectedTo[nbr]

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getId(self):
        return self.id

class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self,f,t,cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())

if __name__ =="__main__":
    x = OSN()
    x.buildGraph('facebook_network (2).csv')
    print(x.findClosePath("Clark", "Schneider"))





