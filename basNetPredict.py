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
# make Prediction  using Jaccard's coefficient method
def predictorAtCoefficient(communities):
  bufferHash = {}
  for comminity in communities:
    predictWithNeighborsOverLapRate(comminity,bufferHash)
  items = bufferHash.items()
  return items
# Author: Zhuoli
# make prediction with neighbors overlap
# rate method in a undirected community
def predictWithNeighborsOverLapRate(community,bufferHash):
  visited = []
  for node in community.nodes():
    nodeNeighbors = community.neighbors(node)
    for nodeNeighbor in nodeNeighbors:
      subneighbors = community.neighbors(nodeNeighbor)
      subneighbors.remove(node)
      for subneighbor in subneighbors:
        # omit connected links
        if tuple([subneighbor,node]) in community.edges():
          continue
        if tuple([node,subneighbor]) in community.edges():
          continue
        numerator = (len(set(community.neighbors(subneighbor)) & set(nodeNeighbors)) + 0.0)
        denominator = (len(set(community.neighbors(subneighbor)) | set(nodeNeighbors)) + 0.1)
        rate = numerator / denominator
        edge = tuple([subneighbor,node])
        if edge in bufferHash:
          value = bufferHash[edge]
          if rate > value:
            bufferHash[edge]=rate
            bufferHash[tuple(edge[-1],edge[0])] = rate
        else:
          bufferHash[edge] = rate
          bufferHash[tuple([edge[-1],edge[0]])] = rate
  return 
# Author: Zhuoli
# make prediction using common neighbors method
def predictorAtCommonNeighbors(communities):
  bufferHash = {}
  for comminity in communities:
    predictAtCommonNeighbors(comminity,bufferHash)
  items = bufferHash.items()
  return items

# make prediction using common neighbors method in one community
def predictAtCommonNeighbors(community,bufferHash):
  visited = []
  for node in community.nodes():
    nodeNeighbors = community.neighbors(node)
    for nodeNeighbor in nodeNeighbors:
      subneighbors = community.neighbors(nodeNeighbor)
      subneighbors.remove(node)
      for subneighbor in subneighbors:
        # omit connected links
        if tuple([subneighbor,node]) in community.edges():
          continue
        if tuple([node,subneighbor]) in community.edges():
          continue
        commons = (len(set(community.neighbors(subneighbor)) & set(nodeNeighbors)) + 0.0)
        edge = tuple([subneighbor,node])
        if edge in bufferHash:
          value = bufferHash[edge]
          if commons > value:
            bufferHash[edge]= commons
            bufferHash[tuple(edge[-1],edge[0])] = commons
        else:
          bufferHash[edge] = commons
          bufferHash[tuple([edge[-1],edge[0]])] = commons
  return

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
