//
// Created by Амир Мухтаров on 07.04.2022.
//
#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <algorithm>
#include <stdexcept>

#include "../network/link_budget.h"
#include "../network/connection_between_station.h"
#include "../network/connection_between_station.h"
#include "./tree.h"

#include <nlohmann/json.hpp>

using json = nlohmann::json;

struct Restriction{
    int cost_limit;
    int delay_limit;
};

struct Arrival{
    unsigned int rate;
    unsigned int packet_size;
};

struct Configuration{
    std::string method;
    bool place_all_station;
    std::string estimation_method;
    double deviation;
    double last_optimal_noncoverage;
    bool drawing;
};


struct Radio{
    std::vector<std::map<std::string, int>> sta;
    int _sta_count = sta.size();
    std::map<std::string, int> gateway;
    std::map<std::string, int> user_device;
    int frequency;
    int link_som;
    int coverage_som;
    std::vector<std::vector<double>> link_distance;
    std::vector<double> link_distance2gateway;
    std::vector<double> gateway2link_distance;
    std::vector<double> coverage;
};


struct InputData{
    Configuration configuration;
    std::vector<int> gateway_coordinate;
    std::vector<int> placement_coordinate;
    Restriction restriction;
    Arrival arrival;
    Radio radio;
    std::vector<int> cost;
    std::vector<int> throughput;

};


/**
 * Preparation of problem input data
 * @param input_dataset from JSON-file
 * @return  Data: data
 */
InputData prepare(json & input_dataset) {
    InputData data;
    // Given coordinates
    data.gateway_coordinate = input_dataset["gateway_placement"]
            .get<std::vector<int>>();
    data.placement_coordinate = input_dataset["placement"].get<std::vector<int>>();

    // Configuration of the problem
    data.configuration.method = input_dataset["configuration"]["method"];
    data.configuration.place_all_station =
            input_dataset["configuration"]["place_all_station"];




//    TODO: check it (NULL)
    if (input_dataset["configuration"]["relative_deviation"] != NULL) {
        data.configuration.deviation =
                input_dataset["configuration"]["relative_deviation"].get<double>
                        () * (data.gateway_coordinate[1] - data
                        .gateway_coordinate[0]);
    } else {
        data.configuration.deviation = 0.0;
    }
    data.configuration.last_optimal_noncoverage =
            input_dataset["configuration"]["last_optimal_noncoverage"];
    data.configuration.drawing = input_dataset["configuration"]["drawing"];

//    Exceptions
    const std::vector<std::string> method{"bf", "bab"};
    if (! std::count(method.begin(), method.end(), data.configuration.method)) {
        throw std::invalid_argument("Wrong method of solving the problem. "
                                    "Choose bf or bnb");
    }

    std::vector<std::string> estimation_method{"ILP", "knapsack", "LP"};
    if (std::find(estimation_method.begin(),
                  estimation_method.end(),
                  data.configuration.estimation_method) != estimation_method
                  .end()){
        throw std::invalid_argument("Wrong method of solving right estimation"
                                    " coverage of in branch and bound method."
                                    "  Choose ILP, knapsack or LP.");
    }

    if ((data.configuration.deviation != 0.0)  and (data.configuration
    .last_optimal_noncoverage != 0.0)){
        throw std::invalid_argument("Input data consist relative deviation."
                                    "It is necessary to give last found "
                                    "optimal noncoverage.");
    }

//    Given restriction of the problem
    data.restriction.delay_limit = input_dataset["delay_limit"];
    data.restriction.cost_limit = input_dataset["cost_limit"];

//  Given arrival parameters
    data.arrival.rate = input_dataset["arrival_rate"];
    data.arrival.packet_size = input_dataset["average_packet_size"];

//  Given cost and throughput of stations
    for (int i = 0; i < input_dataset["sta"].size(); i++) {
        data.cost.push_back(input_dataset["sta"][i]["cost"]);
        data.throughput.push_back(input_dataset["sta"][i]["throughput"]);
        data.radio.sta.push_back(input_dataset["sta"][i]);
    }

//  Radio communication parameters
    data.radio.gateway = input_dataset["gateway"];
    data.radio.user_device = input_dataset["user_device"];
    data.radio.frequency = input_dataset["frequency"];
    data.radio.link_som = input_dataset["link_som"];
    data.radio.coverage_som = input_dataset["coverage_som"];


    auto params = get_station_parameters(data.radio.gateway,
                                         data.radio.user_device,
                                         data.radio.sta,
                                         data.radio.frequency,
                                         data.radio.link_som,
                                         data.radio.coverage_som);

    data.radio.coverage = params.coverage;
    data.radio.link_distance = params.link_distance2sta;
    data.radio.link_distance2gateway = params.link_distance2gateway;
    data.radio.gateway2link_distance = params.gtw2link_distance;
    return data;
}


/**
 * Search for the optimal placement
 * @param input_dataset input data of an optimal problem
 */
void run(json input_dataset) {

    InputData data = prepare(input_dataset);
//    if (is_able_to_exist_solution(data.radio.link_distance,
//                                  data.radio.link_distance2gateway,
//                                  data.radio.gateway2link_distance,
//                                  data.placement_coordinate,
//                                  data.gateway_coordinate)) {
//        bool t;
//    }
    int n = data.placement_coordinate.size();
    int m = data.radio.sta.size();
    std::cout << "Placement number = " << n << std::endl;
    std::cout << "Station number = " << m << std::endl;

    if (data.configuration.place_all_station) {
        /**
         * C math library includes gamma function. Since Г(n) = (n-1)! for
         * positive integers, using tgamma of i+1 yields i!.
         */
        double feasible_placement = (std::tgamma(n+1)/(
                std::tgamma(n + 1 - m - 1) * std::tgamma(m+1))
                        ) * std::tgamma(m+1);
        std::cout << "Number of feasible placement = " << feasible_placement << std::endl;
    }

    /**
     * Starting Searching. Initialize Tree and Schedule
     */

    std::vector<std::vector<double>> _val(10, std::vector<double>(10));
    int key = 0;
    Tree tree;

    std::cout << "tree"<< std::endl;

    std::cout << "Hi!" << std::endl;
}
