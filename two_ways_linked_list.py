class Node(object):
    
    def __init__(self, data, next = None):
        """Instantiates a Node with default next of None"""
        self.data = data
        self.next = next

class TwoWayNode(Node):

    def __init__(self, data, previous = None, next = None):
        Node.__init__(self, data, next)
        self.previous = previous

class TwoWayLinkedNode:
    """
    Class zalupa ebanay romanyk
    """

    def __init__(self):

        self.head = None
        self.tail = None

    def add(self, new_node):
        
        if self.tail == None:
            self.head = new_node
            self.tail = new_node
        else:
            prev_tail = self.tail
            tail.next = new_node
            new_node.previous = prev_tail
            self.tail = new_node

    def __iter__(self):
        pass



    
