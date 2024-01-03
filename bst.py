# Name: Vincewa Tran
# OSU Email: tranvinc@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: assignment4
# Due Date: 11/20/2023
# Description: This program implements a BST ADT containing a BSTNode,
# represents a node in the tree with a value and its left and right children,
# BST is the tree itself with an initialized root node at None.
# there are methods for adding, add(), to the tree removal, remove(), from the
# tree** expanded below
# the following methods
# contains() - a find method that confirms if a value with that node exists
# inorder_traversal() - a method that returns the path, as a queue object, for
# the inorder traversal
# find_min(), find_max() - methods that return the value of the nodes with
# the smallest and largest values
# is_empty() - which returns True if the tree is empty and False otherwise
# make_empty() - that clears the tree completely
# **remove() is the biggest method of this program when accounting for its
# helpers and sub methods
# _find_node_parent() - HELPER that finds the node to remove and its parent
# using a value passed in by the user
# _remove_no_subtrees() - removal case for no left or right children
# _remove_one_subtree() - removal case for left XOR right children
# _remove_two_subtrees() - removal case for a node with both left and right
# children. This is the most complicated case where the method swaps the node
# to be removed with its inorder successor updates values and deletes the
# node to be deleted


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        RECEIVES: value to add
        RETURNS: None
        CONDITIONS:
        1) if the tree is empty, set root node as node(value)
        2) if value is less than curr value move left in the tree
        3) if value is >= curr value move right in the tree
        while moving left or right if the child in that direction is none
        set our node(value) there.
        VARIABLES: curr_node as our pointer/parent as we visit nodes, new node
        with value created upon add, imp values[leftchild, rightchild]
        ------------------------------------------------------------------------
        Adds a value to the tree once an empty left or right child that
        satisfies our conditions is found.
        DUPLICATES ALLOWED, COMPLEXITY O(N)
        """
        # COND 1,
        if not self._root:
            self._root = BSTNode(value)
            return

        # create tracker
        cur_node = self._root

        while cur_node:
            # COND 2
            if value < cur_node.value:
                if not cur_node.left:
                    cur_node.left = BSTNode(value)
                    return
                cur_node = cur_node.left
            else:
                if not cur_node.right:
                    cur_node.right = BSTNode(value)
                    return
                cur_node = cur_node.right

    def remove(self, value: object) -> bool:
        """
        *using variables of the pseudocode in Explorations: BST Operations**
        RECEIVES: value of node to remove k_q
        RETURNS: True if there was a removal and False otherwise
        CONDITIONS: node to remove is found
        CASE 1) removal of node with no subtrees -> _remove_no_subtrees
        CASE 2) removal of node with one subtree -> _remove_one_subtree
        CASE 3) removal of node with two subtrees -> _remove_two_subtrees
        VARIABLES: n=node[to remove], pn=its parent, k_q=removal target value
        Method that removes a passed in target value by first searching for
        the value using a helper method _find_node_parent, returns False if
        the search returns None for n, otherwise it continues to the three
        cases above and returns True after removal.
        """

        # find node and node parent
        node, node_parent = self._find_node_parent(value)

        if node is None:
            return False

        # case 1, no children -> _remove_no_subtrees(pn, n)
        if not node.left and not node.right:
            self._remove_no_subtrees(node_parent, node)
        # case 3, two children -> _remove_two_subtrees(pn, n)
        elif node.left and node.right:
            self._remove_two_subtrees(node_parent, node)
        # case 2, one child -> _remove_one_subtree(pn, n)
        else:
            self._remove_one_subtree(node_parent, node)
        return True

    def _find_node_parent(self, key) -> object:
        """
        *using variables of the pseudocode in Explorations: BST Operations**
        RECEIVES: key as k_q or our target value for the search
        RETURNS: Value of n= the node to remove, and pn=its parent
        CONDITIONS: the current node or node to remove can't be None to
        continue the search, if nothing is returned inside the loop both the
        node to remove and its parent are returned as None, None.
        VARIABLES: key=k_q[removal target], n=cur_node, pn=parent
        Helper function for remove that returns the removal target and its
        parent None is returned for both if not found.
        """
        # start search at root init p to none
        cur_node = self._root
        parent = None
        # while n is not none
        while cur_node:
            # if n.key is k_q return node to remove and its parent
            if cur_node.value == key:
                return cur_node, parent
            # if k_q is less than n.key, pn<-n and n <- n.left
            elif key < cur_node.value:
                parent = cur_node
                cur_node = cur_node.left
            # if k_q is >= than n.key, pn<-n and n <- n.right
            else:
                parent = cur_node
                cur_node = cur_node.right

        # node is not found
        return None, None

    def _remove_no_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        <-[back to] remove
        RECEIVES: (pn, n) *variables expanded on in remove method docstring
        RETURNS: None
        CONDITIONS: passes case 1 in remove
        VARIABLES: node to remove and its parent
        A removal of a node with no children
        """
        # remove node that has no subtrees (no left or right nodes)
        if not remove_parent:
            self._root = None
        elif remove_parent.left == remove_node:
            remove_parent.left = None
        else:
            remove_parent.right = None

    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        <-[back to] remove
        RECEIVES: (pn, n) *variables expanded on in remove method docstring
        RETURNS: None
        CONDITIONS: passes case 2 in remove,
        subcases:
        1) if n.left is not empty our subtree is left
        2) else one_subtree is right
        VARIABLES: node to remove and its parent. one_subtree as our only
        subtree left or right
        A removal of a node with one child [left XOR right]
        """
        # remove node that has a left or right subtree (only)
        one_subtree = remove_node.left if remove_node.left else remove_node.right
        # if pn is none than n[removal target] was the root once its removed
        # the one_subtree becomes the root
        if not remove_parent:
            self._root = one_subtree
        # else update the pn's subchild to the removal nodes subchild based
        # on whether it's the left or right that = node to be removed
        elif remove_parent.left == remove_node:
            remove_parent.left = one_subtree
        else:
            remove_parent.right = one_subtree

    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        <-[back to] remove
        RECEIVES: (pn, n) *variables expanded on in remove method docstring
        RETURNS: None
        CONDITIONS: passes case 3 in remove, this method's cases below
        CASES 1) if ps is not n, update ps.left <- s.right, s.right <- n.right
        CASE 2) if pn is None therefore n = root, self._root <- successor
        CASE 3) if n[to remove] is a left child, pn.left <- successor
        CASE 4) if not 3 then n is a right child, pn <- successor
        VARIABLES: n = [n to remove], pn its parent, s[n.inorderS], ps[s's
        parent]
        A removal of a node with two children, correctly updates the values
        of the whole left by the removal as well as its children based on the cases above
        """
        # set successor to right and start going along its left most nodes
        successor_parent = remove_node
        # inorder successor
        successor = remove_node.right
        # while there's a left node to traverse left
        while successor.left:
            # ps becomes s
            successor_parent = successor
            successor = successor.left

        # Case 1
        if successor_parent != remove_node:
            successor_parent.left = successor.right
            successor.right = remove_node.right
        successor.left = remove_node.left
        # Case 2
        if not remove_parent:
            self._root = successor
        # Case 3
        elif remove_parent.left == remove_node:
            remove_parent.left = successor
        # Case 4
        else:
            remove_parent.right = successor

    def contains(self, value: object) -> bool:
        """
        RECEIVES: value to search
        RETURNS: True or False
        CONDITIONS: If the object does not exist return False else True.
        Search goes on until all nodes are visited or corresponding node to
        value is reached.
        VARIABLES: curr_node as the pointer for the search
        Confirms if a node with the target value exists in the tree
        """
        curr_node = self._root
        # check COND
        while curr_node:
            # exits while loop and returns true if value is found
            if value == curr_node.value:
                return True
            elif value < curr_node.value:
                curr_node = curr_node.left
            else:
                curr_node = curr_node.right
        # if every node is visited without finding the value return false
        return False

    def inorder_traversal(self) -> Queue:
        """
        RECEIVES: None
        RETURNS: A Queue object that contains the values of the inorder
        traversal
        CONDITIONS: if tree is empty return
        VARIABLES: inorder_queue object to return
        This function does an inorder_traversal of the tree and returns its
        path as a queue object.
        """
        def inorder_traverser(node):
            """
            RECEIVES: starting node = self._root
            helper function for recursive traversal of the tree
            """
            # COND
            if node is None:
                return
            # move down as leftward as possible and enqueue values
            inorder_traverser(node.left)
            inorder_queue.enqueue(node.value)
            # move right across the tree once leftmost value of a branch is
            # reached
            inorder_traverser(node.right)
        # create the queue call the helper and return resultant queue
        inorder_queue = Queue()
        inorder_traverser(self._root)
        return inorder_queue

    def find_min(self) -> object:
        """
        RETURNS: min node value
        CONDITIONS: Tree can't be empty. Traversal stops when leftmost node
        is reached.
        VARIABLES: current node as a pointer
        Visits the left most branches of the tree until a node/leaf
        without children is reached, returning its value
        """
        # start at root node
        cur_node = self._root
        if self._root is None:
            return None
        # traverse as leftward as possible
        while cur_node.left:
            cur_node = cur_node.left
        # return the most leftward (min) node's value
        return cur_node

    def find_max(self) -> object:
        """
        RETURNS: max node value
        CONDITIONS: Tree can't be empty. Traversal stops when rightmost node
        is reached.
        VARIABLES: current node as the pointer's position during traversal
        Visits the right most branch of the tree until node/leaf without
        children is reached, returning its value
        """
        cur_node = self._root
        if self._root is None:
            return None
        while cur_node.right:
            cur_node = cur_node.right
        return cur_node

    def is_empty(self) -> bool:
        """
        RETURNS: True or False
        checks if the root node is empty to confirm if the tree is empty or not
        """
        return self._root is None

    def make_empty(self) -> None:
        """
        Sets the root node to None to clear the tree
        """
        self._root = None


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
