"""
call MatLAB engine from Python to src MILP problem
"""
import os
import time

import scipy.io
from scipy.optimize import linprog
import numpy as np
import matlab.engine


def save_mfile(path, array, name):
    """
    save numpy array as mat-file for milp.m
    :param path: it is path to save .m-file
    :param array: numpy array which be saved
    :param name: name of .mat-array
    :return: .mat-file
    """
    scipy.io.savemat(path + name + '.mat', {str(name): array})
    return os.path.abspath(path + name + '.mat')


def solve_ilp_problem(problem, eng,
                      path='./branch_and_bound/estimation/matlab/matfiles/'):
    """
    call m-file with solver function of MIXED-INTEGER LINEAR PROGRAMMING PROBLEM
    :param problem: object of problem. It includes objective function,
    number of integer variables, inequality matrix, linear inequality constraint
    vector, equality matrix, linear equality constraint vector, lower bounds
    vector, upper bounds vector,
    :param eng: MatLab engine
    :param path: path to m.-files
    :return: problem of ILP problem
    """

    f = save_mfile(path, problem.get_f, name='f')
    intcon = save_mfile(path, problem.get_intcon, name='intcon')
    A = save_mfile(path, problem.get_ineq, name='A')
    b = save_mfile(path, problem.get_b, name='b')
    Aeq = save_mfile(path, problem.get_eq, name='Aeq')
    beq = save_mfile(path, problem.get_beq, name='beq')
    lb = save_mfile(path, problem.get_lb, name='lb')
    ub = save_mfile(path, problem.get_ub, name='ub')

    [x, fval, exitflag, output] = eng.milp(f, intcon, A, b, Aeq, beq,
                                           lb, ub, nargout=4)
    if (exitflag == -2) or (fval == 0):
        estimate = 0
    else:
        estimate = -1 * fval
    return estimate


def solve_lp_problem(problem):
    """
    Simplex Method problem of Linear Programming problem
    :param problem: object of problem. It includes objective function,
    inequality matrix, linear inequality constraint vector, lower bounds
    vector, upper bounds vector, and etc.
    :return: result
    """
    obj_func = problem.get_f
    ineq_array = problem.get_ineq
    ineq_b = problem.get_b
    lb = problem.get_lb
    ub = problem.get_ub

    # start_time = time.time()

    b_array = np.vstack([lb, ub])
    minmax_bounds = tuple((b_array[0, i], b_array[1, i])
                          for i in range(len(b_array[0])))

    start_time = time.time()
    res = linprog(obj_func, A_ub=ineq_array, b_ub=ineq_b, bounds=minmax_bounds,
                  method='simplex', callback=None,
                  options={'disp': False})

    estimate = -1 * res.fun

    return estimate
