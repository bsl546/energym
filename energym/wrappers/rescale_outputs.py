import energym
from energym.envs.env import OutputsWrapper
from copy import deepcopy
from energym.spaces.box import Box


class RescaleOutputs(OutputsWrapper):
    r"""Rescales the continuous outputs space of the environment to a given range. By default, variables are rescaled
    between 0 and 1."""

    def __init__(
        self, env: energym.envs.env, lower_bound=None, upper_bound=None
    ):

        super(RescaleOutputs, self).__init__(env)

        rel_keys = [
            p
            for p in list(self.output_space.spaces.keys())
            if isinstance(self.output_space[p], Box)
        ]

        if upper_bound is None:
            upper_bound = {}
        if lower_bound is None:
            lower_bound = {}

        default_upper = {
            key: self.output_space[key].high[0]
            for key in rel_keys
            if (key not in list(upper_bound.keys()))
        }
        default_lower = {
            key: self.output_space[key].low[0]
            for key in rel_keys
            if (key not in list(lower_bound.keys()))
        }

        self.lower_bound = {**lower_bound, **default_lower}
        self.upper_bound = {**upper_bound, **default_upper}

    def outputs(self, outputs: dict):

        output_cop = deepcopy(outputs)
        shared_keys = [
            p for p in output_cop if p in list(self.lower_bound.keys())
        ]

        for key in shared_keys:
            if isinstance(output_cop[key], list):
                for i in range(len(output_cop[key])):
                    output_cop[key][i] = (
                        output_cop[key][i] - self.lower_bound[key]
                    ) / (self.upper_bound[key] - self.lower_bound[key])
            else:
                output_cop[key] = (
                    output_cop[key] - self.lower_bound[key]
                ) / (self.upper_bound[key] - self.lower_bound[key])

        return output_cop

    def revert_outputs(self, outputs: dict):

        output_cop = deepcopy(outputs)
        shared_keys = [
            p for p in output_cop if p in list(self.lower_bound.keys())
        ]

        for key in shared_keys:
            output_cop[key] = self.lower_bound[key] + (
                output_cop[key]
                * (self.upper_bound[key] - self.lower_bound[key])
            )
        return output_cop
