import sys, random
import networkx as nx
#import matplotlib.pyplot as plt
def file2edgelist(argv):
  if len(argv) < 3:
      print 'Usage:', argv[0], '<graph file> <# of edges to predict>'
      return

  try:
      graphfile = open(argv[1])
  except:
      print 'Error: Unable to open graph file.'
      sys.exit()

  try:
      num_edges = int(argv[2])
  except:
      print 'Error: Unable to parse # of edges from command line'
      sys.exit()

  nodes = set()
  edgelist = [] 
  for line in graphfile:
      try:
          n1, n2 = line.split()
      except:
          print 'Error: Malformed graph file.'
          return
      # Do duplicate links handling
      edgelist.append([n1,n2])
      nodes.add(n1)
      nodes.add(n2)
  #for i in range(num_edges):
  #    n1, n2 = random.sample(nodes, 2)
  #    print '%s\t%s' % (n1, n2)
  return edgelist, nodes

# test usage
def readfile():
  edgelist,nodes = file2edgelist(['basnet','model2-2.txt','3'])
  return edgelist
#file2edgelist(sys.argv)


# edgelist 2 Graph
def edgelist2graph(edgelist):
  G = nx.DiGraph()
  G.add_edges_from(edgelist)
  return G
#return ether strongly connected components
def getSubGraph(graph):
  listOfComponentNodes4ECC= nx.weakly_connected_components(graph)
  listOfComponentNodes4SCC = nx.strongly_connected_components(graph)
  #strongly connected components
  scc = []
  for i in range(0,len(listOfComponentNodes4SCC)):
    subgraph = graph.subgraph(listOfComponentNodes4SCC[i]) 
    scc.append(subgraph)
  # Weakly connceted components
  ecc = []
  for i in range(0,len(listOfComponentNodes4ECC)):
    subgraph = graph.subgraph(listOfComponentNodes4ECC[i])
    ecc.append(subgraph)
  print 'graph nodes size:        ' + str(len(graph.nodes()))
  print 'SCC   components number: ' + str(len(scc))
  print 'ECC   components number: ' + str(len(ecc))
  return scc,ecc


#draw graph
def draw(graph):
  pos = nx.graphviz_layout(graph,prog='twopi',args='')
  plt.figure(figsize=(8,8))
  nx.draw(graph,pos,node_size=100,alpha=0.1,node_color='blue',with_labels=True)
  plt=axis=('equal')
  plt.savfig('sub_graph.png')
  plt.show()

# prints 
def prints(edgelist):
  for edge in edgelist:
    print edge[0] +'\t' + edge[-1]

# Author: Zhuoli
# makePrediction at neighbors overlap method with list of communites
def makePredictionAtNOP(communities):
  buffers = []
  for comminity in communities:
    BUFFER = predictWithNeighborsOverLap(comminity)
    buffers.extend(BUFFER)
  return buffers
# Author: Zhuoli
# make prediction with neighbors overlap method in a community
def predictWithNeighborsOverLap(community):
  BUFFER = []
  visited = []
  for node in community.nodes():
    visited.append(node)
    neighbors = community.neighbors(node)
    for neighbor in neighbors:
      if not neighbor in visited:
        edge = [node,neighbor]
        numerator = (len(set(community.neighbors(neighbor)) & set(neighbors)) + 0.0)
        denominator = (len(set(community.neighbors(neighbor)) | set(neighbors)) + 0.1)
        rate = numerator / denominator
        if rate > 0:
          BUFFER.append([edge,rate])
  return BUFFER

# Author: xiaofeng
# get best machies
# Given a list of prediction and expected number
# A prediction is [ [pair], probability]
# Return a list of prediction
def getBestMaches(BUFFER,number):

  return BUFFER

# convert set of nodes to list of communities
def getCommunities(graph,setOfNodes):
  communities = []
  for nodes in setOfNodes:
    subgraph = graph.subgraph(list(nodes))
    communities.append(subgraph)
  return communities
