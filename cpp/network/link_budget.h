//
// Created by Амир Мухтаров on 08.04.2022.
//

#ifndef BST_BS_TYPES_SET_LINK_BUDGET_H
#define BST_BS_TYPES_SET_LINK_BUDGET_H

#endif //BST_BS_TYPES_SET_LINK_BUDGET_H

int get_station_parameters(std::map<std::string, int> gateway,
                           std::map<std::string, unsigned int> user_device,
                           std::vector<std::map<std::string, int>> sta,
                           int frequency,
                           int link_som,
                           int coverage_som);