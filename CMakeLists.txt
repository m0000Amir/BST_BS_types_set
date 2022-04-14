cmake_minimum_required(VERSION 3.20)
project(BST_BS_types_set)

set(CMAKE_CXX_STANDARD 20)

find_package(nlohmann_json 3.10.5 REQUIRED)

add_executable(BST_BS_types_set
        cpp/problem.cpp
        cppitertools/product.hpp
        cpp/binary_search/get.cpp cpp/binary_search/get.h
        cpp/network/link_budget.cpp
        cpp/network/link_budget.h
        )

target_link_libraries(BST_BS_types_set PRIVATE nlohmann_json::nlohmann_json)
