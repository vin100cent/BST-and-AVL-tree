# AVL and Binary Search Tree Data Structure Implementations

This was in exercise to learn and implement a self-balancing tree. Here it's an AVL tree that builds on a binary search tree. The queue_and_stack.py provides both programs with queue/stack properties and behaviors. 

## avl.py
Uses an underlying binary search tree. It inherits the data and methods from bst.py. Some methods are overwritten such as _remove_two_subtrees add and remove. The program has methods to balance the tree using RR, LL, RL, LR rotations to keep the AVL tree an AVL tree.

**AVLNode** is essentially BSTNode

## bst.py
Implementation of a BST ADT 

**BSTNode Class::** represents a node along the BST and contains the value at a node as well as its left and right pointers–or children.

**BST Class** represents the tree itself with an initialized root node at None.

#### Methods
contains() - a find method that confirms if a value with that node exists
inorder_traversal() - a method that returns the path, as a queue object, for
the inorder traversal
find_min(), find_max() - methods that return the value of the nodes with
the smallest and largest values
is_empty() - which returns True if the tree is empty and False otherwise
make_empty() - that clears the tree completely
remove() is the largest method of this program when accounting for its
helpers and sub methods
_find_node_parent() - HELPER that finds the node to remove and its parent
using a value passed in by the user
_remove_no_subtrees() - removal case for no left or right children
_remove_one_subtree() - removal case for left XOR right children
_remove_two_subtrees() - removal case for a node with both left and right
children. This is the most complicated case where the method swaps the node
to be removed with its inorder successor updates values and deletes the
node to be deleted