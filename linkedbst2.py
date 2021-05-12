"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
from math import ceil
from random import sample
import time

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):

            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)


        recurse(self._root)
        return lyst

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        node = self._root

        while True:
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                node = node.left
            else:
                node = node.right

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        node = self._root

        while True:
            if self.isEmpty():
                self._root = BSTNode(item)
                break

            elif item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                    break
                else:
                    node = node.left

            elif node.right == None:
                node.right = BSTNode(item)
                break
            
            else:
                node = node.right

        self._size += 1


    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        if self.isEmpty():
            return 0

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top == None:
                return -1
            else:
                return 1 + max(height1(top.left), height1(top.right))
        
        return height1(self._root)

         

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        height = self.height()
        size = self._size

        if height <= ceil(log(size + 1, 2) - 1):
            return True
        return False

    def rangeFind(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        lst = self.inorder()
        low_idx = lst.index(low)
        high_idx = lst.index(high)
        return lst[low_idx:high_idx+1]



    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        tree = self.inorder()
        self.clear()

        def recurse_split(tree):
            
            if len(tree) == 1:
                if self.find(tree[0]) == None:
                    self.add(tree[0])
                return

            else:

                need_idx = ceil((len(tree) - 1) / 2)

                node = tree[need_idx]
                self.add(node)
                if len(tree) % 2 == 0:
                    left_tree = tree[:ceil(len(tree) / 2)]
                    if len(tree) != 2:
                        right_tree = tree[-(need_idx-1):]
                    else:
                        right_tree = tree[-1:]
                else:
                    left_tree = tree[:ceil(len(tree) / 2)-1]
                    right_tree = tree[-(need_idx):]             

                recurse_split(left_tree)
                recurse_split(right_tree)
                return
        recurse_split(tree)

        return self


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """

        if self.find(item) == None:
            try:
                self.add(item)
                lst = self.inorder()
                item_idx = lst.index(item)
                output = lst[item_idx+1]
                self.remove(item)
                return output
            except IndexError:
                return None

        lst = self.inorder()
        item_idx = lst.index(item)
        try:
            output = lst[item_idx+1]
        except IndexError:
            return None
        return output

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        if self.find(item) == None:
            try:
                self.add(item)
                lst = self.inorder()
                item_idx = lst.index(item)
                output = lst[item_idx-1]
                self.remove(item)
                if item_idx == 0:
                    return None
                return output
            except IndexError:
                return None
        lst = self.inorder()
        item_idx = lst.index(item) - 1
        if item_idx == -1:
            return None
        output = lst[item_idx]
        return output   
    
    def lst_search(self,lst, lst_linear):
        time1 = time.time()
        self.clear()
        counter = 0
        for i in lst_linear:
            if i in lst_linear:
                counter += 1

        if counter == 10000:
            self.clear()
        
        end = time.time()
        return end - time1

    def linear_bstree(self,lst, lst_linear):
        time2 = time.time()
        counter = 0
        self.clear()
        for i in lst:
            self.add(i)
        
        for i in lst_linear:
            self.find(i)
            counter += 1
        

        self.clear()
        end = time.time()
        return end - time2

    def random_bstree(self,lst, lst_random):
        time3 = time.time()
        counter = 0
        self.clear()
        for i in lst:
            self.add(i)
        
        for i in lst_random:
            self.find(i)
            counter += 1
        

        self.clear()
        end = time.time()
        return end - time3

    def search_in_balanced(self,lst, lst_random):
        time4 = time.time()
        counter = 0
        tree_new = LinkedBST()
        for i in lst:
            tree_new.add(i)

        tree_new.rebalance()

        for i in lst_random:
            tree_new.find(i)
            counter += 1

        end = time.time()

        return end - time4


    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        lst = []

        with open(path,"r",encoding='utf-8') as output_file:
            for line in output_file:
                line = line.strip()
                lst.append(line)

        lst_random = sample(lst,10000)
        lst_linear = lst[:10000]
        lst = lst[:900]



        time1 = self.lst_search(lst, lst_linear)
        time2 = self.linear_bstree(lst, lst_linear)
        time3 = self.random_bstree(lst, lst_random)
        time4 = self.search_in_balanced(lst,lst_random)
        
        print(f"Search time for 10000 random words in alphabetically arranged list is {time1}")
        print(f"Search time for 10000 in order words in binary tree is {time2}")
        print(f"Search time for 10000 random words in binary tree is {time3}")
        print(f"Search time for 10000 random words in rebalanced binary tree is {time4}")

        return "Here is your time"

tree = LinkedBST()

# print(tree.demo_bst("wordss.txt"))

a = tree.demo_bst("wordss.txt")

print(a)