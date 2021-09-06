"""
An optimal problem.
Branch and Bound method using Binary Search Tree.
"""
from connection.feasible_placement import is_able_to_exist_solution
from bab.bst import Tree
from bab.schedule import Schedule
from bab.evaluation import solve_cost, solve_delay
from connection.feasible_placement import check_link
from bab.branch_and_bound import check_estimate
from bs.sta_value import get_value


import matlab.engine


def get(input_data, share=0.1):
    """ Getting solution"""
    arrival_rate = input_data.arrival_rate
    average_packet_size = input_data.average_packet_size
    cost_limit = input_data.cost_limit
    delay_limit = input_data.delay_limit
    gtw = input_data.gateway_placement
    place = input_data.placement

    # cov = tuple(input_data.sta[i]['r'] for i in input_data.sta)
    # comm_dist = tuple(input_data.sta[i]['R'] for i in input_data.sta)
    cost = tuple(input_data.sta[i]['c'] for i in range(len(input_data.sta)))
    # departure_rate = tuple(input_data.sta[i]['mu'] for i in input_data.sta)
    throughput = tuple(input_data.sta[i]['throughput']
                       for i in range(len(input_data.sta)))
    comm_dist, comm_dist2gtw, cov = get_value(input_data.gateway,
                                              input_data.user_device,
                                              input_data.sta)

    deviation = share * (gtw[1] - gtw[0])

    assert is_able_to_exist_solution(comm_dist, comm_dist2gtw, place, gtw), (
        'There is not solution for this case')
    tree = Tree()
    statistics = Schedule()

    tree.initiate(place, cov)
    statistics.add(float('inf'), float('inf'), tree.top)
    # statistics.record.append(gtw[-1])
    statistics.record[-1]['optimal'] = gtw[-1]

    engine = matlab.engine.start_matlab('-nojvm')
    engine.cd(r'./estimation/matlab/', nargout=0)

    parent = tree.top
    while tree.is_possible_to_add_new_nodes(parent):
        i, j = tree.get_indices(parent.pi)
        if (i is not None) and (j is not None):
            """add left node"""
            tree.add_left_node(i, j, parent)

            # parent.left_child.noncov.estimate = solve_noncoverage(i, j,
            #                                                       parent, gtw,
            #                                                       place, cov)
            # parent.left_child.noncov.estimate = get_noncoverage(i, j, parent,
            #                                                     gtw, place,
            #                                                     cov, cost,
            #                                                     cost_limit,
            #                                                     engine)
            parent.left_child.cost = solve_cost(parent, cost[j])
            parent.left_child.delay = solve_delay(parent, arrival_rate,
                                                  average_packet_size,
                                                  throughput[j])
            # statistics.add(i, j, parent.left_child)
            # PLOT GRAPH
            # draw(tree.graph)

            """add right node"""
            tree.add_right_node(i, j, parent)

            parent.right_child.noncov = parent.noncov
            parent.right_child.cost = parent.cost
            parent.right_child.delay = parent.delay

            # PLOT GRAPH
            # draw(tree.graph)

            if (check_link(i, j, parent, place, comm_dist, comm_dist2gtw, gtw)
                    and check_estimate(i, j, parent, statistics, place, gtw,
                                       cov, cost, cost_limit, delay_limit,
                                       deviation, engine)):
                parent = parent.left_child
            else:
                tree.unchecked_node.pop()
                parent = parent.right_child
        else:
            parent = tree.unchecked_node[-1]
            tree.unchecked_node.pop()
        # draw(tree.graph)
    print('Total number of nodes is {}'.format(tree.node_keys[-1]))
