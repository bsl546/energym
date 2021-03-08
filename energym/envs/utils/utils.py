import os


def replace_ep_version(ep_version):
    """Sets the correct EnergyPlus version for the simulation model.

    Unused!

    Parameters
    ----------
    ep_version : str
        Version needed for the model.

    Returns
    -------
    str
        Path to the corresponding EnergyPlus version.
    """
    path_array = os.environ["PATH"].split(os.pathsep)
    updated_path_array = [
        entry for entry in path_array if not "EnergyPlus" in entry
    ]
    updated_path_array.append(ep_version)
    os.environ["PATH"] = os.pathsep.join(updated_path_array)
    return os.pathsep.join(updated_path_array)
