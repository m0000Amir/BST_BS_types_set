from estimation.problem.knapsack import KnapsackProblem

import numpy as np


class ILP(KnapsackProblem):
    def __init__(self, cov, cost, cost_limit, place=None):
        super().__init__(cov, cost, cost_limit)
        self.num_place = len(place)

    def prepare(self):
        KnapsackProblem.prepare(self)
        ineq_number = [1 for i in range(self.get_column_num)]

        self._ineq_constraints = np.vstack(
            (self._ineq_constraints, ineq_number))
        if self.num_place is None:
            self._b = np.vstack((self._b, self.get_column_num))
        else:
            self._b = np.vstack((self._b, self.num_place))