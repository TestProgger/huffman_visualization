import os
from graphviz import Digraph , ENGINES , FORMATS
import argparse
from zipfile import ZipFile , ZIP_DEFLATED
from multiprocessing import Pool
##### My Libs ;)

from lib.BinaryTree import BinaryTree
from lib.Code import Code
from lib.Node import  Node
from lib.Handlers  import  Handlers
from lib.CsvWriter import CsvWriter


parser = argparse.ArgumentParser(description="huffman Tree")
parser.add_argument('-N' , dest='N' , required=True , type=int )
parser.add_argument('-p0' , dest='pz' , required=True, type=float)
parser.add_argument('-p1' , dest='po' , required=True , type=float)
parser.add_argument('-fn' , dest='filename' , required=True , type=str )
parser.add_argument('--no-csv' , dest='no_csv' , required=False  , default=False , action="store_true")
parser.add_argument('--no-tree' , dest='no_tree' , required=False , default=False , action="store_true")
parser.add_argument('-engine' ,dest='engine' , required=False , type=str , default='dot' ,choices=ENGINES)
parser.add_argument('--file-format' , dest='fileformat' , required=False , type=str , choices=FORMATS , default="jpeg")
parser.add_argument('--file-formats' , dest='fileformats' , required=False , type=str , default="jpeg")
parser.add_argument('--zip' , dest='zip' , required=False , action="store_true")
config = parser.parse_args()

max_code_length = len( bin( config.N - 1 ).replace('0b','') )


handlers = Handlers(max_code_length , config)


huffman_matrix = [sorted([ handlers.get_formated_code(i) for i in range(config.N) ])]
huffman_matrix[0].reverse()
__huffman_matrix = huffman_matrix[0]

while len( huffman_matrix[-1] ) > 1:
    __tmp_arr = handlers.copy_obj( huffman_matrix[-1] )

    huffman_matrix[-1][-1].set_bit(True)
    huffman_matrix[-1][-2].set_bit(False)

    __tmp_sum = round( __tmp_arr[-1].probability + __tmp_arr[-2].probability , 12)
    __tmp_code = __tmp_arr[-2].code.replace("|" , ";") + "|"+ __tmp_arr[-1].code.replace("|" , ";")
    huffman_matrix.append(__tmp_arr[:-1] )
    huffman_matrix[-1][-1] = Code( __tmp_sum , __tmp_code , False )
    huffman_matrix[-1].sort()
    huffman_matrix[-1].reverse()

huffman_matrix.reverse()

binTree = BinaryTree()
binTree.insert(huffman_matrix[0][0])
for code_vector in huffman_matrix:
    for code in code_vector:
        binTree.insert(code)

tree = handlers.init_order(binTree , 'p')
nodes = sorted(list( filter( lambda x : x.data ,  handlers.tree_to_node(tree)) ))


if not config.no_csv:
    binary_marked_nodes = sorted(list( filter( lambda x : x.data , handlers.tree_to_node( handlers.init_order_with_marked_endpoint(binTree , 'p') ))))
    binary_marked_nodes = list( filter( lambda node : node.marker.endswith('e') , binary_marked_nodes   ))
    binary_marked_nodes = list( map( lambda node: Node( node.marker.replace('e' , '') , node.data) , binary_marked_nodes ) )
    binary_marked_nodes = handlers.symbol_mark_to_bin(binary_marked_nodes)

    csv_writer = CsvWriter( config.filename)

    Ne_row = [ len(i) for i in binary_marked_nodes  ]
    pNe = [ Ne_row[ind]*__huffman_matrix[ind].probability  for ind , val in enumerate(Ne_row) ]


    csv_writer.prepare_data(
        __huffman_matrix,
        binary_marked_nodes,
        Ne_row,
        pNe
    )

    csv_writer.write()

def draw_tree(data:tuple[str, str, str]):
    filename : str  = data[0] + "_" + data[1]
    fileformat : str  = data[1]
    engine : str = data[2]
    graph = Digraph(filename , format=fileformat , encoding="utf-8" , strict=True , engine=engine)

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

    graph.unflatten(stagger=5).render(filename , cleanup=True , directory="./out")
    return os.path.join( './out'  , graph.name +"." + fileformat)


def main():
    fileformats = list(set(config.fileformats.split(',')))
    engine = config.engine
    filename = config.filename

    data_to_draw = [ ( filename , format , engine )  for format in fileformats ]

    with Pool(len(fileformats)) as pool:
        visualization_files = pool.map( draw_tree  , data_to_draw )
    
    if config.zip:
        with ZipFile(filename + ".zip"  , mode='w' , compression=ZIP_DEFLATED) as zp:
            for files in visualization_files:
                zp.write(files)
            zp.write( './out/' + filename+".csv" )
    

 
    



if __name__ == "__main__":
    if not config.no_tree:
        main()