from .Code import Code
from .BinaryTree import BinaryTree
from .Node import Node

class Handlers:
    def __init__(self , max_code_length : int , config : dict ):
        self.max_code_length = max_code_length
        self.config = config

    def init_order(self , node : BinaryTree  , marker: str):
        mas = {}
        if node:
            mas[marker+ "l"] = self.init_order(node.left , marker + "l")
            mas[marker]  =  node.data.probability
            mas[marker+ "r"] = self.init_order(node.right , marker + 'r')
        return mas if mas != {} else None

    def init_order_with_marked_endpoint(self ,node : BinaryTree  , marker: str):
        mas = {}
        if node:
            mas[marker+ "l"] = self.init_order_with_marked_endpoint(node.left , marker + "l")
            if node.right == None and node.left == None:
                mas[marker+ "e"]  =  node.data.probability
            else:
                mas[marker]  =  node.data.probability
            mas[marker+ "r"] = self.init_order_with_marked_endpoint(node.right , marker + 'r')
        return mas if mas != {} else None


    def tree_to_node(self , tree : dict ):
        nodes = []
        for key , val in tree.items():
            if isinstance( val  , dict):
                nodes += self.tree_to_node( val )
            else:
                nodes.append( Node(key , val) )
        return nodes

    def get_formated_code(self ,num : int):
        code = bin(num).replace('0b', '').zfill(self.max_code_length)
        probability = round( pow( self.config.pz , code.count('0')  ) * pow( self.config.po , code.count('1') ) , 12)
        return Code( probability , code , False )

    def copy_obj( self , obj : list[Code] ):
        __tmp_arr = []
        for code in obj:
            __tmp_arr.append( Code( code.probability , code.code , False ) )
        return __tmp_arr

    def symbol_mark_to_bin(self , nodes : list[Node] ):
        bin_marked_nodes = list()
        for node in nodes:
            bin_marked_nodes.append(
                    node.marker.replace('p' , '').replace('l' , '0').replace('r' , '1'))
        return bin_marked_nodes