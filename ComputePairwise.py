#A Program To Solve Network Formation Games Computationally
#Max Gallop

#Need it to be non-recursive!
import networkx as nx
from itertools import *
from math import log
import matplotlib.pyplot as plt
def powerset(iterable):
  s = list(iterable)
  return list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))

#def dif(x, y):
#  return 1 - abs(x - y)
  

def utility(graph):
  util = {}
  delta = .5
  c = 0.1
  for i in graph.nodes():
    util[i] = 0
    for j in graph.nodes():
      if nx.has_path(graph, i, j):
        util[i] += (graph.node[j]["cap"]*(1-abs(graph.node[i]["ideo"]-graph.node[j]["ideo"]))*delta**nx.shortest_path_length(graph,i,j))
    util[i] = (util[i])**.5 - (c*len(graph.neighbors(i)))
  return util
  

def One_Add(graph):
  for i in graph.nodes():
    for j in graph.nodes():
      if i != j:
        if j not in G[i]:
          graphprime = nx.Graph()
          graphprime.add_nodes_from(graph)
          graphprime.add_edges_from(graph.edges())
          for k in graph.nodes():
            graphprime.node[k]["cap"], graphprime.node[k]["ideo"] = graph.node[k]["cap"], graph.node[k]["ideo"]
          graphprime.add_edge(i, j)
          if utility(graphprime)[i] > utility(graph)[i] and utility(graphprime)[j] > utility(graph)[j]:
            graph.add_edge(i,j)
          else:
            graphprime.remove_edge(i, j)

def One_Cut(graph): 
  for i in graph.nodes():
    graphprime = graph
    x = []
    for nodes in G[i]:
      x.append(nodes)
    possibilities = list(powerset(x))
    x, y = graph.node[i]["cap"], graph.node[i]["ideo"]
    graphprime = nx.Graph()
    graphprime.add_nodes_from(graph)
    graphprime.add_edges_from(graph.edges())
    graphprime.remove_node(i)
    graphprime.add_node(i)
    for i in graph.nodes():
      graphprime.node[i]["cap"], graphprime.node[i]["ideo"] = graph.node[i]["cap"], graph.node[i]["ideo"]
    for j in possibilities:
      for k in j:
        graphprime.add_edge(i, k)
      if utility(graphprime)[i] > utility(graph)[i]:
        graph.add_edges_from(graphprime.edges())
      else:
        for k in j:
          graphprime.remove_edge(i, k)

def Find_Pairwise_Nash(graph):
  Done, Add, Cut = False, False, False
  while Done == False:
    if Add and Cut == True:
      Done = True
    while Add == False:
      x = graph.edges()
      One_Add(graph)
      if graph.edges() == x:
        Add = True
      else:
        Cut = False
    while Cut == False:
      Add = False
      x = graph.edges()
      One_Cut(graph)
      if graph.edges() == x:
        Cut = True
      else:
        Add = False

G = nx.Graph()
G.add_nodes_from(["US", "UK", "China", "Russia", "France", "Japan", "Germany", "Iran"])
G.node["US"]['cap'] = 1
G.node["China"]['cap'] = .8
G.node["Russia"]['cap'] = .5
G.node["UK"]['cap'] = .6
G.node["France"]['cap'] = .4
G.node["Germany"]['cap'] = .8
G.node["Japan"]['cap'] = .8
G.node["Iran"]['cap'] = .1


G.node["US"]['ideo'] = 1
G.node["China"]['ideo'] = .2
G.node["Russia"]['ideo'] = .2
G.node["UK"]['ideo'] = 1
G.node["France"]['ideo'] = .9
G.node["Germany"]['ideo'] = 1
G.node["Japan"]['ideo'] = 1
G.node["Iran"]['ideo'] = 0
G.nodes()

Find_Pairwise_Nash(G)
nx.draw(G)
plt.draw()
plt.savefig("MidExternMidCost.png")

