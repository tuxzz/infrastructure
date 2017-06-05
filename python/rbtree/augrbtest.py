from rbtree import *
import bisect

def compute(node):
    v = node._maxEnd()
    node.maxEnd = v
    if(node.leftNode is not None and node.leftNode.augmented > v):
        v = node.leftNode.augmented
    if(node.rightNode is not None and node.rightNode.augmented > v):
        v = node.rightNode.augmented
    return v

class Interval:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    def __str__(self):
        return str((self.begin, self.end))

    def isOverlapped(self, b):
        return b.begin < self.end and b.end > self.begin

class NumberNode(RBNode):
    def __init__(self, x):
        super().__init__(self, None, None, RBNode.Red)
        self.x = x

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

class IntervalNode(RBNode):
    def __init__(self, x):
        super().__init__(self, None, None, RBNode.Red)
        self.x = x
        self.s = RBTreeCore()
        self.propagate, self.copy, self.rotate = augmentCallbacks(compute)

    def _maxEnd(self):
        node = self.s.root
        if(node is None):
            raise ValueError("No node")
        while(node.rightNode is not None):
            node = node.rightNode
        return node.x

    def _insertX(self, v):
        tree = self.s
        data = NumberNode(v)
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

    def _searchX(self, v):
        tree = self.s
        node = tree.root
        if(node is None):
            raise KeyError("No such key")
        while(node is not None):
            if(v < node.x):
                node = node.leftNode
            elif(v > node.x):
                node = node.rightNode
            else:
                return node
        raise KeyError("No such key")

    def _eraseX(self, n):
        tree = self.s
        tree.erase(n)
        n.markAsIsolated()

    def printTree(self, layer = 0):
        if(self.rightNode is not None):
            self.rightNode.printTree(layer + 1)
        childList = []
        node = self.s.firstPostOrderNode()
        while(node is not None):
            childList.append(node.x)
            node = node.nextPostOrderNode()
        print("%s%d(%s,%s,%s)" % ("    " * layer, self.x, self.color[0], str(self.augmented), str(childList)))
        if(self.leftNode is not None):
            self.leftNode.printTree(layer + 1)

    def verify(self, layer = 0, lastColor = None, blackCountList = []):
        self.s.root.verify()
        node = self
        if(self.parent is None):
            blackCountList = []
        else:
            assert(self is self.parent.leftNode or self is self.parent.rightNode)
        assert(not (lastColor is RBNode.Red and self.color is RBNode.Red))
        if(node.leftNode is not None):
            assert(node.leftNode.x < node.x)
            assert(node.leftNode.parent is self)
            node.leftNode.verify(layer + 1, self.color, blackCountList)
        if(node.rightNode is not None):
            assert(node.rightNode.x > node.x)
            assert(node.rightNode.parent is self)
            node.rightNode.verify(layer + 1, self.color, blackCountList)
        # verify augment
        assert(self.augmented == compute(self))

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
        new = IntervalNode(data.begin)
        new._insertX(data.end)
        new.parent = None
        tree.root = new
        new.propagate(new, None)
    else:
        parent = None
        node = tree.root
        while(node is not None):
            if(data.begin < node.x):
                if(node.leftNode is None):
                    new = IntervalNode(data.begin)
                    new._insertX(data.end)
                    node.leftNode = new
                    new.parent = node
                    new.propagate(new, None)
                    break
                parent = node
                node = node.leftNode
            elif(data.begin > node.x):
                if(node.rightNode is None):
                    new = IntervalNode(data.begin)
                    new._insertX(data.end)
                    node.rightNode = new
                    new.parent = node
                    new.propagate(new, None)
                    break
                parent = node
                node = node.rightNode
            else:
                node._insertX(data.end)
                node.propagate(node, None)
                return
    tree.insertColor(new, new.rotate)

def search(tree, data):
    node = tree.root
    if(node is None):
        raise KeyError("No such key")
    while(node is not None):
        if(data.begin < node.x):
            node = node.leftNode
        elif(data.begin > node.x):
            node = node.rightNode
        else:
            subNode = node._searchX(data.end)
            return node, subNode
    raise KeyError("No such key")

def erase(tree, node, subNode):
    node._eraseX(subNode)
    if(node.s.root is None):
        tree.erase(node, node.propagate, node.copy, node.rotate)
        node.markAsIsolated()
    else:
        node.propagate(node, None)

def searchSubtree(node, iv):
    l = []
    subNode = node.s.firstPostOrderNode()
    while(subNode is not None):
        if(iv.begin < subNode.x):
            l.append((node, subNode))
        subNode = subNode.nextPostOrderNode()
    return l

def searchOverlapped(node, iv):
    l = []
    if(iv.end > node.x and iv.begin < node.maxEnd):
        l += searchSubtree(node, iv)
    if(node.leftNode is not None and iv.begin < node.leftNode.augmented):
        l += searchOverlapped(node.leftNode, iv)
    if(node.rightNode is not None):
        l += searchOverlapped(node.rightNode, iv)
    return l

def allOverlapped(tree, iv):
    node = tree.root
    if(node is None):
        return l
    return searchOverlapped(node, iv)

dataList = [
    Interval(10, 20),
    Interval(10, 50),
    Interval(30, 50),
    Interval(30, 40),
    Interval(30, 90),
    Interval(40, 90),
    Interval(0, 30),
    Interval(50, 128),
    Interval(40, 50),
    Interval(70, 80),
]

deleteList = [
     Interval(30, 40),
     Interval(30, 90),
     Interval(50, 128),
]

tree = RBTreeCore()
for iv in dataList:
    insert(tree, iv)
for iv in deleteList:
    node, subNode = search(tree, iv)
    assert(node.x == iv.begin)
    assert(subNode.x == iv.end)
    erase(tree, node, subNode)
tree.root.printTree()
tree.root.verify()

aoList = allOverlapped(tree, Interval(50, 90))
result = [(70, 80), (40, 90)]
for node, subNode in aoList:
    result.remove((node.x, subNode.x))
assert(len(result) == 0)

aoList = allOverlapped(tree, Interval(0, 15))
result = [(10, 20), (10, 50), (0, 30)]
for node, subNode in aoList:
    result.remove((node.x, subNode.x))
assert(len(result) == 0)

aoList = allOverlapped(tree, Interval(200, 300))
assert(len(aoList) == 0)
