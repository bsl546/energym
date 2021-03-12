import numpy as np
from energym.envs.env import StepWrapper


class DonwsampleOutputs(StepWrapper):
    r"""Transform the outputs via an arbitrary function.

    Example::

        >>> TBD


    Args:
        env (Env): environment
        steps: number of downsampling steps
        downsampling_dic ({keys:callable}): keys and callable functions on them

    """

    def __init__(self, env, steps: int, downsampling_dic: dict):
        super(DonwsampleOutputs, self).__init__(env)
        for key in downsampling_dic:
            assert callable(downsampling_dic[key])
        self.downsampling_dic = downsampling_dic
        self.steps = steps

    def step(self, inputs):
        output_dic = dict.fromkeys(self.downsampling_dic.keys())
        for key in output_dic:
            output_dic[key] = []
        for _ in range(self.steps):
            outputs = self.env.step(inputs)
            for key in output_dic:
                output_dic[key] += [outputs[key]]

        for key in self.downsampling_dic:
            output_dic[key] = self.downsampling_dic[key](output_dic[key])

        return output_dic

    def get_forecast(self, **kwargs):
        forecast = self.env.get_forecast(**kwargs)
        for key in forecast:
            forecast[key] = self.downsampling_dic[key](
                np.array(forecast[key])[
                    : (len(forecast[key]) // self.steps) * self.steps
                ].reshape(-1, self.steps),
                axis=1,
            )
            forecast[key] = list(forecast[key])

        return forecast
