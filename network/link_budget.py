"""
It is used link budget equation to calculate link distance parameter beetwen
station and coverage parameter of station.

LINK BUDGET:
Ptr - Ltr + Gtr - Lfs + Grecv - Lrecv = SOM + Precv,
where
    Ptr is a transmitter output power, [dBm];

    Ltr is a ransmitter losses, [dB];

    Gtr is a transmitter antenna gain, [dBi];

    Lfs is a free space path loss, [dB];

    Grecv is a receiver antenna gain,  [dBi];

    Lrecv is a receiver losses, [dB];

    SOM is a system operating margin, [dB];

    Precv is a receiver sensitivity, [dBm].

The Free Space Path Loss equation defines the propagation signal loss between
two antennas through free space (air).

FREE SPACE PATH LOSS EQUATION:
    FSPL = ((4⋅pi⋅R⋅f)/c)^2.

This formula expressed in decibels will be calculated as:
    L_fs = 20⋅lg(F) + 20⋅lg(R) + K,
where
    F is a radio wave centre frequency of a communication link;
    R is a distance between transmit and receive antennas;
    K is a constant.

Constant K depends on frequency and distance:

    - for a frequency in GHz and a distance in km, constant K is equal to 92.45;
    - for a frequency in MHz and distance in km, constant K is equal to 32.4;
    - for a frequency in MHz and distance in m, constant K is equal to -27.55.

"""

from dataclasses import dataclass
from math import log10
from itertools import product
from typing import Tuple


import numpy as np


@dataclass()
class StaParameterSet:
    """
    Given station parameter set. This parameters is used to calculate
    link distance parameter between station and coverage parameter of station
    """
    p_tr_link: list
    g_tr_link: list
    p_recv_link: list
    l_link: list
    l_coverage: list
    p_recv_coverage: list
    g_recv_coverage: list


@dataclass()
class UserDeviceParameterSet:
    """ This parameters is used to calculate
    coverage parameter between station and user device"""
    p_tr: float
    g_tr: float
    l_tr: float


@dataclass()
class GatewayParameterSet:
    """This parameters is used to calculate
    link distance parameter between station and gateway"""
    p_tr: float
    g_tr: float
    p_recv: float
    g_recv: float
    l_recv: float


@dataclass
class GetDistanceInput:
    """ Inputs to solve distance parameters"""
    p_tr: float
    l_tr: float
    g_tr: float
    p_recv: float
    g_recv: float
    l_recv: float


def get_distance(lb_input: GetDistanceInput,
                 som: float = 10,
                 f: float = 2437,
                 k: float = -27.55) -> float:
    """
        Using Link Budget Equation and Friis equation obtaining distance between
        transmitter and receiver
    Parameters
    ----------
    lb_input - link budget equation input
    som - system operating margin
    f - radio wave centre frequency
    k - constant of free space path loss equation

    Returns
    -------
        Distance of radio signal broadcast

    """
    l_fs = (lb_input.p_tr - lb_input.l_tr + lb_input.g_tr + lb_input.g_recv -
            lb_input.l_recv - lb_input.p_recv - som)
    distance = round(10 ** ((l_fs - 20 * log10(f) - k)/20))
    return distance


def get_station_parameters(
        gateway: dict,
        user_device: dict,
        sta: list,
        f: float,
        link_som: float,
        coverage_som: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:

    sta_param = StaParameterSet(
        p_tr_link=list(sta[i]['Ptr_link'] for i in range(len(sta))),
        g_tr_link=list(sta[i]['Gtr_link'] for i in range(len(sta))),
        p_recv_link=list(sta[i]['Precv_link'] for i in range(len(sta))),
        l_link=list(sta[i]['L_link'] for i in range(len(sta))),
        l_coverage=list(sta[i]['L_coverage'] for i in range(len(sta))),
        p_recv_coverage=list(sta[i]['Precv_coverage'] for i in range(len(sta))),
        g_recv_coverage=list(sta[i]['Grecv_coverage'] for i in range(len(sta))),
    )
    ud_param = UserDeviceParameterSet(
        p_tr=user_device['Ptr'],
        g_tr=user_device['Gtr'],
        l_tr=user_device['Ltr'],
    )
    gtw_param = GatewayParameterSet(
        p_tr=gateway['Ptr'],
        g_tr=gateway['Gtr'],
        p_recv=gateway['Precv'],
        g_recv=gateway['Grecv'],
        l_recv=gateway['Lrecv'],
    )
    i = [_ for _ in range(len(sta_param.p_tr_link))]
    j = [_ for _ in range(len(sta_param.p_tr_link))]
    link_distance2sta = np.zeros([len(i), len(j)])
    link_distance2gateway = np.zeros([len(i)])
    gtw2link_distance = np.zeros([len(i)])
    coverage = np.zeros([len(i)])
    for s1, s2 in product(i, j):
        if s1 != s2:
            ld_input = GetDistanceInput(p_tr=sta_param.p_tr_link[s1],
                                        l_tr=sta_param.l_link[s1],
                                        g_tr=sta_param.g_tr_link[s1],
                                        p_recv=sta_param.p_recv_link[s2],
                                        g_recv=sta_param.g_tr_link[s2],
                                        l_recv=sta_param.l_link[s2])
            link_distance2sta[s1, s2] = get_distance(ld_input,
                                                     som=link_som,
                                                     f=f)
    for s1 in i:
        ld2gtw_input = GetDistanceInput(p_tr=sta_param.p_tr_link[s1],
                                        l_tr=sta_param.l_link[s1],
                                        g_tr=sta_param.g_tr_link[s1],
                                        p_recv=gtw_param.p_recv,
                                        g_recv=gtw_param.g_recv,
                                        l_recv=gtw_param.l_recv)
        link_distance2gateway[s1] = get_distance(ld2gtw_input,
                                                 som=link_som,
                                                 f=f)
    for s1 in i:
        gtw2ld_input = GetDistanceInput(p_tr=gtw_param.p_tr,
                                        g_tr=gtw_param.g_tr,
                                        l_tr=gtw_param.l_recv,
                                        p_recv=sta_param.p_recv_link[s1],
                                        l_recv=sta_param.l_link[s1],
                                        g_recv=sta_param.g_tr_link[s1],
                                        )
        gtw2link_distance[s1] = get_distance(gtw2ld_input,
                                             som=link_som,
                                             f=f)
    for s1 in i:
        coverage_input = GetDistanceInput(p_tr=ud_param.p_tr,
                                          l_tr=ud_param.l_tr,
                                          g_tr=ud_param.g_tr,

                                          p_recv=sta_param.p_recv_coverage[s1],
                                          l_recv=sta_param.l_coverage[s1],
                                          g_recv=sta_param.g_recv_coverage[s1])
        coverage[s1] = get_distance(coverage_input, som=coverage_som, f=f)
    print('coverage = {}'.format(coverage))
    print('link distance = {}'.format(link_distance2sta))
    print('link distance 2 gateway = {}'.format(link_distance2gateway))
    print('gateway 2 link distance = {}'.format(gtw2link_distance))
    return link_distance2sta, link_distance2gateway, coverage


if __name__ == '__main__':
    coverage_input1 = GetDistanceInput(p_tr=20,
                                       l_tr=1,
                                       g_tr=5,
                                       p_recv=-67,
                                       l_recv=0,
                                       g_recv=1)

    coverage_input2 = GetDistanceInput(p_tr=9,
                                       l_tr=0,
                                       g_tr=1,
                                       p_recv=-77,
                                       l_recv=1,
                                       g_recv=5)

    print(get_distance(coverage_input1, som=14))
    print(get_distance(coverage_input2, som=14))
