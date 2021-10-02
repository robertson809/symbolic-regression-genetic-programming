from random import *
OPERATORS = ['+', '-', '*', '/']


##static methods
def print_in_order(current_node):
    #if I have reached a leaf, return
    if current_node is None:
        return
    #print left
    print_in_order(current_node.left)
    print(current_node.value)
    print_in_order(current_node.right)
    return


class Node:
    #type zero is operator, type 1 is number (either coefficient or variable)
    value = 0
    type = None
    right = None
    left = None
    depth = 0

    #type 0 is operator, type 1 is coefficient/variable (number)
    def __init__(self, type, depth):
        self.type = type
        self.depth = depth
        if type == 'op':
            self.value = OPERATORS[randint(0, 3)]
        elif type == 'num':
            rand = randint(0,1)
            if rand == 0:
                self.value = randint(-5, 5)
            elif rand == 1:
                self.value = 'x'
        else:
            print('error, must be op or num')

    #changes the value of a node to a random operator
    def change_to_operator(self):
        self.type = 'op'
        self.value = OPERATORS[randint(0, 3)]

        #escape divide by zero error
        if self.value == '/' and self.right == 0:
            self.value = OPERATORS[randint(0, 2)]


    #takes node input which should be a number, changes it to an operator, and
    #gives it two number children
    def add_children(self):
            if self.left is None and self.right is None :
                self.change_to_operator()
                self.left = Node('num', self.depth + 1)
                self.right = Node('num', self.depth + 1)
                #we have added two children to the
                #shallowest node
                return
            else:
                raise Exception('error, to add children the node must have none')
                

    #scraped method to print the tree
    #https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python
    def display(self):
        lines, _, _, _ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.value
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.value
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.value
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.value
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


##Testing##
# Node1 = Node('num')
# Node1.add_children()
# print_in_order(Node1)
