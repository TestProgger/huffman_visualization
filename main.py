from graphviz import Digraph , ENGINES , FORMATS
import argparse

##### My Libs ;)

from lib.BinaryTree import BinaryTree
from lib.Code import Code
from lib.Node import  Node
from lib.Handlers  import  Handlers
from lib.CsvWriter import CsvWriter


parser = argparse.ArgumentParser(description="Haffman Tree")
parser.add_argument('-N' , dest='N' , required=True , type=int )
parser.add_argument('-p0' , dest='pz' , required=True, type=float)
parser.add_argument('-p1' , dest='po' , required=True , type=float)
parser.add_argument('-fn' , dest='filename' , required=True , type=str )
parser.add_argument('-engine' ,dest='engine' , required=False , type=str , default='dot' ,choices=ENGINES)
parser.add_argument('--file-format' , dest='fileformat' , required=False , type=str , choices=FORMATS)
config = parser.parse_args()

max_code_length = len( bin( config.N - 1 ).replace('0b','') )


handlers = Handlers(max_code_length , config)


haffman_matrix = [sorted([ handlers.get_formated_code(i) for i in range(config.N) ])]
haffman_matrix[0].reverse()
__haffman_matrix = haffman_matrix[0]

while len( haffman_matrix[-1] ) > 1:
    __tmp_arr = handlers.copy_obj( haffman_matrix[-1] )

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

tree = handlers.init_order(binTree , 'p')
nodes = sorted(list( filter( lambda x : x.data ,  handlers.tree_to_node(tree)) ))

binary_marked_nodes = sorted(list( filter( lambda x : x.data , handlers.tree_to_node( handlers.init_order_with_marked_endpoint(binTree , 'p') ))))
binary_marked_nodes = list( filter( lambda node : node.marker.endswith('e') , binary_marked_nodes   ))
binary_marked_nodes = list( map( lambda node: Node( node.marker.replace('e' , '') , node.data) , binary_marked_nodes ) )
binary_marked_nodes = handlers.symbol_mark_to_bin(binary_marked_nodes)



csv_writer = CsvWriter( config.filename)

Ne_row = [ len(i) for i in binary_marked_nodes  ]


pNe = [ Ne_row[ind]*__haffman_matrix[ind].probability  for ind , val in enumerate(Ne_row) ]


csv_writer.prepare_data(
    __haffman_matrix,
    binary_marked_nodes,
    Ne_row,
    pNe
)

csv_writer.write()

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
