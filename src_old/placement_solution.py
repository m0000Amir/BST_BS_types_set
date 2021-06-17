"""
Solution table for Binary search tree
"""
from collections import deque


class Schedule:
    """
    Solution table
    """
    def __init__(self):
        self.place = deque()
        self.station = deque()
        self.pi = deque()
        self.estimate = deque()
        self.step = deque()
        self.record = deque()
        self.print_record = list()

    def add(self, place, station, pi, estimate, step=0):
        """

        :param place: index of placement
        :param station: index of station
        :param pi: matrix pi
        :param estimate: estimate of 'non-coverage'
        :param step: node of binary search tree
        :return: new row of Solution table
        """
        self.place.append(place)
        self.station.append(station)
        self.pi.append(pi)
        self.estimate.append(estimate)
        self.step.append(step)
