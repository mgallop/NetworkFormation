#A Program To Solve Network Formation Games Computationally
#Max Gallop

import networkx as nx
from itertools import *
from math import log
from math import hypot
import time
import csv
import random
import copy


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
  return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def powerset2(seq):
  if len(seq) <= 1:
    yield seq
    yield []
  else:
    for item in powerset2(seq[1:]):
      yield [seq(0)] + item
      yield item

###CHANGE THIS FUNCTION IF YOU WANT TO CHANGE THE UTILITY FUNCTION  
## Anna Utility Function 3
def utility2(graph,actor, delta = 1, c = 0):
  util = {}
  for i in graph.nodes():
    util[i] = 0
    for j in graph.nodes():
      if nx.has_path(graph, i, j):
       util[i] += (graph.node[j]["cap"]*(1-abs(graph.node[i]["ideo"]-graph.node[j]["ideo"]))*delta**(nx.shortest_path_length(graph,i,j)))
    util[i] = (util[i])**.5 - (c*len(graph.neighbors(i)))
  return util[actor]

def utility(graph, actor, delta, c):
  Z = nx.shortest_path_length(graph, actor)
  utilz = 0
  for i in Z.keys():
    utilz += (graph.node[i]["cap"]*(1-abs(graph.node[i]["ideo"]-graph.node[actor]["ideo"]))*delta**(Z[i]))
  utilz **= .5
  utilz -= c*nx.degree(graph, actor)
  return utilz
	

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
        if utility(graphprime,i,delta, c) > utility(graph, i,delta, c) and utility(graphprime,j, delta, c) > utility(graph, j,delta, c):
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
    possibilities = powerset(x)#                  # all possible subsets of (i)'s neighbors
    graphprime = copy.deepcopy(winner)
    y = graph.edges(i)
    graphprime.remove_edges_from(y)
    #print i, 'old neighbors:', graph[i]
    for j in possibilities:#                            # in each potential subgroup of i's neighbors
      for k in j:#                                      # for each member of that subgroup
        graphprime.add_edge(i, k)#                      # connect it to (i)
      if utility(graphprime,i, delta, c) > utility(winner, i, delta, c):
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
  path = []
  Done, Add, Cut = False, False, False
  while Done == False:
    if Add and Cut == True:
      Done = True
    while Add == False:
      print "Adding:", time.clock()
      edges = graph.edges()
      One_Add(graph, delta, c, orderb)
      if graph.edges() == edges:
        Add = True
      else:
        Cut = False ###Track outcomes, if improving cycle, break and retry with new order.
        if nx.to_dict_of_lists(graph) in path:
          Coin_Flip_Graph(graph, random.uniform(0,1))
          print "Uh Oh, an improving cycle. Shuffling and trying again!"
          Find_Pairwise_Nash(graph, delta, c)
          Add, Cut = True, True
          break
        else:
          path.append(nx.to_dict_of_lists(graph))
    while Cut == False:
      print "Cutting:", time.clock()
      Add = False
      edges = graph.edges()
      One_Cut(graph, delta, c, orderb)
      if graph.edges() == edges:
        Cut = True
      else:
        Add = False
        if nx.to_dict_of_lists(graph) in path:
          Coin_Flip_Graph(graph, random.uniform(0,1))
          print "Uh Oh, an improving cycle. Shuffling and trying again!"
          Find_Pairwise_Nash(graph, delta, c)
          Add, Cut = True, True
          break
        else:
          path.append(nx.to_dict_of_lists(graph))
  return graph.copy()
        
def Find_Many_Pairwise_Nashes(graph, delta, c, granularity):
  eqlist = []
  figs = 0
  len = 1.0/granularity
  for l in frange(0,end = 1, inc = len):
    Coin_Flip_Graph(graph, l)
    Find_Pairwise_Nash(graph, delta, c)
    changedlist=[]
    if nx.to_dict_of_lists(graph) not in eqlist:
      eqlist.append(nx.to_dict_of_lists(graph))
      plt.clf()
      nx.draw_circular(graph)
      plt.draw()
      plt.savefig("Eq" + str(figs)+".png")
      figs += 1   
  return eqlist
    
    
def Coin_Flip_Graph(graph, prob = .5):
  x = graph.nodes()
  graph.remove_edges_from(graph.edges())
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


def One_Add2(graph, delta, c,  order = 3):
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
        if utility2(graphprime,i,delta, c) > utility2(graph, i,delta, c) and utility2(graphprime,j, delta, c) > utility2(graph, j,delta, c):
          graph.add_edge(i,j)
            #print i, 'adds:      ', j
            

			
def One_Cut2(graph, delta, c, order = 3): 
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
      if utility2(graphprime,i, delta, c) > utility2(winner, i, delta, c):
        winner = copy.deepcopy(graphprime)
        #print i, 'winner' , j
      for k in j:
        graphprime.remove_edge(i, k)#
    graph.remove_edges_from(graph.edges())          
    graph.add_edges_from(winner.edges())
    #print i, 'new neighbors:', winner[i]               

    
def Find_Pairwise_Nash2(graph, delta, c, orderb = 3):
  path = []
  Done, Add, Cut = False, False, False
  while Done == False:
    if Add and Cut == True:
      Done = True
    while Add == False:
      print "Adding:", time.clock()
      edges = graph.edges()
      One_Add2(graph, delta, c, orderb)
      if graph.edges() == edges:
        Add = True
      else:
        Cut = False ###Track outcomes, if improving cycle, break and retry with new order.
        if nx.to_dict_of_lists(graph) in path:
          Coin_Flip_Graph(graph, random.uniform(0,1))
          print "Uh Oh, an improving cycle. Shuffling and trying again!"
          Find_Pairwise_Nash2(graph, delta, c)
          Add, Cut = True, True
          break
        else:
          path.append(nx.to_dict_of_lists(graph))
    while Cut == False:
      print "Cutting:", time.clock()
      Add = False
      edges = graph.edges()
      One_Cut2(graph, delta, c, orderb)
      if graph.edges() == edges:
        Cut = True
      else:
        Add = False
        if nx.to_dict_of_lists(graph) in path:
          Coin_Flip_Graph(graph, random.uniform(0,1))
          print "Uh Oh, an improving cycle. Shuffling and trying again!"
          Find_Pairwise_Nash2(graph, delta, c)
          Add, Cut = True, True
          break
        else:
          path.append(nx.to_dict_of_lists(graph))
