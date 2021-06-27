# Huffman Tree Visualization

### Prepare

Install [graphviz](https://graphviz.org/download/) on your OS


Install python wrap by graphviz
```bash
    pip install graphviz
```

Example
```bash
    python main.py -N 128 -p0 0.1 -p1 0.9 -fn <filename> 
```

```bash

    usage: main.py [-h] -N N -p0 PZ -p1 PO -fn FILENAME [-engine {neato,osage,patchwork,circo,twopi,fdp,sfdp,dot}]
    
    -N              Maximum number is a combination
    -p0             Probability of occurrence of zero
    -p1             Probability of occurrence of one
    -fn             Name of the output file
    -engine         Which engine will be used to render the tree    
    --file-format   Output file format
        
```


