from ComputePairwise import *
import unittest

delta = 1

class TestPairwise(unittest.TestCase):
  
  def setUp(self):
    return
  
  def test_none(self):
    T = grapher("Toy2.csv")
    X = grapher("Toy2.csv")
    Coin_Flip_Graph(T, 1.01)
    Coin_Flip_Graph(X, .5)
    Find_Pairwise_Nash(X, c = 1, delta = 1)
    self.assertEqual(len(T.edges()), len(X.edges()))
  
  def test_all(self):
    T = grapher("Toy2.csv")
    X = grapher("Toy2.csv")
    Coin_Flip_Graph(T, -.1)
    Find_Pairwise_Nash(X, c = 0, delta = .99)
    self.assertEqual(len(T.edges()), len(X.edges()))

  def test_many_all(self):
    X = grapher("Toy2.csv")
    self.assertEqual(len(Find_Many_Pairwise_Nashes(X, .99, 0, 5)), 1) 

  def test_none_all(self):
    X = grapher("Toy2.csv")
    self.assertEqual(len(Find_Many_Pairwise_Nashes(X, .99, 1, 5)), 1)
  	
if __name__ == '__main__':
  unittest.main()
  
