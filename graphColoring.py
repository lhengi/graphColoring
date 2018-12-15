from z3 import Solver, Bool, Bools, Or, And, Not, Implies, If, BoolVector
import numpy as np
import random
import time

def constructMyRandomGraph(numNodes, probToKeepNode):
    myGraph ={
        0: []
    }

    for i in range(0, numNodes):
        myGraph[i] = (list(range(0, numNodes)))
        myGraph[i].remove(i)

    for i in range(0, numNodes):
        for j in range(0, numNodes):
            probToDelete = random.randint(0, 101)
            if probToDelete > probToKeepNode:
                if j in myGraph[i]:
                    myGraph[i].remove(j)
                if i in myGraph[j]:
                    myGraph[j].remove(i)

    return myGraph

def constructMy2Dbool(graph, numColors):
    n = len(graph.items())
    m = []

    for i in range(0, n):
        m.append(BoolVector("m" + str(i), numColors))

    return m

def addDistinctRule(myBools, x, numColors, graph):
    n = len(graph.items())

    for i in range(0, n):  # each row
        for c in range(0, numColors):  # each color
            for c2 in range(c + 1, numColors):  # each color
                x.add(Or(Not(myBools[i][c]), Not(myBools[i][c2])))  # this cell cant be both these colors
    return x

def atLeastOneRule(myBools, x, graph):
    n = len(graph.items())

    for i in range(0, n):  # each row
        x.add(Or(myBools[i]))

    return x

def addAdjacentRule(myBools, x, numColors, graph):
    n = len(graph.items())

    for i in range(0, n):  # each row
        for j in range(0, len(graph[i])):
            for c in range(0, numColors):  # each color
                if i < graph[i][j]:
                    x.add(Or(Not(myBools[i][c]), Not(myBools[graph[i][j]][c])))  # this cell cant be both these colors
    return x

def heuristic(graph):
    saturatedNodes = [node for node in sorted(graph, key=lambda node: len(graph[node]), reverse=True)]
    colorDiction = {}
    for i in saturatedNodes:
        colorDiction[i] = -1
    colorArr = [0]
    for node in saturatedNodes:
        avlColors = colorArr.copy();
        for edg in graph[node]:
            try:
                if colorDiction[edg] != -1:
                    avlColors.remove(colorDiction[edg])
            except ValueError:
                pass
        if len(avlColors) <= 0:
            colorDiction[node] = len(colorArr)
            colorArr.append(len(colorArr))
        else:
            colorDiction[node] = avlColors[0]
    #for node in colorDiction:
        #print(node," ",colorDiction[node])

    return colorArr






def main():
    numNodes = 70
    probToKeepEdge = 60

    myGraph = constructMyRandomGraph(numNodes, probToKeepEdge)
    print(myGraph)
    print('heuristic started')
    start = time.time()
    print(len(heuristic(myGraph))," colors")
    end = time.time()
    print('end ---- heuristic'," Time: ",end-start)

    #for i in range(0, numNodes):
    #    print(i, ':', myGraph[i])

    for i in range(1, 1000):

        x = Solver()
        myBools = constructMy2Dbool(myGraph, i)
        x = addDistinctRule(myBools, x, i, myGraph)
        x = atLeastOneRule(myBools, x, myGraph)
        x = addAdjacentRule(myBools, x, i, myGraph)
        start = time.time()


        if x.check().r > 0:
            end = time.time()
            print('YES can be colored using', i, 'Colors',' time: ',(end-start))
            for j in range(0, len(myGraph.items())):  # each row
                    for c in range(0, i):
                        if(x.model().get_interp(myBools[j][c])):
                            print(j, c)

            break

        else:
            end = time.time()
            print('NO can\'t be colored using', i, 'Colors'," time: ",(end-start))

start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
