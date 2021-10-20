"""
An optimal problem.
Branch and Bound method using Binary Search Tree.
"""
from network.connection_between_station import is_able_to_exist_solution
from binary_search.tree import Tree
from binary_search.schedule import Schedule
from network.performance_characteristics import solve_cost, solve_delay
from network.connection_between_station import check_station_connection
from bab.branch_and_bound import check_estimate
from network.link_budget import get_station_parameters


import matlab.engine


def get(input_data, share=0.1):
    """ Getting problem"""
    arrival_rate = input_data.arrival_rate
    average_packet_size = input_data.average_packet_size
    cost_limit = input_data.cost_limit
    delay_limit = input_data.delay_limit
    gateway_coordinate = input_data.gateway_placement
    placement_coordinate = input_data.placement

    cost = tuple(input_data.sta[i]['c'] for i in range(len(input_data.sta)))
    throughput = tuple(
        input_data.sta[i]['throughput'] for i in range(len(input_data.sta)))
    link_distance, link_distance2gateway, coverage = get_station_parameters(
        input_data.gateway,input_data.user_device, input_data.sta)

    deviation = share * (gateway_coordinate[1] - gateway_coordinate[0])

    assert is_able_to_exist_solution(
        link_distance, link_distance2gateway, placement_coordinate,
        gateway_coordinate), 'There is not problem for this case'

    # Starting Searching
    # Initialize Tree and Schedule
    tree = Tree()
    tree.initiate(placement_coordinate, coverage)

    statistics = Schedule(tree.top)
    statistics.record[-1]['optimal'] = gateway_coordinate[-1]

    engine = matlab.engine.start_matlab('-nojvm')
    engine.cd(r'./estimation/matlab/', nargout=0)

    parent = tree.top
    while tree.is_possible_to_add_new_nodes(parent):
        i, j = tree.get_indices(parent.pi)
        if (i is not None) and (j is not None):
            """add left node"""
            tree.add_left_node(i, j, parent)
            parent.left_child.cost = solve_cost(parent, cost[j])
            parent.left_child.delay = solve_delay(parent, arrival_rate,
                                                  average_packet_size,
                                                  throughput[j])

            """add right node"""
            tree.add_right_node(i, j, parent)
            parent.right_child.noncov = parent.noncov
            parent.right_child.cost = parent.cost
            parent.right_child.delay = parent.delay

            # PLOT GRAPH
            # draw(tree.graph)

            if (check_station_connection(i, j, parent, placement_coordinate, link_distance, link_distance2gateway, gateway_coordinate)
                    and check_estimate(i, j, parent, statistics, placement_coordinate, gateway_coordinate,
                                       coverage, cost, cost_limit, delay_limit,
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
