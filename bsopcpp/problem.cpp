//
// Created by Амир Мухтаров on 02.04.2022.
//
#include <iostream>
#include <fstream>
#include <nlohmann/json.hpp>
#include <chrono>

#include "binary_search/get.h"

using json = nlohmann::json;

//void run(json input_dataset);

int main() {
    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
    std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();

    std::ifstream json_file("../input/article_experience4_debug.json");
    json input_dataset = json::parse(json_file);

    std::cout << typeid(input_dataset.at("sta")).name() << std::endl;
    std::cout << "cost_limit is " << input_dataset.at("cost_limit")  << std::endl; // 12000

    std::cout << "Time difference = " <<
    std::chrono::duration_cast<std::chrono::nanoseconds> (end - begin).count() << " ns" << std::endl;

    run(input_dataset);

    return 0;
}
