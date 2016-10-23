# Author:
# Damian Boland

class Node(object):
  def __init__(self, router):
    self.Router = router
    self.Children = []

  def add_node(self, newNode):
    self.Children.append(newNode)


