# Optimal problem of stations placement
Optimal placement of Base Station of Wireless Broadband Network with 
linear topology. It is the proposed Branch and Bound method of solving the problem.

## Input data
Input data is JSON-file, which consists of optimal problem data and
configuration data. See instanse in `./input` folder.

### Configuration

```json
{
  "configuration": {
    "method": "bab",
    "estimation_method": "knapsack",
    "place_all_station": false,
    "drawing": false,
    "last_optimal_noncoverage": 0,
    "relative_deviation": null
  }
}  
```
It is consist:

- Flag `"method"` can be contain one of:
   1. `"bnb"` -- Branch and Bound;
   2. `"bf"` -- Brute Force.
- Flag `"estimation_method"` can be contain one of:
  1. `ILP` -- Integer Linear Problem;
  2. `Knapsack` -- Knapsack problem;
  3. `LP` -- Linear Problem.
- Flag `"place_all_station"` is `True` if it is necessary to place all given 
stations, `False` is otherwise.
- Flag `"drawing"` is `True` if it is necessary to obtain the figure of binary 
search tree.
- Flag `"last_optimal_noncoverage"` contains noncoverage of last optimal 
solution. This is necessary to get a set of feasible placements, each of 
which has noncoverage is no more than a given `"relative_deviation"` 
from obtained solution. 


## Run
`python3 problem.py`

### The estimation of the right noncoverage
To estimate the right noncoverage is used Gurobi Optimizer.
How to install package `gurobipy` see https://www.gurobi.com. 

### Solution
Obtained solution of optimal problem is `solution.json`.

## Publication
[A Problem of Optimal Location of Given Set of Base Stations in Wireless Networks with Linear Topology](https://link.springer.com/chapter/10.1007%2F978-3-030-36625-4_5)