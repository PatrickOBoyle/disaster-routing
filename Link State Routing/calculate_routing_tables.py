# Author:
# Damian Boland

import os
import socket
import sys
import Tree
import Node
import csv
#ransRange = 100
 
def create_routing_tables():
  path = "config/network_map.csv"
  routerNodes = get_router_nodes(path)
  
  ports = []
  tables = []
  
  for node in routerNodes:
    port = node[0]
    shortestHops=init_hop_List(routerNodes, port)
    shortestHops = shortest_path(shortestHops, routerNodes)
    myTree = build_Tree(shortestHops, routerNodes)
    table= []
    table = build_table(myTree, table, shortestHops)
    
    ports.append(port)
    tables.append(table)
  return ports, tables

def find_next_dest(table, destination):
  for i in range(len(table)):
    path = table[i]
    router = path[0]
    if router == destination:
      nxt = int(path[1])
      return nxt
    
def build_Tree(hopList, routerInfo):

  tree = Tree.Tree()
  hopList = reset_hopList_bool(hopList)

  routersInTree = []
  portInfo, hopList= find_smallest(hopList)
  port = portInfo[0]
  routersInTree.append(port)
  head= Node.Node(port)
  tree.add_node(head, None)
  nxtPort = port
  parent = tree.look_up(head)
  while len(routersInTree) != len(hopList):
 
    neighbours = get_neighbours(nxtPort, routerInfo)
    if neighbours is None:
      break
    
    for i in range(len(neighbours)-1):
      myPort = neighbours[i]
      if not check_node_in_tree(routersInTree, myPort):
	child = Node.Node(myPort)

	routersInTree.append(myPort)
	tree.add_node(child, parent)
    
    parentInfo, hopList = find_smallest(hopList)
    nxtPort = parentInfo[0]
    parent = Node.Node(nxtPort)	      #must pass a not to the look_up function
    parent = tree.look_up(parent)     #finding the parent in the tree.     
  return tree
def check_node_in_tree(nodes, newNode):
  for i in range(len(nodes)):
    if newNode == nodes[i]:
      return True

  return False
#routerInfo, the router and who that routers neighbours are 
def shortest_path(hopList,routerInfo ):
  while True:
    myRouterInfo, hopList= find_smallest(hopList)
    if myRouterInfo[0] is None:
      return hopList
    myRouter = myRouterInfo[0]
    myHops = myRouterInfo[1]
    neighbours= get_neighbours(myRouter, routerInfo)  
    for i in range(len(neighbours)):
      router = neighbours[i]
      for i in range(len(hopList)):
	routerChk = hopList[i]
	routerToFind = routerChk[0]
	hops = routerChk[1]
	if routerToFind == router:
	  if (myHops+1) < hops:
	    routerChk[1] = myHops+1
	    hopList[i] = routerChk
	    break
  	     
  

def build_table(myTree, myTable, hopList):
  for i in range(len(hopList)):
    routerInfo = hopList[i]
    router = routerInfo[0]
    myNode = Node.Node(router)
    path=myTree.find_route(myNode)
    receiver = path
    route = (router ,receiver )
    myTable.append(route)
  return myTable
def create_empty_table(hopList):
  table = []
  for i in range(len(hopList)):
    route = []
    routerInfo = hopList[i]
    router = routerInfo[0]
    route.append(router)
    route.append(None)
    table.append(route)  
  
  return table
#find routers in range of a given router
def get_neighbours(myRouter, routerInfo):
  neighbours = None
  for i in range(len(routerInfo)):
    router = routerInfo[i]
    if myRouter == router[0]:
      neighbours= router[1]
      break
  return neighbours

#find router with smallest number of hops to it, that hasnt been checked already
def find_smallest(hopList):  
  nxtRouter = None
  smallest = 2000
  for i in range(len(hopList)):
    routerInfo = hopList[i]
    check = routerInfo[2]
    if not check:
      if smallest> routerInfo[1]:
	smallest = routerInfo[1]
	nxtRouter = routerInfo[0]
	

  for i in range(len(hopList)):    #ensure the same router isn't checked more then once
    routerInfo = hopList[i]
   
    if nxtRouter == routerInfo[0]:
      routerInfo[2] = True
      hopList[i] = routerInfo
      break
  info = (nxtRouter, smallest)
  return info, hopList

def reset_hopList_bool(hopList):
  for i in range(len(hopList)):
    routerInfo = hopList[i]
    routerInfo[2] = False
    hopList[i] = routerInfo
  return hopList

#initializing the number of hops from this router to another 
def init_hop_List(routers, myRouter):
  hopList = []
  check = False
  for i in range(len(routers)):
    routerInfo = []
    nodeInfo = routers[i]
    node = nodeInfo[0]
    hops =  (sys.maxint - 1)
    routerInfo.append(node) #the node, the number of hops to that node and if that nodes path has been checked
    if myRouter == node:
      hops = 0
    routerInfo.append(hops)
    routerInfo.append(check)
    hopList.append(routerInfo) 
     
  return hopList;
def get_router_nodes(network_map_path):
    # list of all nodes
    router_nodes = []
   
    with open(network_map_path, "r") as network_map:
        # get a list of all routers and connections, IE - Create nodes
        reader = csv.reader(network_map, delimiter=',')
       
        for row in reader:
	    connections = row[1].split(' ')
            router_node = (row[0], connections)
            router_nodes.append(router_node)
    return router_nodes
