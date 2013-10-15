from multiprocessing import Process,Manager
from collections import namedtuple

process_num = 2
def deliverTask(graph,nbrsOutHash,nbrsInHash,nbrs,edgeHash):
  manager = Manager()
  visitedHash = manager.dict()
  result = manager.dict()
  k = manager.Value('L',1)


  nodes = graph.nodes()
  process = []
  Args = namedtuple('Args',['edgeHash','nbrsOutHash','nbrsInHash','nbrs'])
  Resours = namedtuple('Resours',['visitedHash','result','k'])
  args = Args(edgeHash,nbrsOutHash,nbrsInHash,nbrs)
  resours = Resours(visitedHash,result,k)
  nodes_size = len(nodes)
  subnodes_size = nodes_size / process_num
  start = 0
  for num in range(0,process_num):
    subnodes = nodes[start:start+subnodes_size]
    p = Process(target = processingWithNeighborsOverLapRate,
        args = (subnodes,start,resours,args))
    process.append(p)
    start += subnodes_size
  for p in process:
    p.start()

  ps = len(process)
  for t in process:
    t.join()

  print 'Deliver Done!'
  print str(ps) + ' process worked'
  print 'result size: ' + str(len(result))
  return result.items()


def processingWithNeighborsOverLapRate(nodes,start,resours,args):
  print 'we are in process ' + str(start)
  try:
    visitedHash = resours.visitedHash
    result =resours.result
    k = resours.k
    edgeHash = args.edgeHash
    nbrsOutHash = args.nbrsOutHash
    nbrsInHash = args.nbrsInHash
    nbrs = args.nbrs
    for node in nodes:
      print 'loop: ' + str(k.value) + '\t' + '%.3f%% completed' % ((k.value*100 + 0.0)/97134)
      k.value = k.value + 1
      getPred4ThisNode(node,visitedHash,result,edgeHash,nbrsOutHash,nbrsInHash,nbrs)
  except:
     print 'Something wrong'
     raise



# get prediction for this node
def getPred4ThisNode(node,visitedHash,result,edgeHash,nbrsOutHash,nbrsInHash,nbrs):
  visitedHash[node] = True
  nodeNeighbors = nbrs[node]
  for nodeNeighbor in nodeNeighbors:
    subneighbors = nbrs[nodeNeighbor]
    for subneighbor in subneighbors:
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
