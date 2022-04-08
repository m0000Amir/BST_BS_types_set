from typing import List

import numpy as np


class KnapsackProblem:
    def __init__(self, cov: List, cost: List, cost_limit: float):
        self.cov = cov
        self.cost = cost
        self.cost_limit = cost_limit
        self._column_name = ['s' + str(i + 1) for i in range(len(self.cov))]
        self._f = None
        self._ineq_constraints = None
        self._b = None
        self._eq_constraints = np.array([])  # empty
        self._beq = np.array([])  # empty
        self._intcon = np.array([[i + 1 for i in range(self.get_column_num)]])
        self._lb = np.zeros([len(self.cov)])
        self._ub = np.ones([len(self.cov)])
        self.prepare()

    def prepare(self) -> None:
        """Prepare data of problem"""

        """
        Objective function
        Coefficient -2 means that we solve maximization problem (multiple all 
        value to -1) and also there are left coverage area and right coverage 
        area for each station (2* cov)
        """

        f = [-2 * self.cov[i] for i in range(self.get_column_num)]
        self._f = np.array(f)

        """ Inequality Constraints"""
        ineq_cost = [self.cost[i] for i in range(self.get_column_num)]
        self._ineq_constraints = np.array(ineq_cost)
        self._b = np.array(self.cost_limit)

        """ 
        There is no equality constraints. 
        self._eq_constraints is empty
        self._beq is empty
        """

    @property
    def get_column_num(self) -> int:
        return len(self._column_name)

    @property
    def get_column_name(self) -> List[str]:
        return self._column_name

    @property
    def get_f(self) -> np.ndarray:
        return self._f

    @property
    def get_ineq(self) -> np.ndarray:
        return self._ineq_constraints

    @property
    def get_b(self) -> np.ndarray:
        return self._b

    @property
    def get_eq(self) -> np.ndarray:
        return self._eq_constraints

    @property
    def get_beq(self) -> np.ndarray:
        return self._beq

    @property
    def get_intcon(self) -> np.ndarray:
        return self._intcon

    @property
    def get_lb(self) -> np.ndarray:
        return self._lb

    @property
    def get_ub(self) -> np.ndarray:
        return self._ub
