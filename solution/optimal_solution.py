"""
An optimal problem.
Branch and Bound method using Binary Search Tree.
"""
from connection.feasible_placement import is_able_to_exist_solution
from bab.bst import Tree
from bab.schedule import Schedule
from bab.evaluation import solve_noncoverage, solve_cost, solve_delay
from connection.feasible_placement import check_link
from bab.branch_and_bound import check_estimate_old_func


def get(input_data, share=0.1):
    """ Getting solution"""
    arrival_rate = input_data.arrival_rate
    cost_limit = input_data.cost_limit
    delay_limit = input_data.delay_limit
    gtw = input_data.gateway_placement
    place = input_data.placement

    # cov = tuple(input_data.sta[i]['r'] for i in input_data.sta)
    # comm_dist = tuple(input_data.sta[i]['R'] for i in input_data.sta)
    cost = tuple(input_data.sta[i]['c'] for i in input_data.sta)
    departure_rate = tuple(input_data.sta[i]['mu'] for i in input_data.sta)

    deviation = share * (gtw[1] - gtw[0])

    assert is_able_to_exist_solution(comm_dist, place, gtw), ('There is not '
                                                              'solution for '
                                                              'this case')
    tree = Tree()
    statistics = Schedule()

    tree.initiate(place, cov)
    statistics.add(float('inf'), float('inf'), tree.top)
    statistics.record.append(gtw[-1])

    parent = tree.top
    while tree.is_possible_to_add_new_nodes(parent):
        i, j = tree.get_indices(parent.pi)
        if (i is not None) and (j is not None):
            """add left node"""
            tree.add_left_node(i, j, parent)

            parent.left_child.noncov.estimate = solve_noncoverage(i, j,
                                                                  parent, gtw,
                                                                  place, cov)
            parent.left_child.cost = solve_cost(parent, cost[j])
            parent.left_child.delay = solve_delay(parent, arrival_rate,
                                                  departure_rate[j])
            statistics.add(i, j, parent.left_child)
            # PLOT GRAPH
            # draw(tree.graph)

            """add right node"""
            tree.add_right_node(i, j, parent)

            parent.right_child.noncov = parent.noncov
            parent.right_child.cost = parent.cost
            parent.right_child.delay = parent.delay

            # PLOT GRAPH
            # draw(tree.graph)

            if (check_link(i, j, parent, place, comm_dist, gtw) and
                check_estimate_old_func(parent.left_child, statistics, place, gtw,
                                        cost_limit, delay_limit, deviation)):
                parent = parent.left_child
            else:
                tree.unchecked_node.pop()
                parent = parent.right_child
        else:
            parent = tree.unchecked_node[-1]
            tree.unchecked_node.pop()
        # draw(tree.graph)
    print('Total number of nodes is {}'.format(tree.node_keys[-1]))
