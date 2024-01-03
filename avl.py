# Name: Vincewa Tran
# OSU Email: tranvinc@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment4
# Due Date: 11/21/23
# Description: This program represents a AVL data structure with an
# underlying binary search tree that it inherits data and methods from.
# some key methods are overwritten such as _remove_two_subtrees add and remove.
# The program has methods to balance the tree using RR, LL, RL, LR rotations
# to keep the AVL tree an AVL tree.


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

# ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        RECEIVES: value to be added to the AVL tree
        RETURNS: None
        CONDITIONS: None
        VARIABLES: None
        Adds an AVLNode with passed in value to the AVL tree
        """
        if self._root is None:
            self._root = AVLNode(value)
            return
        self._add_recursive(self._root, value)
        self._rebalance(self._root)

    def _add_recursive(self, node: AVLNode, value: object) -> AVLNode:
        """
        A recursive helper method to add a new value to the AVL tree.
        It finds the appropriate position in the tree and adds the value.
        """
        if value == node.value:
            return node

        if value < node.value:
            if node.left is None:
                new_node = AVLNode(value)
                node.left = new_node
                new_node.parent = node
            else:
                node.left = self._add_recursive(node.left, value)

        if value > node.value:
            if node.right is None:
                new_node = AVLNode(value)
                node.right = new_node
                new_node.parent = node
            else:
                node.right = self._add_recursive(node.right, value)

        self._update_height(node)
        return self._rebalance(node)

    def remove(self, value: object) -> bool:
        """
        Removes the value from the AVL tree.
        Returns True if the value is removed, False otherwise.
        """
        node, node_parent = self._find_node_parent(value)

        if node is None:
            return False

        # p is our point of action or where we start rebalancing
        p = node_parent if node_parent else node

        # case 1, no children -> _remove_no_subtrees(pn, n)
        if not node.left and not node.right:
            self._remove_no_subtrees(node_parent, node)

        # case 3, two children -> _remove_two_subtrees(pn, n)
        elif node.left and node.right:
            successor_parent = self._remove_two_subtrees(node_parent, node)
            p = successor_parent if successor_parent else node

        # case 2, one child -> _remove_one_subtree(pn, n)
        else:
            self._remove_one_subtree(node_parent, node)
        # set p to correct parent of point of change

        while p:
            self._rebalance(p)
            p = p.parent

        return True

    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node:BSTNode) -> AVLNode:
        """
        <-[back to] remove
        RECEIVES: remove_parent, remove_node
        RETURNS: successor_parent
        CONDITIONS: remove_node has two children
        VARIABLES: successor_parent, successor
        Removes a node with two children
        Node with 2 children pre-removal:   Node with 2 children post-removal:
                5                                   6
               / \                                 / \
              4   6                               4   7
                 / \                                 / \
                7   8                               8   9
                 \
                  9
        """
        # find successor
        successor_parent = remove_node
        successor = remove_node.right

        # find the leftmost node in the right subtree
        while successor.left:
            successor_parent = successor
            successor = successor.left

        # replace the value of the node to be removed with the value of the successor
        remove_node.value = successor.value

        # remove the successor
        if successor_parent == remove_node:
            remove_node.right = successor.right
        else:
            successor_parent.left = successor.right

        # return the parent of the successor
        return successor_parent


    def _balance_factor(self, node: AVLNode) -> int:
        """
        Calculates the balance factor of a passed in AVLNode
        """
        left_height = node.left.height if node.left else -1
        right_height = node.right.height if node.right else -1
        return left_height-right_height

    def _get_height(self, node: AVLNode) -> int:
        """
        RECEIVES: node that needs height updated
        RETURNS: Height of the target node
        CONDITIONS:
        VARIABLES:
        Returns the current height of a specific node
        """
        self._update_height(node)
        return node.height

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        RECEIVES: node that the rotation is centered around
        RETURNS: The new root: AVLNode
        CONDITIONS:
        VARIABLES: child[node that moves upwards ie new root], node[node
        that moves downwards]
        Performs a left rotation centered around child and sends node
        downwards to balance the AVL tree

        Rotate left ex:      Post Rotation:
            5                   6
           / \                 / \
          4   6               5   7
             / \             / \
            7   8           4   8
             \
              9

        """
        child = node.right
        node.right = child.left

        if child.left:
            child.left.parent = node

        child.parent = node.parent

        # update the parent of node
        if not node.parent:
            self._root = child
        elif node.parent.left == node:
            node.parent.left = child
        else:
            node.parent.right = child

        child.left = node
        node.parent = child

        self._update_height(node)
        self._update_height(child)
        return child

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        RECEIVES: node that the rotation is centered around
        RETURNS: The new root: AVLNode
        VARIABLES: Child returned. this child can also be thought of as the
        pivot point of our rotation
        Right rotation to balance AVL tree.

        Rotate right ex:     Post Rotation:
            5                   4
           / \                 / \
          4   6               2   5
         / \                     / \
        2   3                   3   6
        """
        child = node.left
        node.left = child.right

        if child.right:
            child.right.parent = node

        child.parent = node.parent

        # update the parent of node
        if not node.parent:
            self._root = child
        elif node.parent.left == node:
            node.parent.left = child
        else:
            node.parent.right = child

        child.right = node
        node.parent = child

        self._update_height(node)
        self._update_height(child)
        return child

    def _update_height(self, node: AVLNode) -> None:
        """
        RECEIVES: node that needs height updated
        RETURNS: None
        Updates the height of a specific node
        """
        left_height = node.left.height if node.left else -1
        right_height = node.right.height if node.right else -1
        node.height = 1+max(left_height, right_height)

    def _rebalance(self, node: AVLNode) -> AVLNode:
        """
        Method that rebalances the AVL tree after an add or removal of a node
        Rotation cases:
        RR:                     LL:                    RL:                   LR:
            5                   5                       5                     5
             \                  \                     /                      /
              6                 7                   4                       3
               \                \                 /                       / \
                7               8               3                       2   4
        """

        # update height of current node
        self._update_height(node)

        # check the balance factor
        balance_factor = self._balance_factor(node)

        # R-heavy
        if balance_factor < -1:
            # R-R case
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            # R-L case
            return self._rotate_left(node)

        # L-Heavy
        if balance_factor > 1:
            # L-L Case
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        return node


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
