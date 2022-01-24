"""
Linear Problem Solution.  https://scipy.org.
Simplez method
"""
import time

from scipy.optimize import linprog
import numpy as np


def solve_problem(problem):
    """
    Simplex Method to solve Linear Programming problem
    Parameters
    ----------
    problem input data:
        - objective function;
        - inequality matrix;
        - constraint vector;
        - lower bounds.
    vector, upper bounds vector

    Returns
    -------
        Objective values
    """
    obj_func = problem.get_f
    ineq_array = problem.get_ineq
    ineq_b = problem.get_b
    lb = problem.get_lb
    ub = problem.get_ub

    b_array = np.vstack([lb, ub])
    minmax_bounds = tuple(
        (b_array[0, i], b_array[1, i])
        for i in range(len(b_array[0]))
    )

    res = linprog(obj_func, A_ub=ineq_array, b_ub=ineq_b, bounds=minmax_bounds,
                  method='simplex', callback=None, options={'disp': False})

    estimate = -1 * res.fun

    return estimate
