# Wrappers

Wrappers are used to transform an environment in a modular way:

```python
from gym.wrappers import MyWrapper
env = energym.make('SimpleHouseSlab-v0')
env = MyWrapper(env)
```

## Quick tips for writing your own wrapper

- Don't forget to call `super(class_name, self).__init__(env)` if you override the wrapper's `__init__` function
- You can access the inner environment with `self.unwrapped`
- You can access the previous layer using `self.env`
- The variables `metadata`, `input_space`, `output_space`  and `spec` are copied to `self` from the previous layer
- Create a wrapped function for at least one of the following: `__init__(self, env)`, `step`, `reset`
- Your layered function should take its input from the previous layer (`self.env`) and/or the inner layer (`self.unwrapped`)
