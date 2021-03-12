import copy

from energym import spaces
from energym.envs.env import OutputsWrapper


class FilterOutputs(OutputsWrapper):
    """Filter dictionary observations by their keys.

    Args:
        env: The environment to wrap.
        filter_keys: List of keys to be included in the observations.

    Raises:
        ValueError: If observation keys in not instance of None or
            iterable.
        ValueError: If any of the `filter_keys` are not included in
            the original `env`'s observation space

    """

    def __init__(self, env, filter_keys=None):
        super(FilterOutputs, self).__init__(env)

        wrapped_output_space = env.output_space
        assert isinstance(
            wrapped_output_space, spaces.Dict
        ), "FilterObservationWrapper is only usable with dict observations."

        output_keys = wrapped_output_space.spaces.keys()

        if filter_keys is None:
            filter_keys = tuple(output_keys)

        missing_keys = set(key for key in filter_keys if key not in output_keys)

        if missing_keys:
            raise ValueError(
                "All the filter_keys must be included in the "
                "original output space.\n"
                "Filter keys: {filter_keys}\n"
                "Observation keys: {output_keys}\n"
                "Missing keys: {missing_keys}".format(
                    filter_keys=filter_keys,
                    output_keys=output_keys,
                    missing_keys=missing_keys,
                )
            )

        self.output_space = type(wrapped_output_space)(
            [
                (name, copy.deepcopy(space))
                for name, space in wrapped_output_space.spaces.items()
                if name in filter_keys
            ]
        )

        self._env = env
        self._filter_keys = tuple(filter_keys)

    def outputs(self, outputs):
        filter_outputs = self._filter_outputs(outputs)
        return filter_outputs

    def _filter_outputs(self, outputs):
        outputs = type(outputs)(
            {
                name: value
                for name, value in outputs.items()
                if name in self._filter_keys
            }
        )
        return outputs
