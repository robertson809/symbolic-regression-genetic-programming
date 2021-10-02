from collections import deque
from Node import *
from random import *
from readData import *
MUTATE_PROB = .05
SIZE_PENALTY_COEFF = .1
#next, we should add variables

class Tree:
    #change this based on research to not have all trees of the
    #same depth
    def __init__(self, size):
        self.root = Node('num', 1)
        self.size = 1
        self.depth = 1
        self.fitness = float('inf')

        #do a BFD to find a child without a node
        frontier = deque([self.root])
        #continue until we've reached the desired size
        while self.size < size:
            next_node = frontier.popleft()
            if next_node.left is None and next_node.right is None:
                next_node.add_children()
                self.size += 2
                #add the new children
                frontier.append(next_node.left)
                frontier.append(next_node.right)
                #update depth
                if next_node.left.depth > self.depth:
                    self.depth = next_node.left.depth
            else:
                frontier.append(next_node.left)
                frontier.append(next_node.right)

    #make the tree comparable, two trees are equal if they point to the same reference
    def __eq__(self, other):
        if self is other:
            return True
        else:
            return False

    #define equality as outputting the same number (assuming that if f(10) = g(10), then f = g
    def __lt__(self, other):
        if self.fitness < other.fitness:
            return True
        else:
            return False

    #returns a value from the tree given input x
    def evaluate (self,x):
        return self.evaluateTree(self.root, x)

    #helper function recursvely calculates the output of the expression tree
    #given input x
    #https://www.geeksforgeeks.org/evaluation-of-expression-tree/
    def evaluateTree(self,node, x):
        # empty tree
        if node is None:
            return 0
        #if divide by zero, return inf
        if node.value=='/' and node.right==0:
            print ("divided by zero")
            return float('inf')

        # leaf node
        if node.left is None and node.right is None:
            if node.value=='x':
                return float(x)
            else:
                return node.value

        # evaluate left tree
        left_sum = self.evaluateTree(node.left,x)

        # evaluate right tree
        right_sum = self.evaluateTree(node.right,x)
        if left_sum ==None or right_sum==None:
            return None

        # check which operation to apply
        if node.value == '+':
            return float(left_sum + right_sum)

        elif node.value == '-':
            return float(left_sum - right_sum)

        elif node.value == '*':
            return float(left_sum * right_sum)

        else:
            if right_sum!=0:
                return float(left_sum / right_sum)
            else:
                return float('inf')

    #returns the fitness of the tree, as an int
    #accounts for bloat by negatively weighting
    #size
    def calcFitness(self, data):
        #squared error
        sqrerr = 0
        #use each set of data points
        for row in range(len(data)):

            #what is this line? Why would the answer ever equal none?, why do we calculate this?
            ans = self.evaluate(data[row][0])
            if ans !=None:
                sqrerr += (ans-data[row][1])**2
        mse = sqrerr/len(data)
        rmse= mse**(.5)
        #Need to add size penalty
        rmse+=SIZE_PENALTY_COEFF*self.size
        self.fitness = mse
        return mse

    #mate two trees
    def crossover(self, other):
        #Choose randomly where to crossover
        selfPath = self.getRandomBitString(randint(1,self.depth))
        otherPath = other.getRandomBitString(randint(1,other.depth))


        #Find node on self
        root1 = self.root
        root_depth1 = 1
        for i in range(len(selfPath)):
            #if 0 try going left
            if selfPath[i] == '0' and root1.left:
                #save parent
                parent1=root1
                direct1='l'
                root1 = root1.left
                root_depth1+=1
            #if 1 try going right
            elif selfPath[i]=='1' and root1.right:
                #save parent
                parent1=root1
                direct1='r'
                root1 = root1.right
                root_depth1+=1


        #Find node on otherPath
        root2 = other.root
        root_depth2 = 1
        for i in range(len(otherPath)):
            #if 0 try going left
            if otherPath[i] == '0' and root2.left:
                #save parent
                parent2=root2
                direct2='l'
                root2 = root2.left
                root_depth2+=1
            #if 1 try going right
            elif otherPath[i]=='1' and root2.right:
                #save parent
                parent2=root2
                direct2='r'
                root2 = root2.right
                root_depth2+=1

        #Swap places
        if direct1=='l':
            parent1.left=root2
        elif direct1=='r':
            parent1.right=root2
        else:
            print ('Did not crossover parent1')

        if direct2=='l':
            parent2.left=root1
        elif direct2=='r':
            parent2.right=root1
        else:
            print ('Did not crossover parent2')


        #Update depth
        #root_length1=self.getRootLength(root1,-1)
        #root_length2=self.getRootLength(root2,-1)
        #print (root_length1)
        #print (root_length2)
        #Root level plus length
        #self.depth=self.updateDepth(self.root)
        other.depth=other.updateDepth(other.root)
        other.size=other.updateSize(other.root)

        #new_tree = Tree(5)
        return other


    # def getRootLength(self,root,root_length):
    #     print self.depth
    #     self.root.display()
    #     if root==None:
    #         return root_length
    #     return(max(self.getRootLength(root.left,root_length+1),
    #     self.getRootLength(root.right,root_length+1)))

    #recursive algorithm that returns the depth of a tree
    def updateDepth(self,root, depth=0):
        if root == None:
            return depth
        depth+=1
        return max(self.updateDepth(root.right, depth),
        self.updateDepth(root.left,depth))

    #recursive algorithm that updates the size of a tree
    def updateSize(self, root,size=0):
        if root==None:
            return size
        return self.updateSize(root.right,size)+self.updateSize(root.left,size)

    #change a tree, focus on changing the lower level
    def mutate(self,root):
        if random.random() <  MUTATE_PROB:
        #never mutate closer to root than 2 places from depth
            #never mutate the root
            lower = max(1,self.depth-2)
            path = self.getRandomBitString(randint(lower,self.depth+2))
            direct=''
            depth = 1
            for i in range(len(path)):
                #if 0 try going left
                if path[i] == '0' and root.left:
                    #save parent
                    parent=root
                    direct='l'
                    root = root.left
                    depth+=1

                #if 1 try going right
                elif path[i]=='1' and root.right:
                    #save parent
                    parent=root
                    direct='r'
                    root = root.right
                    depth+=1
            #Once we've found the node to mutate, mutate it
            new_node = Node(root.type,depth)
            new_node.right=root.right
            new_node.left=root.left
            print (new_node.value)
            if direct=='l':
                parent.left=new_node
            elif direct=='r':
                parent.right=new_node



    #Used to choose a random path down the tree
    def getRandomBitString(self,length):
        string=''
        for i in range(length):
            bit = randint(0,1)
            string+=str(bit)
        return string


##testing
Tree1 = Tree(3)
fitness = (Tree1.calcFitness(small_train1))