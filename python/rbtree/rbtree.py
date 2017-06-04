def dummyAugment(a, b):
    pass

class RBNode:
    Red = "Red"
    Black = "Black"

    __slots__ = ("parent", "leftNode", "rightNode", "color")

    def __init__(self, parent, leftNode, rightNode, color):
        self.parent = parent
        self.leftNode = leftNode
        self.rightNode = rightNode
        self.color = color

    def isIsolated(self):
        return self.parent is self

    def markAsIsolated(self):
        self.parent = self
        self.color = self.Red

    def nextNode(self):
        node = self
        if(node.isIsolated()):
            return None

        if(node.rightNode is not None):
            node = node.rightNode
            while(node.leftNode is not None):
                node = node.leftNode
            return node

        parent = node.parent
        while(parent is not None and node is parent.rightNode):
            node = parent
            parent = node.parent
        return parent

    def prevNode(self):
        node = self
        if(node.isIsolated()):
            return None

        if(node.leftNode is not None):
            node = node.leftNode
            while(node.rightNode is not None):
                node = node.rightNode
            return node

        parent = node.parent
        while(parent is not None and node is parent.leftNode):
            node = parent
            parent = node.parent
        return parent

    def _leftDeepestNode(self):
        node = self
        while(True):
            while(node.leftNode is not None):
                node = node.leftNode
            if(node.rightNode is not None):
                node = node.rightNode
            else:
                return node

    def nextPostOrderNode(self):
        parent = self.parent
        if(parent is not None and self is parent.leftNode and parent.rightNode is not None):
            return parent.rightNode._leftDeepestNode()
        return parent

class RBTreeCore:
    __slots__ = ("root",)

    def __init__(self, root = None):
        self.root = root

    def isEmpty(self):
        return self.root is None

    def firstNode(self):
        node = self.root
        if(node is None):
            return None
        while(node.leftNode is not None):
            node = node.leftNode
        return node

    def lastNode(self):
        node = self.root
        if(node is None):
            return None
        while(node.rightNode is not None):
            node = node.rightNode
        return node

    def firstPostOrderNode(self):
        if(self.isEmpty()):
            return None
        return self.root._leftDeepestNode()

    def _changeChild(self, old, new, parent):
        if(parent is not None):
            if(parent.leftNode is old):
                parent.leftNode = new
            else:
                parent.rightNode = new
        else:
            self.root = new

    def _rotateAndSetParents(self, old, new, color):
        parent = old.parent
        new.parent, new.color = old.parent, old.color
        old.parent, old.color = new, color
        self._changeChild(old, new, parent)

    def insertColor(self, node, augmentRotate = dummyAugment):
        parent = node.parent
        while(True):
            if(parent is None):
                node.color = RBNode.Black
                break
            elif(parent.color is RBNode.Black):
                break

            gparent = parent.parent
            tmp = gparent.rightNode
            if(parent is not tmp): # parent is gparent.leftNode
                if(tmp is not None and tmp.color is RBNode.Red):
                    tmp.color = RBNode.Black
                    parent.color = RBNode.Black
                    node = gparent
                    parent = node.parent
                    node.color = RBNode.Red
                    continue
                tmp = parent.rightNode
                if(node is tmp):
                    tmp = node.leftNode
                    parent.rightNode = tmp
                    node.leftNode = parent
                    if(tmp is not None):
                        tmp.parent, tmp.color = parent, RBNode.Black
                    parent.parent, parent.color = node, RBNode.Red
                    augmentRotate(parent, node)
                    parent = node
                    tmp = node.rightNode
                gparent.leftNode = tmp
                parent.rightNode = gparent
                if(tmp is not None):
                    tmp.parent, tmp.color = gparent, RBNode.Black
                self._rotateAndSetParents(gparent, parent, RBNode.Red)
                augmentRotate(gparent, parent)
                break
            else: # parent is gparent.rightNode
                tmp = gparent.leftNode
                if(tmp is not None and tmp.color is RBNode.Red):
                    tmp.color = RBNode.Black
                    parent.color = RBNode.Black
                    node = gparent
                    parent = node.parent
                    node.color = RBNode.Red
                    continue
                tmp = parent.leftNode
                if(node is tmp):
                    tmp = node.rightNode
                    parent.leftNode = tmp
                    node.rightNode = parent
                    if(tmp is not None):
                        tmp.parent, tmp.color = parent, RBNode.Black
                    parent.parent, parent.color = node, RBNode.Red
                    augmentRotate(parent, node)
                    parent = node
                    tmp = node.leftNode
                gparent.rightNode = tmp
                parent.leftNode = gparent
                if(tmp is not None):
                    tmp.parent, tmp.color = gparent, RBNode.Black
                self._rotateAndSetParents(gparent, parent, RBNode.Red)
                augmentRotate(gparent, parent)
                break

    def _augmentedEraseHelper(self, node, augmentCopy, augmentPropagate):
        child = node.rightNode
        tmp = node.leftNode
        if(tmp is None):
            parent, color = node.parent, node.color
            self._changeChild(node, child, parent)
            if(child is not None):
                child.parent, child.color = parent, color
                rebalance = None
            else:
                rebalance = parent if(color is RBNode.Black) else None
            tmp = parent
        elif(child is None):
            parent, color = node.parent, node.color
            tmp.parent, tmp.color = parent, color
            self._changeChild(node, tmp, parent)
            rebalance = None
            tmp = parent
        else:
            successor = child
            tmp = child.leftNode
            if(tmp is None):
                parent = successor
                child2 = successor.rightNode
                augmentCopy(node, successor)
            else:
                while True:
                    parent = successor
                    successor = tmp
                    tmp = tmp.leftNode
                    if(tmp is None):
                        break
                child2 = successor.rightNode
                parent.leftNode = child2
                successor.rightNode = child
                child.parent = successor
                augmentCopy(node, successor)
                augmentPropagate(parent, successor)
            tmp = node.leftNode
            successor.leftNode = tmp
            tmp.parent = successor

            color = node.color
            tmp = node.parent
            self._changeChild(node, successor, tmp)
            if(child2 is not None):
                successor.parent, successor.color = tmp, color
                child2.parent, child2.color = parent, RBNode.Black
                rebalance = None
            else:
                color2 = successor.color
                successor.parent, successor.color = tmp, color
                rebalance = parent if(color2 is RBNode.Black) else None
            tmp = successor
        augmentPropagate(tmp, None)
        return rebalance

    def _eraseColorHelper(self, parent, augmentRotate):
        node = None
        while True:
            sibling = parent.rightNode
            if(node is not sibling): # node is parent.leftNode
                if(sibling.color is RBNode.Red):
                    tmp1 = sibling.leftNode
                    parent.rightNode = tmp1
                    sibling.leftNode = parent
                    tmp1.parent, tmp1.color = parent, RBNode.Black
                    self._rotateAndSetParents(parent, sibling, RBNode.Red)
                    augmentRotate(parent, sibling)
                    sibling = tmp1
                tmp1 = sibling.rightNode
                if(tmp1 is None or tmp1.color is RBNode.Black):
                    tmp2 = sibling.leftNode
                    if(tmp2 is None or tmp2.color is RBNode.Black):
                        sibling.parent, sibling.color = parent, RBNode.Red
                        if(parent.color is RBNode.Red):
                            parent.color = RBNode.Black
                        else:
                            node = parent
                            parent = node.parent
                            if(parent is not None):
                                continue
                        break
                    tmp1 = tmp2.rightNode
                    sibling.leftNode = tmp1
                    tmp2.rightNode = sibling
                    parent.rightNode = tmp2
                    if(tmp1 is not None):
                        tmp1.parent, tmp1.color = sibling, RBNode.Black
                    augmentRotate(sibling, tmp2)
                    tmp1, sibling = sibling, tmp2
                tmp2 = sibling.leftNode
                parent.rightNode = tmp2
                sibling.leftNode = parent
                tmp1.parent, tmp1.color = sibling, RBNode.Black
                if(tmp2 is not None):
                    tmp2.parent = parent
                self._rotateAndSetParents(parent, sibling, RBNode.Black)
                augmentRotate(parent, sibling)
                break
            else: # node is parent.rightNode
                sibling = parent.leftNode
                if(sibling.color is RBNode.Red):
                    tmp1 = sibling.rightNode
                    parent.leftNode = tmp1
                    sibling.rightNode = parent
                    tmp1.parent, tmp1.color = parent, RBNode.Black
                    self._rotateAndSetParents(parent, sibling, RBNode.Red)
                    augmentRotate(parent, sibling)
                    sibling = tmp1
                tmp1 = sibling.leftNode
                if(tmp1 is None or tmp1.color is RBNode.Black):
                    tmp2 = sibling.rightNode
                    if(tmp2 is None or tmp2.color is RBNode.Black):
                        sibling.parent, sibling.color = parent, RBNode.Red
                        if(parent.color is RBNode.Red):
                            parent.color = RBNode.Black
                        else:
                            node = parent
                            parent = node.parent
                            if(parent is not None):
                                continue
                        break
                    tmp1 = tmp2.leftNode
                    sibling.rightNode = tmp1
                    tmp2.leftNode = sibling
                    parent.leftNode = tmp2
                    if(tmp1 is not None):
                        tmp1.parent, tmp1.color = sibling, RBNode.Black
                    augmentRotate(sibling, tmp2)
                    tmp1, sibling = sibling, tmp2
                tmp2 = sibling.rightNode
                parent.leftNode = tmp2
                sibling.rightNode = parent
                tmp1.parent, tmp1.color = sibling, RBNode.Black
                if(tmp2 is not None):
                    tmp2.parent = parent
                self._rotateAndSetParents(parent, sibling, RBNode.Black)
                augmentRotate(parent, sibling)
                break

    def erase(self, node):
        rebalance = self._augmentedEraseHelper(node, dummyAugment, dummyAugment)
        if(rebalance is not None):
            self._eraseColorHelper(rebalance, dummyAugment)
