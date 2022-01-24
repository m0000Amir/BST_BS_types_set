from binary_search.tree import Node

from branch_and_bound.estimation.problem.ilp import ILP
from branch_and_bound.estimation.problem.knapsack import KnapsackProblem
from branch_and_bound.estimation.problem import gurobi
from branch_and_bound.estimation.problem import lp
from network.performance_characteristics import noncoverage_between_station
from binary_search.schedule import Schedule


from typing import Tuple, Any
from dataclasses import dataclass


import numpy as np
from termcolor import colored


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



def get_noncoverage_estimation(p: int,
                               s: int,
                               node: Node,
                               data: dataclass) -> Tuple[float, bool]:
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

    vacant_stations_coverage = [data.radio.coverage[i]
                                for i in range(len(data.radio.coverage))
                                if (i not in j) and (i != s)]
    vacant_stations_cost = [data.cost[i] for i in range(len(data.radio.coverage))
                            if (i not in j) and (i != s)]

    vacant_placement_points = [data.placement_coordinate[j]
                               for j in range(len(data.placement_coordinate))
                               if (j not in i) and (j != p)]

    if len(vacant_stations_coverage) is 0 or len(vacant_placement_points) is 0:
        right_noncoverage_estimate = node.left_child.noncoverage.right
    else:
        remaining_cost = data.restriction.cost_limit - node.cost - data.cost[s]

        if data.configuration.estimation_method == 'knapsack':
            problem = KnapsackProblem(vacant_stations_coverage,
                                      vacant_stations_cost,
                                      remaining_cost)
        # elif flag == 'ILP' or flag == 'LP':
        else:
            problem = ILP(vacant_stations_coverage,
                          vacant_stations_cost,
                          remaining_cost,
                          vacant_placement_points)

        if ((data.configuration.estimation_method == 'knapsack') or
                (data.configuration.estimation_method == 'ILP')):
            # # todo: delete matlpab solver
            # right_cov_estimate = solve_ilp_problem(problem, engine)
            right_cov_estimate = gurobi.solve(problem)

        else:
            right_cov_estimate = lp.solve_problem(problem)

        right_noncoverage_estimate = noncoverage_between_station(
            data.placement_coordinate[p], data.gateway_coordinate[1],
            data.radio.coverage[s], right_cov_estimate)

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
    from binary_search.get import is_able_to_get_solution

    if data.configuration.deviation is None:
        "The method gives optimal solutions."
        if (node.left_child.noncoverage.estimate <
                statistics.record[-1]['optimal']):

            # if is_able_to_connect_gateways(node.left_child,
            #                                data.gateway_coordinate):
            if is_able_to_get_solution(node, data):
                node_noncoverage = (node.left_child.noncoverage.left +
                                    node.left_child.noncoverage.right)

                if node_noncoverage < statistics.record[-1]['optimal']:
                    statistics.append_record(node, optimal=node_noncoverage)
                    print(statistics)
                    print_placed_station(node, data)
            return True
    else:
        """ 
        The method gives the sequence of best decisions. Results consist of 
        optimal solutions and feasible solutions.
        """
        # if node.left_child.noncoverage.estimate <= (
        #         statistics.record[-1]['optimal'] + data.deviation):
        if node.left_child.noncoverage.estimate <= (
                data.last_optimal_noncoverage + data.deviation):

            # if is_able_to_connect_gateways(node.left_child,
            #                                data.gateway_coordinate):

            if is_able_to_get_solution(node, data):
                node_noncoverage = (node.left_child.noncoverage.left +
                                    node.left_child.noncoverage.right)
                if node_noncoverage <= (data.last_optimal_noncoverage +
                                        data.deviation):
                    if len(statistics.record) == 1:
                        # Initial record (all linear section)
                        statistics.append_record(node, optimal=node_noncoverage)
                        print(statistics)
                        print_placed_station(node, data)
                    else:
                        statistics.append_record(node, feasible=node_noncoverage)
                        print(statistics)
                        print_placed_station(node, data)
            return True


def check_estimation(p: int,
                     s: int,
                     node: Node,
                     data: dataclass,
                     statistics: Schedule,
                     eng) -> bool:
    # todo: delete eng
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


    # if not data.place_all_station and eng is None:
    #     raise TypeError

    if data.configuration.place_all_station:
        # TODO: rewrite in function
        i, j = np.where(node.pi == 1)

        vacant_stations_coverage = [data.radio.coverage[i]
                                    for i in range(len(data.coverage))
                                    if (i not in j) and (i != s)]
        vacant_placement_points = [data.placement_coordinate[j]
                                   for j in
                                   range(len(data.placement_coordinate))
                                   if (j not in i) and (j != p)]

        right_noncoverage_estimate = noncoverage_between_station(
            data.placement_coordinate[p], data.gateway_coordinate[-1],
            data.radio.coverage[s], sum(2*vacant_stations_coverage))
        novcov_estimate = (node.left_child.noncoverage.left +
                           right_noncoverage_estimate)
        node.left_child.noncoverage.estimate = novcov_estimate

    else:
        node.left_child.noncoverage.estimate = get_noncoverage_estimation(
            p, s, node, data)

    return better_than_record(node, data, statistics)



