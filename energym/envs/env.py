import os
from pathlib import Path
from os.path import expanduser


class Env:
    """The main Energym class to describe an abstract simulation environment.

    It encapsulates an environment with arbitrary behind-the-scenes
    dynamics. An environment can be partially or fully observed.


    Notes
    -----
    Are the functions render() and seed() needed? TODO
    Is this class in general useful? Do we plan to incorporate other
    simulation models which are not FMUs? TODO
    Accept field keys or identify them? Maybe not a good idea... # TODO

    Attributes
    ----------
    input_space
        The Space object corresponding to valid actions
    output_space
        The Space object corresponding to valid observations
    reward_range : tuple
        A tuple corresponding to the min and max possible rewards
    energym_path : str
        Absolute path to the energym folder.
    runs_path : str
        Path to store the information of the simulation run.

    Methods
    -------
    step(action)
        Advances the simulation by one timestep. (not implemented)
    reset()
        Resets the simulation environment. (not implemented)
    close()
        Closes the simulation environment. (not implemented)
    get_forecast()
        Gets the forecasts for external parameters.
    get_output()
        Gets the outputs of the last simulation step.

    """

    metadata = {"render.modes": []}
    reward_range = (-float("inf"), float("inf"))
    spec = None

    # Set these in ALL subclasses
    input_space = None
    output_space = None

    def __init__(self):
        """ """
        self.energym_path = Path(__file__).resolve().parent.parent.parent
        home = expanduser("~")
        self.runs_path = os.path.join(home, "Energym_runs")
        if not os.path.isdir(self.runs_path):
            try:
                os.mkdir(self.runs_path)
            except:
                raise Exception("Unable to create folder 'runs'")

    def step(self, action):
        """Advances the simulation by one timestep.

        Not implemented. Subclasses should override this method.

        Parameters
        ----------
        action : dict
            An action provided by the controller

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError

    def reset(self):
        """Resets the simulation environment.

        Not implemented. Subclasses should override this method.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError

    def close(self):
        """Closes the simulation environment.

        Not implemented. Subclasses should override this method.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError

    def get_forecast(self, **kwargs):
        """Return forecasts for the environment.

        Not implemented. Subclasses should override this method.

        Raises
        ------
        NotImplementedError
        """
        return None

    def get_output(self):
        """Gets the outputs of the last simulation step.

        Not implemented. Subclasses should override this method.

        Raises NotImplementedError
        """

        raise NotImplementedError

    @property
    def unwrapped(self):
        """Completely unwrap this env.

        Returns
        -------
        energym.Env
            The base non-wrapped energym.Env instance.
        """
        return self

    def __str__(self):
        if self.spec is None:
            return "<{} instance>".format(type(self).__name__)
        else:
            return "<{}<{}>>".format(type(self).__name__, self.spec.id)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
        # propagate exception
        return False


class Wrapper(Env):
    """Wraps the environment to allow a modular transformation.

    This class is the base class for all wrappers. The subclass could override
    some methods to change the behavior of the original environment without touching the
    original code.

    .. note::

        Don't forget to call ``super().__init__(env)`` if the subclass overrides :meth:`__init__`.

    """

    def __init__(self, env):
        self.env = env
        self.input_space = self.env.input_space
        self.output_space = self.env.output_space

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(
                "attempted to get missing private attribute '{}'".format(name)
            )
        return getattr(self.env, name)

    @classmethod
    def class_name(cls):
        return cls.__name__

    def step(self, inputs):
        return self.env.step(inputs)

    def get_forecast(self, **kwargs):
        return self.env.get_forecast(**kwargs)

    def get_output(self):
        return self.env.get_output()

    def reset(self, **kwargs):
        return self.env.reset(**kwargs)

    def close(self):
        return self.env.close()

    def __str__(self):
        return "<{}{}>".format(type(self).__name__, self.env)

    def __repr__(self):
        return str(self)

    @property
    def unwrapped(self):
        return self.env.unwrapped


class OutputsWrapper(Wrapper):
    """Wrapper to transform simulations outputs"""

    def reset(self, **kwargs):
        outputs = self.env.reset(**kwargs)
        return self.outputs(outputs)

    def step(self, inputs):
        outputs = self.env.step(inputs)
        return self.outputs(outputs)

    def get_forecast(self, **kwargs):
        forecast = self.env.get_forecast(**kwargs)
        return self.outputs(forecast)  # forecasts always have to be part of the outputs

    def get_output(self):
        return self.outputs(self.env.get_output())

    def outputs(self, outputs):
        raise NotImplementedError

    def revert_outputs(self, outputs):
        raise NotImplementedError


class StepWrapper(Wrapper):
    """Wrapper to transform steps"""

    def reset(self, **kwargs):
        return self.env.reset(**kwargs)

    def step(self, inputs):
        raise NotImplementedError


class InputsWrapper(Wrapper):
    """Wrapper to transform simulations inputs"""

    def reset(self, **kwargs):
        return self.env.reset(**kwargs)

    def step(self, inputs):
        return self.env.step(self.inputs(inputs))

    def inputs(self, inputs):
        raise NotImplementedError

    def revert_inputs(self, inputs):
        raise NotImplementedError