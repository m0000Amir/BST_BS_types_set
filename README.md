![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-%230C55A5.svg?style=for-the-badge&logo=scipy&logoColor=%white)
![C++](https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white)
[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)

<h1 align="center">Hi there, I'm <a href="https://www.researchgate.net/profile/Amir-Mukhtarov-2" 
target="_blank">Amir</a> 
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>
<h3 align="center">Computer science, communication system researcher</h3>

# Optimal problem of stations placement

Optimal placement of Base Station of Wireless Broadband Network with 
linear topology. It is the proposed Branch and Bound method of solving the problem.



![figure](bsoppy/drawing/bsp.png?raw=true "Title")

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

### The binary tree

To find optimal placement the algorithm used binary search tree.
![figure](bsoppy/drawing/tree_traversal.png?raw=true "Title")

### The estimation of the right noncoverage
To estimate the right noncoverage is used SciPy and Gurobi Optimizer.


<img src="https://scipy.github.io/devdocs/_static/logo.svg" alt="альтернативный текст" width="60" height="40">
<img src="https://cdn.gurobi.com/wp-content/uploads/2018/12/logo-final.png" alt="альтернативный текст" width="150" height="40">

How to install package `gurobipy` see https://www.gurobi.com.

### Solution
Obtained solution of optimal problem is `solution.json`.

## Publication 
[A Problem of Optimal Location of Given Set of Base Stations in Wireless Networks with Linear Topology](https://link.springer.com/chapter/10.1007%2F978-3-030-36625-4_5)
<img alt="img.png" height="15" src="https://link.springer.com/oscar-static/images/springerlink/svg/springerlink-6c9a864b59.svg" width="80"/>


