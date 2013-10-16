from multiprocessing import Process,Manager,Queue,Pipe
from collections import namedtuple
import time
import sys
process_num = 2
def deliverTask(starttime,graph,nbrsOutHash,nbrsInHash,nbrs,edgeHash):
  def processingWithNeighborsOverLapRate(nodes,start,starttime,child_conn,args):
    print 'we are in process ' + str(start)
    edgeHash = args.edgeHash
    nbrsOutHash = args.nbrsOutHash
    nbrsInHash = args.nbrsInHash
    nbrs = args.nbrs
    localresult = {}
    localvisitedHash = {}
    for node in nodes:
      getPred4ThisNode(node,localvisitedHash,localresult,edgeHash,nbrsOutHash,nbrsInHash,nbrs)
    print 'update start time: ' + str(time.time() - starttime)
    child_conn.send(localresult)
    print 'update end time ' + str(time.time() - starttime)
    print 'child processing done!'
    return


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
  connections = []
  for num in range(0,process_num):
    parent_conn,child_conn = Pipe()
    connections.append([parent_conn,child_conn])

  nodes = graph.nodes()
  process = []
  Args = namedtuple('Args',['edgeHash','nbrsOutHash','nbrsInHash','nbrs'])
  args = Args(edgeHash,nbrsOutHash,nbrsInHash,nbrs)
  nodes_size = len(nodes)
  subnodes_size = nodes_size / process_num
  start = 0
  print 'Start to create process  time: ' + str(time.time() - starttime)
  for connpair in connections: 
    subnodes = nodes[start:start+subnodes_size]
    p = Process(target = processingWithNeighborsOverLapRate,
        args = (subnodes,start,starttime,connpair[1],args))
    process.append(p)
    p.start()
    start += subnodes_size
  print 'Start to run process  time: ' + str(time.time() - starttime)
  result = {}
  ps = len(process)
  for connpair in connections:
    parent_conn = connpair[0]
    rev= parent_conn.recv()
    result.update(rev)
  #print rev
  for t in process:
    print 'Join'
    t.join()

  print 'Deliver Done time: ' + str(time.time() - starttime)
  print str(ps) + ' process worked'
  return result.items()


