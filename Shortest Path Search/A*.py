import numpy as np
import networkx as nx
import heapq
import math 

inputs = np.loadtxt('data.txt', usecols=range(0,5))

def weight(a,b):
    (x1,y1) = a
    (x2,y2) = b
    
    return math.sqrt(pow(x2-x1,2)+pow(y2-y1,2))

def CreateGraph():
    G = nx.DiGraph()
    for i in range(0,len(inputs)):
        w = int(weight((inputs[i][1],inputs[i][2]),(inputs[i][3],inputs[i][4])))
        G.add_edge((inputs[i][1],inputs[i][2]),(inputs[i][3],inputs[i][4]),weight=w)

        if inputs[i][0]==2:
            G.add_edge((inputs[i][3],inputs[i][4]),(inputs[i][1],inputs[i][2]),weight=w)

    #print(list(G.neighbors((1042,7545))))
    #print(G.edges[(1042,7545), (990.0, 7549.0)]['weight'])
    return G

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(graph, start, goal):

    if start not in graph:
        raise Exception("this start location is not in map")

    if goal not in graph:
        raise Exception("this goal location is not in map")
    
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            path = []
            while came_from[current]:
                path.append(current)
                current = came_from[current]
            path.append(current)
            print("Path found!!")
            return path[::-1]
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.edges[current,next]['weight']
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current
    
    return 'No Path Found'

graph = CreateGraph()
print(a_star_search(graph,'abc',(487,8100)))
