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
#include <string>
#include <map>
#include <vector>

/**
 * Given station parameter set. This parameters is used to calculate
 * link distance parameter between station and coverage parameter of station
 */
struct StaParametersSet{
    std::vector<unsigned int> p_tr_link;
    std::vector<unsigned int> g_tr_link;
    std::vector<int> p_recv_link;
    std::vector<unsigned int> l_link;
    std::vector<unsigned int> l_coverage;
    std::vector<int> p_recv_coverage;
    std::vector<unsigned int> g_recv_coverage;
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
    unsigned int p_tr;
    unsigned int l_tr;
    unsigned int g_tr;
    int p_recv;
    unsigned int g_recv;
    unsigned int l_recv;
};


int get_station_parameters(std::map<std::string, int> gateway,
                           std::map<std::string, unsigned int> user_device,
                           std::vector<std::map<std::string, int>> sta,
                           int frequency,
                           int link_som,
                           int coverage_som) {

    StaParametersSet sta_param;
    for (int i=0; i<sta.size(); i++) {
        sta_param.p_tr_link.push_back(sta[i]["Ptr_link"]);
        sta_param.g_tr_link.push_back(sta[i]["Gtr_link"]);
        sta_param.p_recv_link.push_back(sta[i]["Precv_link"]);
        sta_param.l_link.push_back(sta[i]["L_link"]);
        sta_param.l_coverage.push_back(sta[i]["L_coverage"]);
        sta_param.p_recv_coverage.push_back(sta[i]["Precv_coverage"]);
        sta_param.g_recv_coverage.push_back(sta[i]["Grecv_coverage"]);
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

    std::cout << user_device["Ptr"];
    return 0;
}
