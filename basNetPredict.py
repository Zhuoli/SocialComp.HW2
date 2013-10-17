import sys, random
from collections import namedtuple
from numpy import array
#import matplotlib.pyplot as plt
def parsefile(argv):
  if len(argv) < 3:
      print 'Usage:', argv[0], '<graph file> <# of edges to predict>'
      sys.exit()

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
  inHash = {}
  outHash = {}
  nbrsHash = {}
  edgeHash = {}
  for line in graphfile:
      try:
          n1, n2 = line.split()
      except:
          print 'Error: Malformed graph file.'
          return
      # Do duplicate links handling
      edge = [n1,n2]
      edgeHash[tuple(edge)] = True
      outHash[n1] = [n2]
      inHash[n2] = [n1]
      edgelist.append([n1,n2])
      nodes.add(n1)
      nodes.add(n2)
  #for i in range(num_edges):
  #    n1, n2 = random.sample(nodes, 2)
  #    print '%s\t%s' % (n1, n2)
  
  nbrs = {}
  # initial node's degree hash table
  for node in nodes:
      outNeighbors = outHash.get(node)
      if outNeighbors == None:
          outNeighbors = []
      outHash[node] = list(set(outNeighbors))
      inNeighbors = inHash.get(node)
      if inNeighbors == None:
          inNeighbors = []
      inHash[node] = list(set(inNeighbors))
      outset = set(outHash[node])
      inset = set(inHash[node])
      nbrs[node] = list(outset | inset)
  return  nodes,edgeHash,outHash,inHash,nbrs

# test usage
def readfile():
  edgelist,nodes = file2edgelist(['basnet','model2-2.txt','3'])
  return edgelist
#file2edgelist(sys.argv)


# edgelist 2 Graph
def edgelist2graph(edgelist,inHash,outHash,nbrsHash,edgeHash):
  for edge in edgelist:
    edgeHash[tuple(edge)] = 1
    #get out link hash table
    neighbors = outHash[edge[0]]
    neighbors.append(edge[1])
    # get in link hash Table
    neighbors = inHash[edge[1]]
    neighbors.append(edge[1])
  return 


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
def prints(pairs):
  for pair in pairs:
    edge = pair[0]
    print str(edge[0]) + '\t' + str(edge[1])
# debug prints 
def debugPrints(pairs):
  for pair in pairs:
    edge = pair[0]
    priority = pair[-1]
    print 'link: ' + edge[0] +'\t' + edge[-1] + '\t, Priority: ' + str(priority) 

# Author: Zhuoli
# make Prediction  using Jaccard's coefficient method
def predictorAtCoefficient(nodes,edgeHash,nbrsInHash,nbrsOutHash,nbrsHash):
  items = predictWithNeighborsOverLapRate(nodes,edgeHash,nbrsOutHash,nbrsInHash,nbrsHash)
  return items
# Author: Zhuoli
# fullfill the neighbor hash sable
def getNeighborHash(graph):
  inHash = {}
  outHash = {}
  nbrs = {}
  nodes = graph.nodes()
  for node in nodes:
    outEdges = graph.out_edges(node)
    if len(outEdges) > 0:
      arrOut = array(outEdges)
      outNbors = list(arrOut[:,1])
      outHash[node] = outNbors
    else:
      outNbors = []
      outHash[node] = []
   
    inEdges  = graph.in_edges(node)
    if len(inEdges) > 0:
      arrIn = array(inEdges)
      inNbors  = list(arrIn[:,1])
      inHash[node]=inNbors
    else:
      inNbors = []
      inHash[node] = []
    nbrs[node] = list(set(outNbors) | set(inNbors)) 
  return inHash,outHash,nbrs
# get hashtable for community edges
def getEdgeHash(community):
  edgeHash = {}
  edges = community.edges()
  for edge in edges:
    edgeHash[tuple(edge)] = 1
  return edgeHash
# Author: Zhuoli
# make prediction with neighbors overlap
# rate method in a undirected community
def predictWithNeighborsOverLapRate(nodes,edgeHash,nbrsOutHash,nbrsInHash,nbrs):
#  print 'in predict with neighbor over lap rate'
  visitedHash ={}
  result = {}
  k = 1
  for node in nodes:
    #print 'loop: ' + str(k) +'\t' + '%.3f%% completed' % ((k*100 + 0.0)/ 97134) 
    k = k+1
    getPred4ThisNode(node,visitedHash,result,edgeHash,nbrsOutHash,nbrsInHash,nbrs)
  return result.items()

# get prediction for this node
def getPred4ThisNode(node,visitedHash,result,edgeHash,nbrsOutHash,nbrsInHash,nbrs):
  visitedHash[node] = True
  nodeNeighbors = list(set(nbrs[node]))
#   print 'first loop level node neighbors size: ' + str(len(nodeNeighbors))
  for nodeNeighbor in nodeNeighbors:
    subneighbors = nbrs[nodeNeighbor]
#   print 'second loop level subneighbors size: ' + str(len(subneighbors))
    for subneighbor in subneighbors:
#        print 'third loop level node size: ' + str(len(subneighbors))
        # omit connected links
      if subneighbor == node:
        continue
      if subneighbor in visitedHash:
        continue
      if tuple([subneighbor,node]) in edgeHash:
        continue
      if tuple([node,subneighbor]) in edgeHash:
        continue
      numerator = (len(set(nbrs[subneighbor]) & set(nodeNeighbors)) + 0.0)
      denominator = (len(set(nbrs[subneighbor]) | set(nodeNeighbors)) + 0.1)
      rate = numerator / denominator
      edge = tuple([subneighbor,node])
      result[edge] = rate
  return
# Author: Zhuoli
# make prediction using common neighbors method
def predictorAtCommonNeighbors(nodes,edgeHash,nbrsInHash,nbrsOutHash,nbrsHash):
  visited ={}
  result = {}
  for node in nodes:
    visited[node] = True
    nodeNeighbors = nbrsHash[node]
    for nodeNeighbor in nodeNeighbors:
      subneighbors = nbrsHash[nodeNeighbor]
      for subneighbor in subneighbors:
        # omit connected links
        if subneighbor == node:
          continue
        if visited.has_key(subneighbor):
          continue
        if edgeHash.has_key(tuple([subneighbor,node])):
          continue
        if edgeHash.has_key(tuple([node,subneighbor])):
          continue
        commons = (len(set(nbrsHash[subneighbor]) & set(nodeNeighbors)) + 0.0)
        edge = tuple([subneighbor,node])
        result[edge] = commons
  return result.items()
#predictor using Preferential attachment
def predictorAtPref(nodes,edgeHash,inHash,outHash,nbrsHash):
  prioHash = {}
  # build priority hash table, the nodes who share the same degree are in one key
  for node in nodes:
    neighbors = nbrsHash[node]
    degree = len(neighbors)
    if prioHash.has_key(degree):
      queue = prioHash[degree]
      queue.append(node)
    else:
      prioHash[degree] = [node]
  # 
  keys = prioHash.keys()
  keys.sort()
  return prioHash,keys

def getBestMatches4Pref(prioHash,keys,edgeHash,num):
  buffers = []
  for i in range(len(keys) - 1, -1,-1):
    nodes = prioHash[keys[i]]
    for a in nodes:
      for b in nodes:
        if tuple([a,b]) in edgeHash or tuple([b,a]) in edgeHash:
          continue
        if a == b:
          continue
        buffers.append([[a,b],keys[i]])
        num = num-1
        if num < 1:
          return buffers,0
  return buffers,num


# Author: Zhuoli
# get best machies
# Given a list of prediction and expected number
# A prediction is [ [pair], probability]
# Return a list of prediction
def getBestMaches(BUFFER,number):
  if len(BUFFER) ==0:
    return bests,number
  bests = sorted(BUFFER,key=lambda buf: buf[1])
  length = len(bests)
  if length > number:
    return bests[length - 1:length - number -1: -1],0
  else:
    return bests, number - length


# convert set of nodes to list of communities
def getCommunities(graph,setOfNodes):
  communities = []
  for nodes in setOfNodes:
    subgraph = graph.subgraph(list(nodes))
    communities.append(subgraph)
  return communities
