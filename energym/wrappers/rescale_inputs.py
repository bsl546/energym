import numpy as np
import energym
from energym.spaces.box import Box
from energym.envs.env import InputsWrapper
from copy import deepcopy


class RescaleInputs(InputsWrapper):
    r"""Rescales the continuous inputs space of the environment to a given range. By default,
    it is rescaled between 0 and 1."""

    def __init__(self, env: energym.envs.env, lower_bound=None, upper_bound=None):

        super(RescaleInputs, self).__init__(env)

        rel_keys = [
            p
            for p in list(self.input_space.spaces.keys())
            if isinstance(self.input_space[p], Box)
        ]

        if upper_bound is None:
            upper_bound = {}
        if lower_bound is None:
            lower_bound = {}

        default_upper = {key: self.input_space[key].high[0] for key in rel_keys if
                         (key not in list(upper_bound.keys()))}
        default_lower = {key: self.input_space[key].low[0] for key in rel_keys if
                         (key not in list(lower_bound.keys()))}

        self.lower_bound = {**lower_bound, **default_lower}
        self.upper_bound = {**upper_bound, **default_upper}

    def inputs(self, inputs: dict) -> dict:

        inputs_cop = deepcopy(inputs)

        shared_keys = [
            p
            for p in inputs_cop
            if p in list(self.lower_bound.keys()) and isinstance(self.input_space[p], Box)
        ]

        for key in shared_keys:
            inputs_cop[key] = list(
                self.lower_bound[key]
                + (self.upper_bound[key] - self.lower_bound[key])
                * (
                    (np.array(inputs_cop[key]))
                )
            )

        return inputs_cop

    def revert_inputs(self, inputs):

        inputs_cop = deepcopy(inputs)

        shared_keys = [
            p
            for p in inputs_cop
            if p in list(self.lower_bound.keys()) and isinstance(self.input_space[p], Box)
        ]

        for key in shared_keys:
            inputs_cop[key] = list(
                (np.array(inputs_cop[key]) - self.lower_bound[key])
                / (self.upper_bound[key] - self.lower_bound[key])

            )
        return inputs_cop
