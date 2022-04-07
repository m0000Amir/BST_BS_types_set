//
// Created by Амир Мухтаров on 07.04.2022.
//
#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <nlohmann/json.hpp>


using json = nlohmann::json;

struct Restriction{
    unsigned int cost_limit;
    unsigned int delay_limit;
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
    std::map<std::string, int> sta;
    int _sta_count = sta.size();
    std::map<std::string, int> gateway;
    std::map<std::string, int> user_device;
    unsigned int frequency;
    unsigned int link_som;
    unsigned int coverage_som;
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
    int cost;
    int throughput;
    Radio radio;
};

/**
 * Preparation of problem input data
 * @param input_dataset from JSON-file
 * @return  Data: data
 */
InputData prepare(json input_dataset) {
    InputData a;
    return a;
}


/**
 * Search for the optimal placement
 * @param input_dataset input data of an optimal problem
 */
void run(json input_dataset) {

    InputData data = prepare(input_dataset);

    std::cout << "Hi!" << std::endl;


}
