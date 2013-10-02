import sys, random
import networkx as nx
import matplotlib.pyplot as plt
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

# get prediction in SCC
def getPredictionInSCC(scc,number):
  # put the likely connected links to prediction
  prediction = []
  for subgraph in scc:
    triadicClosurePrediction = getTriadicClosurePrediction(subgraph)
    if len(triadicClosurePrediction) > 0:
      prediction.extend(triadicClosurePrediction)
  return prediction

# ge prediction in WCC
def getPredictionInWCC(wcc,number):
  # put the likely connected links to prediction
  prediction = set()
  for subgraph in wcc:
    triadicClosurePrediction = getTriadicClosurePrediction(subgraph)
    if len(triadicClosurePrediction) > 0:
      prediction.update(triadicClosurePrediction)
  # if predicted links less than requirement, 
  if len(prediction) < number:
    links = getFamiliarMostPrediction(wcc,number)
    if len(links) > 0:
      predition.update(links)

  return list(prediction)

# get familiar most prediction
def getFamiliarMostPrediction(graphlist,number):
  links = set()
  for graph in graphlist:
    links.update(familiarPrediction(graph))
  return links

# get familiar most prediction in one graph
def familiarPrediction(graph):
  linksSet = set()

  return linksSet

def unionSet(listA,listB):
  return 0

# get the Triadic Closure Prediction
def getTriadicClosurePrediction(graph):
  prediction = []
  doubleLinkedNodes = set()
  for vertex in graph.nodes():
    # set up link for each Triadic Clousre
    possibleNodes = []
    neighbors = graph.neighbors(vertex)
    for neighbor in neighbors:
      # if its neighbour also points back
      if vertex in graph.neighbors(neighbor):
        possibleNodes.append(neighbor)
    links4thisvertex = predictionLinks(possibleNodes,graph)
    if len(links4thisvertex) > 0:
      prediction.extend(links4thisvertex)
  return prediction

# get prediction links
def predictionLinks(nodes,graph):
  if len(nodes) < 2:
    return []
  links = []
  edgelist = graph.edges()
  for a in nodes:
    for b in nodes:
      if not a == b:
        if [a,b] not in edgelist:
          links.append([a,b])
  return links


def getOutDuplicateFrom(linksA,linksB):
  links = []
  for link in linksA:
    if link not in linksB:
      links.append(link)
  return links
