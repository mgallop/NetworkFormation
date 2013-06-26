from ComputePairwise import *
from joblib import Parallel, delayed

starts = [0, .33, .66, 1]
#starts = frange(0,1,.1)*4

G = grapher("MyFile.csv")

x = []
for i in starts:
  Coin_Flip_Graph(G, i)
  new = G.copy()
  x.append(new)

if __name__ == '__main__':
  results = Parallel(n_jobs = -1, verbose = 10)(delayed(Find_Pairwise_Nash)(i, .8, .2) for i in x)
  
result = []
for i in results:
  if i.edges() not in result:
    result.append(i.edges())


G = grapher("Toy2.csv")
params = [[.7, .05], [.4,.1],[.7, .1],[.4, .05]]
  
if __name__ == '__main__':
  results2 = Parallel(n_jobs = -1, verbose = 10)(delayed(Find_Pairwise_Nash)(G, i[0], i[1]) for i in params)
  
result2 = []
for i in results2:
  if i.edges() not in result2:
    result2.append(i.edges())


	
	
