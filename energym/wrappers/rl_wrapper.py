from energym.envs.env import StepWrapper


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

        assert callable(reward_function)
        self.reward_function = reward_function

    def step(self, inputs):
        outputs = self.env.step(inputs)
        reward = self.reward_function(outputs)
        done = False
        info = {}
        return outputs, reward, done, info
