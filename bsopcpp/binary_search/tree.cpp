//
// Created by Амир Мухтаров on 26.04.2022.
//
#include <iostream>
#include <vector>

class ParameterRange {
    double estimate;
    double left;
    double right;
};


class Node {
public:
    int key;
    std::vector<std::vector<double>> pi;

    Node (std::vector<std::vector<double>> & _pi, int & _key) {
        key = _key;
        pi = _pi;
    };
    Node() {
        pi = std::vector<std::vector<double>>(0, std::vector<double>(0));
        key = 0;
    }
};



class Tree {
public:
    Node top;

    Tree() {
        std::vector<std::vector<double>> _val(10, std::vector<double>(10));
        int key = 0;
        top = Node(_val, key);
    }
};
