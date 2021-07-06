# Huffman Tree Visualization

### Prepare

Install [graphviz](https://graphviz.org/download/) on your OS


Install python wrap by graphviz
```bash
    pip install graphviz
```

### Usage

Example
```bash
    python main.py -N 128 -p0 0.1 -p1 0.9 -fn <filename> 
```

```bash
    -N              Maximum number is a combination
    -p0             Probability of occurrence of zero
    -p1             Probability of occurrence of one
    -fn             Name of the output file
    --engine        Which engine will be used to render the tree    
    --file-formats  Output file formats
    --zip           Archive output files

    --no-csv        Don't generate csv  
    --no-tree       Don't generate a tree image
        
```