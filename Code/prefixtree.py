#!python3
from collections import deque

from prefixtreenode import PrefixTreeNode


class PrefixTree:
    """PrefixTree: A multi-way prefix tree that stores strings with efficient
    methods to insert a string into the tree, check if it contains a matching
    string, and retrieve all strings that start with a given prefix string.
    Time complexity of these methods depends only on the number of strings
    retrieved and their maximum length (size and height of subtree searched),
    but is independent of the number of strings stored in the prefix tree, as
    its height depends only on the length of the longest string stored in it.
    This makes a prefix tree effective for spell-checking and autocompletion.
    Each string is stored as a sequence of characters along a path from the
    tree's root node to a terminal node that marks the end of the string."""

    # Constant for the start character stored in the prefix tree's root node
    START_CHARACTER = '^'
    END_CHARACTER = '$'

    def __init__(self, strings=None):
        """Initialize this prefix tree and insert the given strings, if any."""
        # Create a new root node with the start character
        self.root = PrefixTreeNode(PrefixTree.START_CHARACTER)
        # Count the number of strings inserted into the tree
        self.size = 0
        # Insert terminal character
        self.insert('')
        self.size -= 1
        # Insert each string, if any were given
        if strings is not None:
            for string in strings:
                self.insert(string)

    def __repr__(self):
        """Return a string representation of this prefix tree."""
        return f'PrefixTree({self.strings()!r})'

    def is_empty(self):
        """Return True if this prefix tree is empty (contains no strings).
        Time: Θ(1) | Space: Θ(1)
        """
        return self.root.num_children() == 1

    def contains(self, string):
        """Return True if this prefix tree contains the given string.
        Time: O(kn) n = # of strings (width of tree), k = len(string)
        Space: Θ(1)
        """
        cur_node = self.root

        for char in string+'$':
            try:
                cur_node = cur_node.get_child(char) # Update cur_node
            except ValueError:
                ## char wasn't found, so the exact string doesn't exist
                return False
        return True


    def insert(self, string):
        """Insert the given string into this prefix tree.
        Time: O(kn) n = # of strings (width of tree), k = len(string)
        Space: Θ(1)
        """

        cur_node = self.root

        for char in string:
            try:
                ## Try to update cur_node with existing child for char
                cur_node = cur_node.get_child(char)
            except ValueError:
                ## Child for char doesn't exist, so add new child then update
                ## cur_child
                new_node = PrefixTreeNode(char)
                cur_node.add_child(char, new_node)
                cur_node = new_node

        try:
            ## Check if terminate character exists
            cur_node.get_child('$')
        except ValueError:
            ## Terminate character ($) wasn't found, so this must be a new
            ## string
            cur_node.add_child('$', PrefixTreeNode('$')) # Terminal node
            self.size += 1 # Increment because a new string has been inserted


    def _find_node(self, string):
        """Return a pair containing the deepest node in this prefix tree that
        matches the longest prefix of the given string and the node's depth.
        The depth returned is equal to the number of prefix characters matched.
        Search is done iteratively with a loop starting from the root node.
        Time: O(kn) n = # of strings (width of tree), k = len(string)
        Space: Θ(1)
        """
        # Start with the root node
        node = self.root
        depth = 0

        for char in string:
            try:
                node = node.get_child(char) # Update node with child
                depth += 1
            except ValueError:
                ## Child node wasn't found. End of prefix has been reached
                break
        return node, depth


    def complete(self, prefix):
        """Return a list of all strings stored in this prefix tree that start
        with the given prefix string.
        Time: O(n) | Space: O(n)"""
        # Create a list of completions in prefix tree
        completions = []
        ## BFS Search for all completions (maintain relative order of nodes)
        node, depth = self._find_node(prefix)

        if depth < len(prefix):
            return []
        q = deque([(prefix, node)])

        while len(q):
            cur_string, node = q.pop()

            for child in node.children:

                if child.character == '$':
                    ## End of string found
                    completions.append(cur_string)
                else:
                    q.appendleft((cur_string+child.character, child))
        return completions

    def strings(self):
        """Return a list of all strings stored in this prefix tree.
        Time: Θ(n) | Space: O(n)"""
        # Create a list of all strings in prefix tree
        all_strings = []
        q = deque([('', self.root)])

        while len(q):
            cur_string, node = q.pop()

            for child in node.children:
                if cur_string != '' and child.character == '$':
                    all_strings.append(cur_string)
                else:
                    q.appendleft((cur_string+child.character, child))
        return all_strings

    def _traverse(self, node, prefix, visit):
        """Traverse this prefix tree with recursive depth-first traversal.
        Start at the given node with the given prefix representing its path in
        this prefix tree and visit each node with the given visit function.
        Time: Θ(n) | Space: O(lg n)"""

        if child:
            for child in node.children:
                visit(child)
                self._traverse(child, prefix+child.character, visit)


def create_prefix_tree(strings):
    print(f'strings: {strings}')

    tree = PrefixTree()
    print(f'\ntree: {tree}')
    print(f'root: {tree.root}')
    print(f'strings: {tree.strings()}')

    print('\nInserting strings:')
    for string in strings:
        tree.insert(string)
        print(f'insert({string!r}), size: {tree.size}')

    print(f'\ntree: {tree}')
    print(f'root: {tree.root}')

    print('\nSearching for strings in tree:')
    for string in sorted(set(strings)):
        result = tree.contains(string)
        print(f'contains({string!r}): {result}')

    print('\nSearching for strings not in tree:')
    prefixes = sorted(set(string[:len(string)//2] for string in strings))
    for prefix in prefixes:
        if len(prefix) == 0 or prefix in strings:
            continue
        result = tree.contains(prefix)
        print(f'contains({prefix!r}): {result}')

    print('\nCompleting prefixes in tree:')
    for prefix in prefixes:
        completions = tree.complete(prefix)
        print(f'complete({prefix!r}): {completions}')

    print('\nRetrieving all strings:')
    retrieved_strings = tree.strings()
    print(f'strings: {retrieved_strings}')
    matches = set(retrieved_strings) == set(strings)
    print(f'matches? {matches}')


if __name__ == '__main__':
    # Create a dictionary of tongue-twisters with similar words to test with
    tongue_twisters = {
        'Seashells': 'Shelly sells seashells by the sea shore'.split(),
        # 'Peppers': 'Peter Piper picked a peck of pickled peppers'.split(),
        # 'Woodchuck': ('How much wood would a wood chuck chuck'
        #                ' if a wood chuck could chuck wood').split()
    }
    # Create a prefix tree with the similar words in each tongue-twister
    for name, strings in tongue_twisters.items():
        print('\n' + '='*80 + '\n')
        print(f'{name} tongue-twister:')
        create_prefix_tree(strings)
