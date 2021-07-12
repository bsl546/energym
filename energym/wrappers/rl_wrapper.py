from energym.envs.env import StepWrapper
from gym.spaces import Box, Dict, Discrete
import numpy as np


class RLWrapper(StepWrapper):
    r"""Transform steps outputs to have rl (gym like) outputs timesteps, i.e. add rewards, done, and info
    Changes the outputs structure, from outputs to outputs, reward, done, info, as in gym.
    **To be put at the end of all other wrappers.**
    Example::

        >>> TBD


    Args:
        env (Env): environment
        reward_function: reward function

    """

    def __init__(self, env, reward_function):
        super(RLWrapper, self).__init__(env)
        self.observation_space, self.obs_names = self.__build_observation_space(
            self.output_specs
        )
        self.action_space, self.act_names = self.__build_action_space(self.input_specs)
        self.reward_range = (-float("inf"), float("inf"))
        self.metadata = {"render.modes": []}
        self.spec = None

        assert callable(reward_function)
        self.reward_function = reward_function

    def step(self, inputs):
        if isinstance(inputs, np.ndarray):
            actions = {}
            for i, inp in enumerate(inputs):
                act = self.act_names[i]
                if self.input_specs[act]["type"] == "discrete":
                    inp = round(inp)
                actions[act] = [inp]
            outputs = self.env.step(actions)
            reward = self.reward_function(outputs)
            outputs = np.array([outputs[obs] for obs in self.obs_names])
        else:
            outputs = self.env.step(inputs)
            reward = self.reward_function(outputs)
        self._last_output = outputs
        done = False
        info = {}
        return outputs, reward, done, info

    def __build_action_space(self, input_specs):
        """Collects the inputs from the simulation object.

        The inputs have to be contained in input_specs  but
        not every key of the two needs to be an input to the specific model.
        Builds a continuous version of the action space with interval [0,1] for
        originally discrete actions.

        Parameters
        ----------
        input_specs : dict
            Contains possible control inputs from the model.


        """
        input_array = self.get_inputs_names()
        act_names = []

        lower_bounds = []
        upper_bounds = []

        for act_name in input_array:
            if act_name in input_specs:
                act_names.append(act_name)
                act_specs = input_specs[act_name]
                if act_specs["type"] == "scalar":
                    lower_bounds.append(act_specs["lower_bound"])
                    upper_bounds.append(act_specs["upper_bound"])
                elif act_specs["type"] == "discrete":
                    lower_bounds.append(0)
                    upper_bounds.append(1)
                else:
                    raise TypeError("Wrong type in INPUT_SPECS.")
            else:
                raise ValueError("Undefined Input {}".format(act_name))

        lower_bounds = np.array(lower_bounds)
        upper_bounds = np.array(upper_bounds)

        return Box(lower_bounds, upper_bounds), act_names

    def __build_observation_space(self, output_specs):
        """Collects the outputs from the simulation object.

        The outputs have to be contained in output_specs, but not every
        key needs to be an output to the specific model.

        Parameters
        ----------
        output_specs : dict
            Contains possible outputs from the model.
        """
        output_array = self.get_outputs_names()
        obs_names = []

        lower_bounds = []
        upper_bounds = []

        for obs_name in output_array:
            obs_names.append(obs_name)
            obs_specs = output_specs[obs_name]
            if obs_specs["type"] == "scalar":
                lower_bounds.append(obs_specs["lower_bound"])
                upper_bounds.append(obs_specs["upper_bound"])
            elif obs_specs["type"] == "discrete":
                lower_bounds.append(0)
                upper_bounds.append(1)

        lower_bounds = np.array(lower_bounds)
        upper_bounds = np.array(upper_bounds)

        return Box(lower_bounds, upper_bounds), obs_names

    def reset(self):
        self.env.reset()
        return self.get_output()

    def get_output(self):
        out = self.env.get_output()
        out.pop("time")
        return list(out.values())
