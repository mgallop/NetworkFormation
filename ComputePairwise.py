#A Program To Solve Network Formation Games Computationally
#Max Gallop

import networkx as nx
from itertools import *
from math import log
from math import hypot
import matplotlib.pyplot as plt
import csv
import random
import copy
import numpy
import matplotlib.cm as cm


def frange(start, end=None, inc=None):
  if end == None:
    end = start + 0.0
    start = 0.0
  if inc == None:
    inc = 1.0
  L = []
  while 1:
    next = start + len(L) * inc
    if inc > 0 and next >= end:
      break
    elif inc < 0 and next <= end:
      break
    L.append(next)
  return L

def grapher(filename):
  G = nx.Graph()
  with open(filename,'rb') as f:
    m_reader = csv.DictReader(f)
    for row in m_reader:
      G.add_node(row["name"])
      G.node[row["name"]]['cap'] = float(row["cap"])
      G.node[row["name"]]['ideo'] = float(row["ideo"])
    return G

def graph_to_csv(filename, graph):
  with open(filename, "wb") as f:
    my_writer = csv.DictWriter(f, fieldnames = ("name", "cap", "ideo"))
    my_writer.writeheader()
    for i in graph.nodes():
      my_writer.writerow({"name":i, "cap":graph.node[i]['cap'], "ideo": graph.node[i]['ideo']})
      

      
def powerset(iterable):
  s = list(iterable)
  return list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))


###CHANGE THIS FUNCTION IF YOU WANT TO CHANGE THE UTILITY FUNCTION  
## Anna Utility Function 3
def utility(graph, delta = 1, c = 0):
  util = {}
  for i in graph.nodes():
    util[i] = 0
    for j in graph.nodes():
      if nx.has_path(graph, i, j):
        util[i] += (graph.node[j]["cap"]*(1-abs(graph.node[i]["ideo"]-graph.node[j]["ideo"]))*delta**(nx.shortest_path_length(graph,i,j)))
    util[i] = (util[i])**.5 - (c*len(graph.neighbors(i)))
  return util


def One_Add(graph, delta, c,  order = 3):
  if order == 3:
    h = graph.nodes()
  else:
    h = order
  for i in h:
    h = h[1:]
    for j in h:
      if j not in graph[i]:
        graphprime = copy.deepcopy(graph)
        graphprime.add_edge(i, j)
        if utility(graphprime,delta, c)[i] > utility(graph, delta, c)[i] and utility(graphprime, delta, c)[j] > utility(graph, delta, c)[j]:
          graph.add_edge(i,j)
            #print i, 'adds:      ', j
            
def One_Cut(graph, delta, c, order = 3): 
  if order == 3:
    h = graph.nodes()
  else:
    h = order
  for i in h:
    x = []
    for edges in graph.edges(i):
      x.append(edges[1])
    winner = copy.deepcopy(graph)
    possibilities = list(powerset(x))#                  # all possible subsets of (i)'s neighbors
    graphprime = copy.deepcopy(winner)
    y = graph.edges(i)
    graphprime.remove_edges_from(y)
    #print i, 'old neighbors:', graph[i]
    for j in possibilities:#                            # in each potential subgroup of i's neighbors
      for k in j:#                                      # for each member of that subgroup
        graphprime.add_edge(i, k)#                      # connect it to (i)
      if utility(graphprime, delta, c)[i] > utility(winner, delta, c)[i]:
        winner = copy.deepcopy(graphprime)
        #print i, 'winner' , j
      for k in j:
        graphprime.remove_edge(i, k)#
    graph.remove_edges_from(graph.edges())          
    graph.add_edges_from(winner.edges())
    #print i, 'new neighbors:', winner[i]               

	

    
def Find_Directed_Nash(graph): 
  if not nx.is_directed(graph):
    raise NameError("Not a directed graph, punk!")  
  h = graph.nodes()
  winner = copy.deepcopy(graph)
  for i in h:
    x = []
    for nodes in graph.nodes():
      if nodes != i:
        x.append(nodes)
    possibilities = list(powerset(x))#                  # all possible subsets of (i)'s neighbors
    graphprime = copy.deepcopy(graph)
    y = graph.edges(i)
    graphprime.remove_edges_from(y)
    #print i, 'old neighbors:', graph[i]
    for j in possibilities:#                            # in each potential subgroup of i's neighbors
      for k in j:#                                      # for each member of that subgroup
        graphprime.add_edge(i, k)#                      # connect it to (i)
      if utility(graphprime)[i] >= utility(graph)[i] and utility(graphprime)[i] >= utility(winner)[i]:    # if (i) prefers this, add these connections back to graph
        winner = copy.deepcopy(graphprime)
        #print i, 'winner' , j
      else:
        #print i, 'not winner' , j
        for k in j:
          graphprime.remove_edge(i, k)#
    graph.add_edges_from(winner.edges())
    #print i, 'new neighbors:', winner[i]               


def Find_Pairwise_Nash(graph, delta, c, orderb = 3):
  Done, Add, Cut = False, False, False
  while Done == False:
    if Add and Cut == True:
      Done = True
    while Add == False:
      edges = graph.edges()
      One_Add(graph, delta, c, orderb)
      if graph.edges() == edges:
        Add = True
      else:
        Cut = False
    while Cut == False:
      Add = False
      edges = graph.edges()
      One_Cut(graph, delta, c, orderb)
      if graph.edges() == edges:
        Cut = True
      else:
        Add = False
        
def Find_Many_Pairwise_Nashes(graph, delta, c, granularity):
  eqlist = []
  len = 1.0/granularity
  for l in frange(0,end = 1, inc = len):
    Coin_Flip_Graph(graph, l)
    Find_Pairwise_Nash(graph, delta, c)
    changedlist=[]
    if eqlist == []:
      eqlist.append(nx.to_dict_of_lists(graph))
    else:
      tru = 1
      for i in eqlist:
        if i == nx.to_dict_of_lists(graph):
          tru *= 0
      if tru == 1:
        eqlist.append(nx.to_dict_of_lists(graph))
  return eqlist
    
	
def Coin_Flip_Graph(graph, prob = .5):
  x = graph.nodes()
  for i in x:
    x = x[1:]
    for j in x:
      y = random.uniform(0,1)
      if y > prob:
        graph.add_edge(i,j)



#T = grapher("Toy2.csv")
#X = grapher("Toy2.csv")
#Coin_Flip_Graph(T, 1.01)
#Coin_Flip_Graph(X, .5)
#c = 1.01
#delta = 1
#Find_Pairwise_Nash(X)
#len(X.edges()) == len(T.edges())

#T = Coin_Flip_Graph(T, -.01)
#c = 0
#Find_Pairwise_Nash(X)
#len(X.edges()) == len(T.edges())
