cmake_minimum_required(VERSION 3.20)
project(BST_BS_types_set)

set(CMAKE_CXX_STANDARD 20)

find_package(nlohmann_json 3.10.5 REQUIRED)

add_executable(BST_BS_types_set
        bsopcpp/problem.cpp
        cppitertools/product.hpp
        bsopcpp/binary_search/get.cpp bsopcpp/binary_search/get.h
        bsopcpp/network/link_budget.cpp
        bsopcpp/network/link_budget.h
        bsopcpp/network/connection_between_station.cpp
        bsopcpp/network/connection_between_station.h bsopcpp/binary_search/tree.cpp
        bsopcpp/binary_search/tree.h bsopcpp/binary_search/tree.cpp)

target_link_libraries(BST_BS_types_set PRIVATE nlohmann_json::nlohmann_json)
