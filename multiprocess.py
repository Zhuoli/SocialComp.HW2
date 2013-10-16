from multiprocessing import Queue
import multiprocessing
import time
import math
nprocs = 2
def deliverTask(starttime,graph,nbrsOutHash,nbrsInHash,nbrs,edgeHash):
  def predictor(nodes,starttime,out_q,edgeHash,nbrsOutHash,nbrsInHash,nbrs):
    outdict = {}
    visitedHash = {}
    for node in nodes:
      getPred4ThisNode(node,visitedHash,outdict,edgeHash,nbrsOutHash,nbrsInHash,nbrs)
    print 'update start time: ' + str(time.time() - starttime)
    out_q.put(outdict)
    print 'update end time: ' + str(time.time() - starttime)
    print 'child processing done!'
    
  out_q = Queue()
  nodes = graph.nodes()
  chunksize = int(math.ceil(len(nodes) / float(nprocs)))
  procs = []

  for i in range(nprocs):
    p = multiprocessing.Process(target = predictor,args = (nodes[chunksize * i: chunksize * (i+1)],starttime,out_q,edgeHash,nbrsOutHash,nbrsInHash,nbrs))
    procs.append(p)
    p.start()

  resultdict = {}
  for i in range(nprocs):
    print 'out_q get start time: ' + str(time.time() - starttime)
    resultdict.update(out_q.get())
    print 'out_q get done time: ' + str(time.time() - starttime)

  for p in procs:
    print 'Join'
    p.join()
  return resultdict.items()

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

