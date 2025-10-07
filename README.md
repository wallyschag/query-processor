# Query Processor Project 
## Summary
This project includes a volcano-style iterator model query processor written in python. This program processes JSON serialized queries from tables described in a `.csv` file format. This query processor is capable of Select, Project, Join, Scan, and Limit query operations. It is also capable of evaluating column references and aliases, constants, arithmetic operations, comparison operations, and logical operations. The code takes a modular approach, where the join, limit, project, scan, and select, are all subclasses of a base operation superclass allowing for further implementation of additional operations.

## Validation approach
To validate this model, I ran all of the example queries included within this project. The queries exercise multiple operators. I made sure that every operator was tested and utilized in at least one query. I statically verified the correctness of each query since the correct output for each query was short enough to be read by a human.

## Additional Optimization Features
### Join Algorithms
#### Hash Join
Builds a hash table from the right input based on a join key, then iterates over rows from the left input to find matching rows efficiently. The operator combines matching records from both sides into a single result and returns them one by one.

#### Sort-Merge Join
Loads and sorts both input tables by their join keys, then sequentially scans through them to find and combine matching rows

### Predicate Pushdown
Traverses the query plan tree and moves filter conditions (Select operators) as close as possible to the data sources (Scan operators)

## How to run the system
- All queries (.json files) and tables (.csv files) can be found in data/
- There are two example folders (example1 and example2) which each contain different queries and table data

### Command Template
`CENGINE_OPTIMIZE=[true/false] CENGINE_JOIN_ALGO=[nested_loop/hash/sort_merge] python3 query_processor.py /path/to/query.json`

### Example Command
`CENGINE_OPTIMIZE=true CENGINE_JOIN_ALGO=hash python3 query_processor.py data/example2/query_open_order_line_totals.json`

## AI usage notice
- Since I had no idea where to start this project, I asked ChatGPT to generate a folder structure and some boilerplate code for this project. The ideas for the modular approach came from ChatGPT. I filled in the rest of the details.
