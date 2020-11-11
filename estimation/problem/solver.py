"""
call MatLAB engine from Python to src MILP problem
"""
import os
import itertools
import time

import matlab.engine
import scipy.io


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


def solve_milp_problem(problem, eng, path='./estimation/matlab/matfiles/'):
    """
    call m-file with solver function of MIXED-INTEGER LINEAR PROGRAMMING PROBLEM
    :param problem: object og problem. It includes objective function,
    number of integer variables, inequality matrix, linear inequality constraint
    vector, equality matrix, linear equality constraint vector, lower bounds
    vector, upper bounds vector,
    :param eng: MatLab engine
    :param path: path to m.-files
    :return: solution of ILP problem
    """

    f = save_mfile(path, problem.get_f, name='f')
    intcon = save_mfile(path, problem.get_intcon, name='intcon')
    A = save_mfile(path, problem.get_ineq, name='A')
    b = save_mfile(path, problem.get_b, name='b')
    Aeq = save_mfile(path, problem.get_eq, name='Aeq')
    beq = save_mfile(path, problem.get_beq, name='beq')
    lb = save_mfile(path, problem.get_lb, name='lb')
    ub = save_mfile(path, problem.get_ub, name='ub')

    start_time = time.time()

    # eng = matlab.engine.start_matlab('-nojvm')
    # eng.cd(r'./estimation/matlab/', nargout=0)

    # print("--- MatLab Engine %s seconds ---" % (time.time() - start_time))

    [x, fval, exitflag, output] = eng.milp(f, intcon, A, b, Aeq, beq,
                                           lb, ub, nargout=4)
    if (exitflag == -2) or (fval == 0):
        move_bool = False
        estimate = 0
    else:
        move_bool = True
        # out_x = [round(i) for i in list(itertools.chain(*x))]
        estimate = -1 * fval
    return estimate, move_bool


def solve_lp_problem(f, A, b, Aeq, beq, lb, ub, option='optimization',
                     path='./estimation/matlab/matfiles/'):
    """
    call m-file with solver function with LINEAR PROGRAMMING PROBLEM
    :param path: it is path to save .m-file
    :param f: numpy array of objective function
    :param A: numpy array of inequality matrix
    :param b: numpy array of linear inequality constraint vector
    :param Aeq: numpy array of equality matrix
    :param beq: numpy array of linear equality constraint vector
    :param lb: numpy array of lower bounds vector
    :param ub: numpy array of upper bounds vector
    :param option: default - optimization problem (f->min) or feasible solution
    (f==0)
    :param path: path to m.-files
    :return: solution of LP problem
    """

    f = save_mfile(path, f, name='f')
    A = save_mfile(path, A, name='A')
    b = save_mfile(path, b, name='b')
    Aeq = save_mfile(path, Aeq, name='Aeq')
    beq = save_mfile(path, beq, name='beq')
    lb = save_mfile(path, lb, name='lb')
    ub = save_mfile(path, ub, name='ub')

    start_time = time.time()

    eng = matlab.engine.start_matlab('-nojvm')
    eng.cd(r'./estimation/matlab/', nargout=0)

    print("--- MatLab Engine %s seconds ---" % (time.time() - start_time))

    [x, fval, exitflag, output] = eng.lp(f, A, b, Aeq, beq,
                                         lb, ub, nargout=4)

    out_x = [round(i) for i in list(itertools.chain(*x))]

    return (fval, out_x)
