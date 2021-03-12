from energym.envs.env import OutputsWrapper


class TransformOutputs(OutputsWrapper):
    r"""Transform the outputs via an arbitrary function. May be used, in particular, to add custom outputs.
        Careful: the custom outputs are not registered in output_space. By rescaling, it is needed to first rescale and then
        add these custom outputs

    Example::

        >>> import energym
        >>> env = energym.make('SimpleHouseSlab-v0')
        >>> env = TransformObservation(env, lambda dict: f(dict))
        >>> env.reset()


    Args:
        env (Env): environment
        f ({callable}): callable function on dictionary

    """

    def __init__(self, env, f):
        super(TransformOutputs, self).__init__(env)

        assert callable(f)
        self._f = f

    def outputs(self, outputs):
        return self._f(outputs)
