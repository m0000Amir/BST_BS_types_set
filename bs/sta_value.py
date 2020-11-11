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
    g_recv_link: list
    l_tr: list
    l_recv_link: list

    p_tr_coverage: list
    g_tr_coverage: list


@dataclass()
class UserDeviceParameterSet:
    """ This parameters is used to calculate
    coverage parameter between station and user device"""
    p_ud_coverage: float
    g_ud_coverage: float
    l_ud_coverage: float


@dataclass()
class GatewayParameterSet:
    """This parameters is used to calculate
    link distance parameter between station and gateway"""
    p_gateway: float
    g_gateway: float
    l_gateway: float


@dataclass
class GetDistanceInput:
    """ Inputs to solve distance parameters"""
    p_tr: float
    l_tr: float
    g_tr: float
    p_recv: float
    g_recv: float
    l_recv: float


def get_distance(lb_input, som: float = 10, f: float = 2437, k: float = -27.55):
    """
    Calculate distance parameter (link distance or coverage) using by link
    budget equation.

    :param lb_input: link budget equation input
    :param som: system operating margin
    :param f: radio wave centre frequency
    :param k: constant of free space path loss equation
    :return:
    """
    l_fs = (lb_input.p_tr - lb_input.l_tr + lb_input.g_tr + lb_input.g_recv -
            lb_input.l_recv - lb_input.p_recv - som)
    distance = round(10 ** ((l_fs - 20 * log10(f) - k)/20))
    return distance


def get_value(gateway, user_device, sta):
    sta_param = StaParameterSet(
        p_tr_link=list(sta[i]['Ptr_link'] for i in sta),
        g_tr_link=list(sta[i]['Gtr_link'] for i in sta),
        p_recv_link=list(sta[i]['Precv_link'] for i in sta),
        g_recv_link=list(sta[i]['Grecv_link'] for i in sta),
        l_tr=list(sta[i]['Ltr'] for i in sta),
        l_recv_link=list(sta[i]['Lrecv_link'] for i in sta),
        p_tr_coverage=list(sta[i]['Ptr_coverage'] for i in sta),
        g_tr_coverage=list(sta[i]['Gtr_coverage'] for i in sta),
    )
    ud_param = UserDeviceParameterSet(
        p_ud_coverage=user_device['Precv'],
        g_ud_coverage=user_device['Grecv'],
        l_ud_coverage=user_device['Lrecv'],
    )
    gtw_param = GatewayParameterSet(
        p_gateway=gateway['Precv'],
        g_gateway=gateway['Grecv'],
        l_gateway=gateway['Lrecv'],
    )
    i = [_ for _ in range(len(sta_param.p_tr_link))]
    j = [_ for _ in range(len(sta_param.p_tr_link))]
    link_distance = np.zeros([len(i), len(j)])
    link_distance2gtw = np.zeros([len(i)])
    coverage = np.zeros([len(i)])
    for s1, s2 in product(i, j):
        if s1 != s2:
            ld_input = GetDistanceInput(p_tr=sta_param.p_tr_link[s1],
                                        l_tr=sta_param.l_tr[s1],
                                        g_tr=sta_param.g_tr_link[s1],
                                        p_recv=sta_param.p_recv_link[s2],
                                        g_recv=sta_param.g_recv_link[s2],
                                        l_recv=sta_param.l_recv_link[s2])
            link_distance[s1, s2] = get_distance(ld_input)
    for s1 in i:
        ld2gtw_input = GetDistanceInput(p_tr=sta_param.p_tr_link[s1],
                                        l_tr=sta_param.l_tr[s1],
                                        g_tr=sta_param.g_tr_link[s1],
                                        p_recv=gtw_param.p_gateway,
                                        g_recv=gtw_param.g_gateway,
                                        l_recv=gtw_param.l_gateway)
        link_distance2gtw[s1] = get_distance(ld2gtw_input)
    for s1 in i:
        coverage_input = GetDistanceInput(p_tr=sta_param.p_tr_link[s1],
                                          l_tr=sta_param.l_tr[s1],
                                          g_tr=sta_param.g_tr_link[s1],
                                          p_recv=ud_param.p_ud_coverage,
                                          g_recv=ud_param.g_ud_coverage,
                                          l_recv=ud_param.l_ud_coverage)
        coverage[s1] = get_distance(coverage_input)
    return link_distance, link_distance2gtw, coverage


if __name__ == '__main__':
    get_value()
