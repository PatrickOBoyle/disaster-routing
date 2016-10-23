# Author:
# Damian Boland

import Node
class Tree(object):
  def __init__(self):
    self.Head = None

  def add_node(self,node, parent):
    if self.Head is None:
      self.Head = node
      return
    parent = self.look_up(parent)
    parent.add_node(node)
  
  def look_up(self, parent):
    myNode, Found = self.look_up_rec(parent ,self.Head, False )
    if Found:
      return myNode
    
  def look_up_rec(self, node, parent, found):
    if(node.Router== parent.Router):
      found = True
      return parent, found
    children = parent.Children
    if not children:
      return None, False
    i= 0
    while not found and i < len(children):
      child = children[i]
      parent, found = self.look_up_rec(node,child, found)
      i+=1
    return parent, found
  def find_route(self, routerToFind):
    if routerToFind.Router == self.Head.Router:
      return None
    Found = False
    children = self.Head.Children
    myChild = None
    i = 0
    while not Found and i < len(children):
      myChild = children[i]
      if myChild.Router == routerToFind.Router:
	return myChild.Router
      Found = self.find_route_rec(routerToFind, myChild, Found)
      i +=1
    if Found:
      return myChild.Router
  def find_route_rec(self, router, child, found):
    if router.Router == child.Router:
      return True
    i = 0
    children = child.Children
    while i < len(children) and not found:
      if child.Router == router.Router:
	return True		
      child = children[i]
      found = self.find_route_rec(router, child, found)
      i+=1
    if found:
      return True
    return False
    



