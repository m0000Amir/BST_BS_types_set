# This module uses Gurobi optimizer https://www.gurobi.com/
# It consists Integer Linear Programming solution or Knapsack problem solution
from typing import Union

import gurobipy as gp
from gurobipy import GRB
import numpy as np
from .ilp import ILP
from .knapsack import KnapsackProblem


def solve(problem: Union[ILP, KnapsackProblem]):
    """
    MIP rproblem solver
    Parameters
    ----------
    problem - prepared input variable of MIP problem

    Returns
    -------
        Objective value

    """
    """ Optimal problem """
    # Create a new model
    with gp.Env(empty=True) as env:
        env.setParam('OutputFlag', 0)
        env.start()
        m = gp.Model("Estimation of right noncoverage", env=env)
        m.Params.LogToConsole = 0
    try:
        _length = len(problem.get_f)

        x = m.addMVar(shape=(_length,),
                      lb=problem.get_lb[0],
                      ub=problem.get_ub[0],
                      vtype=GRB.BINARY)
        # Set objective
        obj = problem.get_f

        m.setObjective(obj @ x, GRB.MINIMIZE)

        if np.size(problem.get_ineq) != 0:
            m.addConstr(problem.get_ineq @ x <= problem.get_b,
                        name="inequality")
        if np.size(problem.get_eq) != 0:
            m.addConstr(problem.get_eq @ x == problem.get_beq,
                        name="equality")
        # Optimize model
        m.optimize()

    except gp.GurobiError as e:
        print(f'Error code :{e}')

    except AttributeError:
        print('Encountered an attribute error')

    return -1*m.objVal
