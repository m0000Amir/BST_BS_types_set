//
// Created by Амир Мухтаров on 08.04.2022.
//
//It is used link budget equation to calculate link distance parameter beetwen
//station and coverage parameter of station.
//
//LINK BUDGET:
//Ptr - Ltr + Gtr - Lfs + Grecv - Lrecv = SOM + Precv,
//        where
//Ptr is a transmitter output power, [dBm];
//
//Ltr is a ransmitter losses, [dB];
//
//Gtr is a transmitter antenna gain, [dBi];
//
//Lfs is a free space path loss, [dB];
//
//Grecv is a receiver antenna gain,  [dBi];
//
//Lrecv is a receiver losses, [dB];
//
//SOM is a system operating margin, [dB];
//
//Precv is a receiver sensitivity, [dBm].
//
//The Free Space Path Loss equation defines the propagation signal loss between
//two antennas through free space (air).
//
//FREE SPACE PATH LOSS EQUATION:
//FSPL = ((4⋅pi⋅R⋅f)/c)^2.
//
//This formula expressed in decibels will be calculated as:
//L_fs = 20⋅lg(F) + 20⋅lg(R) + K,
//where
//        F is a radio wave centre frequency of a communication link;
//R is a distance between transmit and receive antennas;
//K is a constant.
//
//Constant K depends on frequency and distance:
//
//- for a frequency in GHz and a distance in km, constant K is equal to 92.45;
//- for a frequency in MHz and distance in km, constant K is equal to 32.4;
//- for a frequency in MHz and distance in m, constant K is equal to -27.55.


#include <iostream>
#include <cmath>
#include <string>
#include <map>
#include <vector>
#include "../../cppitertools/product.hpp"


/**
 * Given station parameter set. This parameters is used to calculate
 * link distance parameter between station and coverage parameter of station
 */
struct StaParametersSet{
    std::vector<int> p_tr_link;
    std::vector<int> g_tr_link;
    std::vector<int> p_recv_link;
    std::vector<int> l_link;
    std::vector<int> l_coverage;
    std::vector<int> p_recv_coverage;
    std::vector<int> g_recv_coverage;
};

/**
 * This parameters is used to calculate
 * coverage parameter between station and user device
 */
struct UserDeviceParameterSet {
    unsigned int p_tr;
    unsigned int g_tr;
    unsigned int l_tr;
};

/**
 * This parameters is used to calculate
 * link distance parameter between station and gateway
 */
struct GatewayParameterSet {
    int p_tr;
    int g_tr;
    int p_recv;
    int g_recv;
    int l_recv;
};


/**
 *  Inputs to solve distance parameters
 */
struct GetDistanceInput{
    int p_tr;
    int l_tr;
    int g_tr;
    int p_recv;
    int g_recv;
    int l_recv;
};

/**
 * Using Link Budget Equation and Friis equation obtaining distance
 * between transmitter and receiver
 * @param lb_input link budget equation input
 * @param som system operating margin
 * @param f radio wave centre frequency
 * @param k constant of free space path loss equation
 * @return Distance of radio signal broadcast
 */
double get_distance(GetDistanceInput lb_input,
                    int som = 10,
                    int f = 2437,
                    double k = -27.55) {
    double l_fs = (lb_input.p_tr - lb_input.l_tr + lb_input.g_tr + lb_input.g_recv -
            lb_input.l_recv - lb_input.p_recv - som);

    double distance = std::pow(
            10,
            (l_fs - 20 * std::log10(f) + lb_input.g_tr + lb_input.g_recv - k) / 20
            );
    return distance;
}

int get_station_parameters(std::map<std::string, int> gateway,
                           std::map<std::string, unsigned int> user_device,
                           std::vector<std::map<std::string, int>> sta,
                           int f,
                           int link_som,
                           int coverage_som) {

    StaParametersSet sta_param;
    for (auto &s: sta) {
        sta_param.p_tr_link.push_back(s["Ptr_link"]);
        sta_param.g_tr_link.push_back(s["Gtr_link"]);
        sta_param.p_recv_link.push_back(s["Precv_link"]);
        sta_param.l_link.push_back(s["L_link"]);
        sta_param.l_coverage.push_back(s["L_coverage"]);
        sta_param.p_recv_coverage.push_back(s["Precv_coverage"]);
        sta_param.g_recv_coverage.push_back(s["Grecv_coverage"]);
    };

    UserDeviceParameterSet ud_param = {
            .p_tr=user_device["Ptr"],
            .g_tr=user_device["Gtr"],
            .l_tr=user_device["Ltr"]
    };

    GatewayParameterSet gtw_param = {
            .p_tr=gateway["Ptr"],
            .g_tr=gateway["Gtr"],
            .p_recv=gateway["Precv"],
            .g_recv=gateway["Grecv"],
            .l_recv=gateway["Lrecv"],
    };


    std::vector<std::vector<double>> link_distance2sta(sta.size(),
                                                       std::vector<double>(
                                                               sta.size()));
    std::vector<double> link_distance2gateway(sta.size(), 0);
    std::vector<double> gtw2link_distance(sta.size(), 0);
    std::vector<double> coverage(sta.size(), 0);

    std::vector<int> _i(sta.size());
    std::vector<int> _j(sta.size());
    for (int i = 0; i < _i.size(); i++) {
        _i[i] = i;
        _j[i] = i;
    }

    for (auto&& [s1, s2] : iter::product(_i, _j)) {
        std::cout << s1 << ", " << s2 << '\n';
        if (s1 != s2) {
            GetDistanceInput ld_input = {
                    sta_param.p_tr_link[s1],
                    sta_param.l_link[s1],
                    sta_param.g_tr_link[s1],
                    sta_param.p_recv_link[s2],
                    sta_param.g_tr_link[s2],
                    sta_param.l_link[s2]
            };
            link_distance2sta[s1][s2] = get_distance(ld_input,
                                                     link_som,
                                                     f=f);
        }
    }

    for (auto& s1: _i) {
        GetDistanceInput ld2gtw_input = {
                sta_param.p_tr_link[s1],
                sta_param.l_link[s1],
                sta_param.g_tr_link[s1],
                gtw_param.p_recv,
                gtw_param.g_recv,
                gtw_param.l_recv
        };
        link_distance2gateway[s1] = get_distance(ld2gtw_input,
                                                 link_som,
                                                 f=f);
    }

    int aa;




//    std::cout << link_distance2sta[0][0] << std::endl;

    std::vector<int> v1{1,2,3};
    std::vector<int> v2{7,8};
    std::vector<std::string> v3{"the","cat"};
    std::vector<std::string> v4{"hi","what's","up","dude"};
    for (auto&& [a, b, c, d] : iter::product(v1,v2,v3,v4)) {
        std::cout << a << ", " << b << ", " << c << ", " << d << '\n';
    }

    return 0;
}
