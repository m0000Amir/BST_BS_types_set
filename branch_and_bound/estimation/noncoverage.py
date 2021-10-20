from binary_search.tree import Node
from branch_and_bound.estimation.problem.ilp import ILP
from branch_and_bound.estimation.problem.knapsack import KnapsackProblem
from branch_and_bound.estimation.problem.solver import solve_ilp_problem
from branch_and_bound.estimation.problem.solver import solve_lp_problem
from network.performance_characteristics import noncoverage_between_station
from binary_search.schedule import Schedule
from network.connection_between_station import is_able_to_connect_gateways


from typing import Tuple, Any
from dataclasses import dataclass


import numpy as np
from matlab.engine import MatlabEngine
from termcolor import colored


def get_noncoverage_estimation(p: int,
                               s: int,
                               node: Node,
                               data: dataclass,
                               engine: MatlabEngine,
                               flag: str = 'ILP') -> Tuple[float, bool]:
    """
    Calculate estimates of noncoverage

    Parameters
    ----------
    p - index of placement
    s - index of station
    node - parent node
    data - input data
    engine - Matlab engine
    flag - kind of problem of right noncoverage estimation:
        - 'ILP' - integer linear programming model,
        - 'knapsack' - knapsack problem,
        - 'LP' - linear problem.

    Returns
    -------
        Noncoverage estimate
    """

    i, j = np.where(node.pi == 1)

    vacant_stations_coverage = [data.coverage[i]
                                for i in range(len(data.coverage))
                                if (i not in j) and (i != s)]
    vacant_stations_cost = [data.cost[i] for i in range(len(data.coverage))
                            if (i not in j) and (i != s)]

    vacant_placement_points = [data.placement_coordinate[j]
                               for j in range(len(data.placement_coordinate))
                               if (j not in i) and (j != p)]

    if len(vacant_stations_coverage) is 0 or len(vacant_placement_points) is 0:
        right_noncoverage_estimate = node.left_child.noncoverage.right
    else:
        remaining_cost = data.cost_limit - node.cost - data.cost[s]

        if flag == 'knapsack':
            problem = KnapsackProblem(vacant_stations_coverage,
                                      vacant_stations_cost,
                                      remaining_cost)
        # elif flag == 'ILP' or flag == 'LP':
        else:
            problem = ILP(vacant_stations_coverage,
                          vacant_stations_cost,
                          remaining_cost,
                          vacant_placement_points)

        if flag == 'knapsack' or flag == 'ILP':
            right_cov_estimate = solve_ilp_problem(problem, engine)
        # elif flag == 'LP':
        else:
            right_cov_estimate = solve_lp_problem(problem)

        right_noncoverage_estimate = noncoverage_between_station(
            data.placement_coordinate[p], data.gateway_coordinate[1],
            data.coverage[s], right_cov_estimate)

    novcov_estimate = (node.left_child.noncoverage.left +
                       right_noncoverage_estimate)

    return novcov_estimate


def better_than_record(node: Node,
                       data: dataclass,
                       statistics: Schedule) -> bool:
    """
    Checking obtained solution with having a record.

    Parameter data include a given deviation.
    If deviation is None than it is necessary to get optimal solution,
    else it is necessary to get optimal and feasible solutions.

    Parameters
    ----------
    node - current node
    data - input data
    statistics - record schedule

    Returns
    -------
        True or False

    """
    if data.deviation is None:
        "The method gives optimal solutions."
        if (node.left_child.noncoverage.estimate <
                statistics.record[-1]['optimal']):

            if is_able_to_connect_gateways(node.left_child,
                                           data.gateway_coordinate):
                node_noncoverage = (node.left_child.noncoverage.left +
                                    node.left_child.noncoverage.right)

                if node_noncoverage < statistics.record[-1]['optimal']:
                    statistics.append_record(optimal=node_noncoverage)
                print(statistics)
                print_placed_station(node, data)
            return True
    else:
        """ 
        The method gives the sequence of best decisions. Results consist of 
        optimal solutions and feasible solutions.
        """
        if node.left_child.noncoverage.estimate <= (
                statistics.record[-1]['optimal'] + data.deviation):

            if is_able_to_connect_gateways(node.left_child,
                                           data.gateway_coordinate):
                node_noncoverage = (node.left_child.noncoverage.left +
                                    node.left_child.noncoverage.right)

                if node_noncoverage < statistics.record[-1]['optimal']:
                    statistics.append_record(optimal=node_noncoverage)
                else:
                    statistics.append_record(feasible=node_noncoverage)
                print(statistics)
                print_placed_station(node, data)
            return True


def check_estimate(p: int,
                   s: int,
                   node: Node,
                   data: dataclass,
                   statistics: Schedule,
                   eng) -> bool:
    """

    Parameters
    ----------
    p - index of placement
    s - index of station
    node - node of binary tree
    data - input data
    statistics - record schedule
    eng- MatLab engine

    Returns
    -------
        True if noncoverage_estimate is not more than obtained record,
        False - otherwise
    """
    node.left_child.noncoverage.estimate = get_noncoverage_estimation(
        p, s, node, data, eng, flag='ILP')

    statistics.add(p, s, node.left_child)

    # if better_than_record(node, data, statistics):
    #     print(statistics)
    #     print_placed_station(node, data)

    return better_than_record(node, data, statistics)

    # if node.left_child.noncoverage.estimate <= (
    #         (statistics.record[-1]['optimal']) + data.deviation):
    #
    #     if is_able_to_connect_gateways(node.left_child,
    #                                    data.gateway_coordinate):
    #         node_noncoverage = (node.left_child.noncoverage.left +
    #                             node.left_child.noncoverage.right)
    #
    #         if node_noncoverage < statistics.record[-1]['optimal']:
    #             statistics.append_record(optimal=node_noncoverage)
    #         else:
    #             statistics.append_record(feasible=node_noncoverage)
    #
    #         print(statistics)
    #         print_placed_station(node, data)
    #
    #     return True
    # else:
    #     return False


def print_placed_station(node: Node, data: dataclass) -> None:
    """
    Print station placement
    Parameters
    ----------
    node - current node
    data - input data

    """
    i, j = np.where(node.left_child.pi == 1)
    placed_sta = ['-'] * len(data.placement_coordinate)

    for k in range(len(i)):
        placed_sta[i[k]] = 'S' + str(j[k] + 1)
    print(colored(placed_sta, 'magenta', 'on_green', attrs=['bold']))
