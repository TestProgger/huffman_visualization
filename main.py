from math import pow
from pprint import pprint
from sys import argv
from graphviz import Digraph , ENGINES , FORMATS
import argparse


##### My Libs ;)

from lib.BinaryTree import BinaryTree
from lib.Code import Code
from lib.Node import Node


parser = argparse.ArgumentParser(description="Haffman Tree")
parser.add_argument('-N' , dest='N' , required=True , type=int )
parser.add_argument('-p0' , dest='pz' , required=True, type=float)
parser.add_argument('-p1' , dest='po' , required=True , type=float)
parser.add_argument('-fn' , dest='filename' , required=True , type=str )
parser.add_argument('-engine' ,dest='engine' , required=False , type=str , default='dot' ,choices=ENGINES)
parser.add_argument('--file-format' , dest='fileformat' , required=False , type=str , choices=FORMATS)
config = parser.parse_args()

max_code_length = len( bin( config.N - 1 ).replace('0b','') )


def init_order(node : BinaryTree  , marker: str):
    mas = {}
    if node:
        mas[marker+ "l"] = init_order(node.left , marker + "l")
        mas[marker]  =  node.data.probability
        mas[marker+ "r"] = init_order(node.right , marker + 'r')
    return mas if mas != {} else None

def init_order_with_marked_endpoint(node : BinaryTree  , marker: str):
    mas = {}
    if node:
        mas[marker+ "l"] = init_order_with_marked_endpoint(node.left , marker + "l")
        if node.right == None and node.left == None:
            mas[marker+ "e"]  =  node.data.probability
        else:
            mas[marker]  =  node.data.probability
        mas[marker+ "r"] = init_order_with_marked_endpoint(node.right , marker + 'r')
    return mas if mas != {} else None


def tree_to_node( tree : dict ):
    nodes = []
    for key , val in tree.items():
        if isinstance( val  , dict):
            nodes += tree_to_node( val )
        else:
            nodes.append( Node(key , val) )
    return nodes

def get_formated_code(num : int):
    code = bin(num).replace('0b', '').zfill(max_code_length)
    probability = round( pow( config.pz , code.count('0')  ) * pow( config.po , code.count('1') ) , 12)
    return Code( probability , code , False )

def copy_obj( obj : list[Code] ):
    __tmp_arr = []
    for code in obj:
        __tmp_arr.append( Code( code.probability , code.code , False ) )
    return __tmp_arr

def symbol_mark_to_bin( nodes : list[Node] ):
    bin_marked_nodes = list()
    for node in nodes:
        bin_marked_nodes.append( 
                node.marker.replace('p' , '').replace('l' , '0').replace('r' , '1'))
    return bin_marked_nodes

haffman_matrix = [sorted([ get_formated_code(i) for i in range(config.N) ])]
haffman_matrix[0].reverse()


while len( haffman_matrix[-1] ) > 1:
    __tmp_arr = copy_obj( haffman_matrix[-1] )

    haffman_matrix[-1][-1].set_bit(True)
    haffman_matrix[-1][-2].set_bit(False)

    __tmp_sum = round( __tmp_arr[-1].probability + __tmp_arr[-2].probability , 12)
    __tmp_code = __tmp_arr[-2].code.replace("|" , ";") + "|"+ __tmp_arr[-1].code.replace("|" , ";")
    haffman_matrix.append(__tmp_arr[:-1] )
    haffman_matrix[-1][-1] = Code( __tmp_sum , __tmp_code , False )
    haffman_matrix[-1].sort()
    haffman_matrix[-1].reverse()

haffman_matrix.reverse()

binTree = BinaryTree()
binTree.insert(haffman_matrix[0][0])
for code_vector in haffman_matrix:
    for code in code_vector:
        binTree.insert(code)

tree = init_order(binTree , 'p') 
nodes = sorted(list( filter( lambda x : x.data ,  tree_to_node(tree)) ))


binary_marked_nodes = sorted(list( filter( lambda x : x.data , tree_to_node( init_order_with_marked_endpoint(binTree , 'p') ))))
binary_marked_nodes = list( filter( lambda node : node.marker.endswith('e') , binary_marked_nodes   )) 
binary_marked_nodes = list( map( lambda node: Node( node.marker.replace('e' , '') , node.data) , binary_marked_nodes ) )
binary_marked_nodes = symbol_mark_to_bin(binary_marked_nodes)
print("\n".join(binary_marked_nodes))



graph = Digraph('Hello' , format=config.fileformat , encoding="utf-8" , strict=True , engine=config.engine)

for node in nodes:
    marker_length = len(node.marker)
    childs = list( filter( lambda x : x.marker.startswith(node.marker) and (marker_length + 1) == len(x.marker) , nodes ) )

    graph.node( node.marker , str(round( node.data , 9)) )

    if len(childs) == 1:
        graph.edge(node.marker , childs[0].marker)
    if len(childs) == 2:
        __left = list( filter( lambda x: x.marker.endswith("l") , childs ) )[0]  
        __right = list( filter( lambda x: x.marker.endswith("r") , childs ) )[0] 

        graph.edge( node.marker , __left.marker )
        graph.edge( node.marker , __right.marker )

graph.unflatten(stagger=5).render(config.filename , cleanup=True , directory="./out")
