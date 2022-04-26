//
// Created by Амир Мухтаров on 15.04.2022.
//

#include <cmath>
#include <vector>

/**
 * Communication distance between Tx and Rx must be no less than the
 * distance between them.
 * @param place1 coordinate of Tx
 * @param place2 coordinate of Rx
 * @param communication_distance communication link distance
 * @return True if communication distance is more the distance between Tx and Rx
 */
bool _in_range(int& place1, int& place2, double& communication_distance) {
    return std::abs(place1 - place2) <= communication_distance;
}


/**
 * Checking the existence of feasible placement with a given placement
 * coordinates and given set of stations.
 * @param link_distance2sta communication link between stations
 * @param link_distance2gateway communication links between stations and gateway
 * @param gtw2link_distance communication links between gateway and stations
 * @param place placement coordinates
 * @param gtw coordinates of gateways
 * @return True if feasible placement is exist, False is otherwise
 */
bool is_able_to_exist_solution(
        std::vector<std::vector<double>>& link_distance2sta,
        std::vector<double>& link_distance2gateway,
        std::vector<double>& gtw2link_distance,
        std::vector<int>& place,
        std::vector<int>& gtw
        ) {

    auto maxElementIndex = (
            std::max_element(
                    link_distance2gateway.begin(),
                    link_distance2gateway.end()
                    ) - link_distance2gateway.begin());

    double maxElement = *std::max_element(link_distance2gateway.begin(),
                                          link_distance2gateway.end());

    if (!(_in_range(gtw[0], place[0], maxElement) and
            _in_range(gtw[0], place[0], gtw2link_distance[maxElementIndex]) and
            _in_range(gtw[1], place[-1], maxElement) and
            _in_range(gtw[1], place[-1], gtw2link_distance[maxElementIndex])
            )) {
        return false;
    }
    std::vector<std::vector<double>> _comm_dist(link_distance2sta);
//    _comm_dist.erase(maxElementIndex);

//    unsigned rowToDelete = 2;
//    if (myVector.size() > rowToDelete)
//    {
//        myVector.erase( myVector.begin() + rowToDelete );
//    }

    return true;
}