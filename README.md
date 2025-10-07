# Query Processor Project 
## Summary
This project includes a volcano-style iterator model query processor written in python. This program processes JSON serialized queries from tables described in a `.csv` file format. This query processor is capable of Select, Project, Join, Scan, and Limit query operations. It is also capale of evaluating column references and aliases, constants, arithetic operations, comparison operations, and logical operations. The code takes a modular approach, where the join, limit, project, scan, and select, are all subclasses of a base operation superclass allowing for futher implementation of additional operations.

## Validation approach
To validate this model, I ran all of the example queries included within this project. The queries exercise multiple operators. I made sure that every operator was tested and utilized in at least one query. I statically verified the correctness of each query since the correct output for each query was short enough to be read by a human.

## How to run the system
- All queries (.json files) and tables (.csv files) can be found in data/
- There are two example folders (example1 and example2) which each contain different queries and table data

### Command Template
`python3 query_processor.py /path/to/query.json`

### Example Command
`python3 query_processor.py data/example2/query_open_order_line_totals.json`

## AI usage notice
- Since I had no idea where to start this project, I asked ChatGPT to generate a folder structure and some boilerplate code for this project. The ideas for the modular approach came from ChatGPT. I filled in the rest of the details.
