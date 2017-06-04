from rbtree import *

class Data(RBNode):
    def __init__(self, x):
        super().__init__(self, None, None, RBNode.Red)
        self.x = x

    def printTree(self, layer = 0):
        if(self.rightNode is not None):
            self.rightNode.printTree(layer + 1)
        print("%s%d(%s)" % ("    " * layer, self.x, self.color[0]))
        if(self.leftNode is not None):
            self.leftNode.printTree(layer + 1)

    def verify(self, layer = 0, lastColor = None, blackCountList = []):
        node = self
        if(self.parent is None):
            blackCountList = []
        assert(not (lastColor is RBNode.Red and self.color is RBNode.Red))
        if(node.leftNode is not None):
            assert(node.leftNode.x < node.x)
            assert(node.leftNode.parent is self)
            node.leftNode.verify(layer + 1, self.color, blackCountList)
        if(node.rightNode is not None):
            assert(node.rightNode.x > node.x)
            assert(node.rightNode.parent is self)
            node.rightNode.verify(layer + 1, self.color, blackCountList)

        if(self.leftNode is None and self.rightNode is None):
            nBlack = 0
            node = self
            while(node is not None):
                if(node.color is RBNode.Black):
                    nBlack += 1
                node = node.parent
            blackCountList.append(nBlack)

        if(self.parent is None):
            nBlack = blackCountList[0]
            for x in blackCountList:
                assert(x == nBlack)

def insert(tree, data):
    if(tree.root is None):
        data.parent = None
        tree.root = data
    else:
        parent = None
        node = tree.root
        while(node is not None):
            if(data.x < node.x):
                if(node.leftNode is None):
                    node.leftNode = data
                    data.parent = node
                    break
                parent = node
                node = node.leftNode
            elif(data.x > node.x):
                if(node.rightNode is None):
                    node.rightNode = data
                    data.parent = node
                    break
                parent = node
                node = node.rightNode
            else:
                raise KeyError("Key conflict")
    tree.insertColor(data)

def erase(tree, data):
    tree.erase(data)
    data.markAsIsolated()

dataList = [13, 17, 8, 1, 11, 15, 25, 27, 22, 6, 0, 256, 254, 18, 3]
tree = RBTreeCore()
deleteList = [11, 256, 13, 25, 18, 17]
for x in dataList:
    data = Data(x)
    if(x in deleteList):
        deleteList[deleteList.index(x)] = data
    insert(tree, data)
tree.root.verify()
for x in deleteList:
    erase(tree, x)
tree.root.printTree()
tree.root.verify()
