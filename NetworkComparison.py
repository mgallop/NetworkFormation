import networkx as nx


def degreedist(graph):
  d = {}
  for i in graph.nodes():
    x = graph.degree(i)
    if x in d:
      d[x] += 1
    else:
      d[x] = 1
  return d

def geodesicdist(graph):
  g = {}
  for i in graph.nodes():
    for j in graph.nodes():
      if i != j:
        if not nx.has_path(graph, i, j):
          x = "None"
        else:
          x = nx.shortest_path_length(graph, i, j)
          if x in g:
            g[x] += .5
          else:
            g[x] = .5
  return g  

def triaddist(graph):
  t = {0:0, 1:0, 2:0, 3:0}
  for i in graph.nodes():
    for j in graph.nodes():
      for k in graph.nodes():
        x = 0
        if i in nx.neighbors(graph, j):
          x += 1
        if i in nx.neighbors(graph, k):
          x += 1
        if j in nx.neighbors(graph, k):
          x += 1
        t[x] += 1
  for q in t:
    t[q] /= 6
  return t

def sharedpartnerdist(graph):
  s = {}
  for i in graph.nodes():
    for j in graph.nodes():
      if nx.has_path(graph,i,j):
        if nx.shortest_path_length(graph, i, j) == 1:
          x = 0
          for k in graph.neighbors(j):
            x += 1
          if x in s:
            s[x] += .5
          else:
            s[x] = .5
  return s
  
G = nx.Graph()
G.add_nodes_from(["US", "UK", "China", "Russia", "France", "Japan", "Germany", "Iran"])

G.add_edge("US", "UK")
G.add_edge("US", "Russia")
G.add_edge("US", "Germany")

y = degreedist(G)
print y