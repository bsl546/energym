import numpy as np

from energym.envs.env import InputsWrapper
from energym.spaces.box import Box


class ClipInputs(InputsWrapper):
    r"""Clip the continuous action within the valid bound. """

    def __init__(self, env):

        self.rel_keys = [
            p
            for p in list(env.input_space.spaces.keys())
            if isinstance(env.input_space[p], Box)
        ]

        super(ClipInputs, self).__init__(env)

    def inputs(self, inputs):

        to_clip = [key for key in inputs if key in self.rel_keys]
        for key in to_clip:
            inputs[key] = np.clip(
                inputs[key], self.input_space[key].low[0], self.input_space[key].high[0]
            )
        return inputs
