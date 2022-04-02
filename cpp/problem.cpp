//
// Created by Амир Мухтаров on 02.04.2022.
//
#include <iostream>
#include <fstream>
#include <nlohmann/json.hpp>


using json = nlohmann::json;

int main() {

    std::ifstream json_file("/Users/m0000a/Projects/BST_BS_types_set/input/article_experience4_debug.json");
    json input_dataset = json::parse(json_file);

    std::cout << input_dataset.at("cost_limit"); // 12000

    return 0;
}
