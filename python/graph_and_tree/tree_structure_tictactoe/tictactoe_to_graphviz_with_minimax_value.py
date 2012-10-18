#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Jérémie DECOCK (http://www.jdhp.org)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os

# TODO:
# - separate State (Node), Transition (Node.getChildNodes() -> Tictactoe), Policy (Minimax)
#TODO: une fonction self.value() qui donne la valeure de l'arbre, quelque soit le joueur, que ce soit un noeud feuille ou non


# STATE + TRANSITION ##########################################################


class Node:
    """Node class.
    
    Build and keep the full tree in memory.
    
    self._state[0:9] is the board state (3x3 squares).
    Each square has value 0 (empty), -1 (filled by player -1) or 1 (filled by
    player 1).

    self._state[9] is the player (1 or -1) who will play in this state."""

    def __init__(self, state):
        self._state = tuple(state)

        # Make child nodes
        self._child_nodes = []
        if not self.isFinal()[0]:
            player_id = self._state[-1]

            # Get the list index of empty squares (that is to say self._state[index]==0)
            empty_indices = [index for index, state in enumerate(self._state[:-1]) if state==0]
            for index in empty_indices:
                child_node_value = list(self._state)  # *copy* the list
                child_node_value[index] = player_id
                child_node_value[-1] = player_id * -1
                
                self._child_nodes.append(Node(child_node_value))
        else:
            pass

    def isFinal(self):
        """Return true is this node is a leaf node and return the value of this node.

        Return 0 as value if the current state is a draw.
        Return -1 as value if player -1 win.
        Return 1 as value if player 1 win.
        Else return None as value."""

        is_final = False
        value = None

        state = self._state[0:9]

        # DRAW GAME ################### TODO: mettre ça dans une fonction à part
        
        # Check if there is at least one empty square
        if state.count(0) == 0:
            is_final = True
            value = 0

        # TODO: it's useless to check if each player has won because the
        # current player is the only one who can win... (a win is a leaf node
        # and for each state, at most one player has won)

        # PLAYER 1 WINS ############### TODO: mettre ça dans une fonction à part

        # Check lines
        if sum(state[0:3])==3 or sum(state[3:6])==3 or sum(state[6:9])==3:
            is_final = True
            value = 1

        # Check columns
        elif sum(state[0:9:3])==3 or sum(state[1:9:3])==3 or sum(state[2:9:3])==3:
            is_final = True
            value = 1

        # Check diagonals
        elif sum(state[0:9:4])==3 or sum(state[2:7:2])==3:
            is_final = True
            value = 1

        # PLAYER -1 WINS ##############

        # Check lines
        elif sum(state[0:3])==-3 or sum(state[3:6])==-3 or sum(state[6:9])==-3:
            is_final = True
            value = -1

        # Check columns
        elif sum(state[0:9:3])==-3 or sum(state[1:9:3])==-3 or sum(state[2:9:3])==-3:
            is_final = True
            value = -1

        # Check diagonals
        elif sum(state[0:9:4])==-3 or sum(state[2:7:2])==-3:
            is_final = True
            value = -1

        return is_final, value

    def getState(self):
        return self._state

    def getChildNodes(self):
        return self._child_nodes


# POLICY ######################################################################


class Minimax:

    @staticmethod
    def minimax_decision(node):

        def value(node):
            value = None
            if node.getState()[9] == 1:
                value = Minimax.max_value(node)
            else:
                value = Minimax.min_value(node)
            return value

        #best_states = max([(child_node, value(child_node)) for child_node in node.getChildNodes()])

        child_nodes = node.getChildNodes()
        best_state, best_value = child_nodes[0], value(child_nodes[0])
        for child_node in child_nodes:
            if value(child_node) > best_value:          # TODO: > or < depends wether player 1 or -1 plays ! quoique... le role "max" tourne, le joueur courrant est toujours max si il utilise la politique minimax ?
                best_state, best_value = child_node, value(child_node)
        
        # TODO return action...

    @staticmethod
    def max_value(node):
        if node.isFinal()[0]:
            return node.isFinal()[1]
        v = -1   # -infinity
        for child_node in node.getChildNodes():
            v = max(v, Minimax.min_value(child_node))
        return v

    @staticmethod
    def min_value(node):
        if node.isFinal()[0]:
            return node.isFinal()[1]
        v = 1    # +infinity
        for child_node in node.getChildNodes():
            v = min(v, Minimax.max_value(child_node))
        return v


###############################################################################

# TODO faire generateur walk() et le réutiliser dans graphviz() et statistics() 

def game_tree_to_graphviz(node, max_depth, filename="tictactoe.dot"):
    """Make a Graphviz representation of the game tree."""

    dot_node_declaration = []
    dot_edge_declaration = []

    symbols = {-1: "x", 0: " ", 1: "o"}

    def walk(node, max_depth):
        """The tree traversal function"""

        # Do something with node value...
        str_val = [symbols[item] for item in node.getState()[0:9]]       # convert node.value (list of integers) to list of string (tictactoe symbols "x", " " and "o")
        color = "black"
        node_final_value = node.isFinal()[1]
        if node_final_value == 1:     # player "1" win
            color = "green"
        elif node_final_value == -1:  # player "-1" win
            color = "red"
        value = 0
        if node.getState()[9] == 1:
            value = Minimax.max_value(node)
        else:
            value = Minimax.min_value(node)
        #dot_node_declaration.append('\t%d [shape=record, color=%s, label="{%s}|{%s}|{%s}"];' % (id(node), color, "|".join(str_val[0:3]), "|".join(str_val[3:6]), "|".join(str_val[6:9])))
        dot_node_declaration.append('\t%d [shape=record, color=%s, label="%d|{%s}|{%s}|{%s}"];' % (id(node), color, value, "|".join(str_val[0:3]), "|".join(str_val[3:6]), "|".join(str_val[6:9])))

        if max_depth > 1:
            for child_node in node.getChildNodes():
                dot_edge_declaration.append('\t%d -> %d;' % (id(node), id(child_node)))

        # Recurse on each child node
        if max_depth > 1:
            for child_node in node.getChildNodes():
                walk(child_node, max_depth - 1)

    # Traverse the tree
    walk(node, max_depth)

    # Write the "dot" file (Graphviz)
    fd = open(filename, "w")
    print >> fd, "digraph G {"
    print >> fd, os.linesep.join(dot_node_declaration)
    print >> fd, os.linesep.join(dot_edge_declaration)
    print >> fd, "}"
    fd.close()

    # Print some statistics about the tree
    print "Graphviz:"
    print len(dot_node_declaration), "nodes generated"
    print len(dot_edge_declaration), "edges generated"
    print 


###############################################################################


def print_statistics(node):
    """ This function is used to check if the number of games (that is to say the
    number of leaf nodes) is correct.
    See http://en.wikipedia.org/wiki/Tic-tac-toe#Number_of_possible_games
        "How many Tic-Tac-Toe games are possible?" Henry Bottomley, 2001
        "Mathematical Recreations" Steve Schaeffer, 2002"""

    number_of_leaf_nodes = {-1:0, 0:0, 1:0}
    number_of_nodes = [0]                     # TODO: remove this ugly workaround

    def walk(node):
        """The tree traversal function"""

        number_of_nodes[0] += 1               # TODO: remove this ugly workaround

        is_final, value = node.isFinal()
        if is_final:
            if value == -1:
                number_of_leaf_nodes[-1] += 1
            elif value == 0:
                number_of_leaf_nodes[0] += 1
            elif value == 1:
                number_of_leaf_nodes[1] += 1
            else:
                print "Error: unknown value."

        # Recurse on each child node
        for child_node in node.getChildNodes():
            walk(child_node)

    walk(node)

    print "Statistics:"
    print number_of_nodes, "nodes in the tree"
    print number_of_leaf_nodes[-1] + number_of_leaf_nodes[0] + number_of_leaf_nodes[1], "possible games (number of leaf nodes)"
    print number_of_leaf_nodes[1], "finished games are won by player 1"
    print number_of_leaf_nodes[-1], "finished games are won by player -1"
    print number_of_leaf_nodes[0], "finished games are drawn"
            

###############################################################################


def main():
    """Main function

    Build the tic-tac-toe game tree and traverse it.
    """

    # Build the game tree
    #root = Node([0, 0, 1,  0, 0, -1,  1, -1, 0,  1])  # Start with a non-empty board
    root = Node([0, 0, 0,  0, 0, 0,  0, 0, 0,  1])

    # Traverse the tree
    game_tree_to_graphviz(root, 3)

    # Traverse the tree
    print_statistics(root)


if __name__ == '__main__':
    main()

