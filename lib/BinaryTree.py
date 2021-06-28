from .Code import Code

class BinaryTree:
    def __init__(self , data : Code = None , marker : str = 'p' ):
        self.data = data
        self.right : BinaryTree = None
        self.left : BinaryTree = None
        self.marker = marker

    def insert(self , data : Code  , marker : str  = 'p'):
        if self.data == None:
            self.data = data
        if self.data.code == data.code:
            return

        if self.data.code.find("|") +1:
            __left = self.data.code.split("|")[1]
            __right = self.data.code.split("|")[0]

            if  __left.find( data.code.replace("|", ";") ) + 1:
                if self.left == None:
                    self.left = BinaryTree(data, marker+'l')
                else:
                    self.left.insert(data)

            if  __right.find( data.code.replace("|", ";") ) + 1:
                if self.right == None:
                    self.right = BinaryTree(data, marker+'r')
                else:
                    self.right.insert(data)

    def __repr__(self):
        return f"Node ( prb: {self.data.probability}  mark : {self.marker}  )"

    def __str__(self):
        return f"Node ( prb: {self.data.probability}  mark : {self.marker} )"
