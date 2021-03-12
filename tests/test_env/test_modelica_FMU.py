import numpy as np
import pandas as pd
import os, time
import platform

import matplotlib.pyplot as plt

import energym
from energym.envs.env_fmu_mod import EnvModFMU


# ============================================================================
# Constants
# ============================================================================
op_sys = platform.system().lower()
T0 = 273.15


# ============================================================================
# Model parameters
# -> this sould go in a json or yaml file
# ============================================================================
def dummy_model():
    mdl = {
        "model_path": os.path.join(
            "dummy",
            "fmus",
            "modelica_dummy_srcmo_vdp_osc",
        ),
        "start_time": 0,
        "stop_time": 30,
        "step_size": 0.1,
        "states": ["x1", "x2"],
        "params": {
            "mu": 1.0,   # damping
            "k": 1.0,   # stiffness
        },
        "in_specs": {
            "u": {"type": "scalar", "lower_bound": -1, "upper_bound": 1}
        },
        "out_specs": None,
        "init": {
            "x1": 1.0,
            "x2": 0.0
        },
        # Controller I/O and Gains
        "input": "u",
        "sensor": "x2",
        "ref": 0.0,
        "kp": 1.2,
        "bound": [-1, 1],
    }
    return mdl


def simple_house_rad():
    mdl = {
        # 'model_path'    : 'modelica\\HP1room\\fmus\\modelica_HP1room_srcmo_HP_u_Rad_1RC.fmu',
        "model_path": os.path.join(
            "simple_house",
            "fmus",
            op_sys,
            "modelica_simple_house_src_HP_u_Rad_1RC_Sun",
        ),
        "weather": "CH_ZH_Maur",
        "start_time": 0,  # [s]
        "stop_time": 21 * 24 * 3600,  # [s]
        "step_size": 5 * 60,  # [s]
        "states": [
            "heaPum.P",
            "heaPum.QCon_flow",
            "rad.Q_flow",
            "temRet.T",
            "temSup.T",
            "TOut.T",
            "temRoo.T",
        ],
        "params": {
            "therm_cond_G": 500,
            "heat_capa_C": 1e7,
        },
        "in_specs": {
            "u": {"type": "scalar", "lower_bound": -1, "upper_bound": 1}
        },
        "out_specs": {
            "y": {"type": "scalar", "lower_bound": -10, "upper_bound": 70}
        },
        "init": {"u": 0.0},
        # Controller I/O and Gains
        "input": "u",
        "sensor": "temRoo.T",
        "ref": T0 + 20,
        "kp": 0.1,
        "bound": [0, 1],
    }
    return mdl


def simple_house_slab():
    mdl = {
        # 'model_path'    : 'modelica\\HP1room\\fmus\\modelica_HP1room_srcmo_HP_u_Slab_1RC.fmu',
        "model_path": os.path.join(
            "simple_house",
            "fmus",
            op_sys,
            "modelica_simple_house_src_HP_u_Slab_1RC_Sun",
        ),
        "weather": "CH_ZH_Maur",
        "start_time": 0,  # [s]
        "stop_time": 21 * 24 * 3600,  # [s]
        "step_size": 5 * 60,  # [s]
        "states": [
            "heaPum.P",
            "heaPum.QCon_flow",
            "sla.surf_a.Q_flow",
            "temRet.T",
            "temSup.T",
            "TOut.T",
            "temRoo.T",
        ],
        "params": {
            "therm_cond_G": 500,
            "heat_capa_C": 1e7,
        },
        "in_specs": {
            "u": {"type": "scalar", "lower_bound": -1, "upper_bound": 1}
        },
        "out_specs": {
            "y": {"type": "scalar", "lower_bound": -10, "upper_bound": 70}
        },
        "init": {"u": 0.0},
        # Controller I/O and Gains
        "input": "u",
        "sensor": "temRoo.T",
        "ref": T0 + 20,
        "kp": 0.1,
        "bound": [0, 1],
    }
    return mdl


def sh_tank():
    mdl = {
        # "model_path": "modelica\\HP1room\\fmus\\modelica_HP1room_srcmo_HP_u_Tank_PI_Rad_1RC.fmu",
        "model_path": os.path.join(
            "simple_house",
            "fmus",
            op_sys,
            "modelica_HP1room_srcmo_HP_u_Tank_PI_Rad_1RC",
        ),
        "start_time": 0,  # [s]
        "stop_time": 21 * 24 * 3600,  # [s]
        "step_size": 5 * 60,  # [s]
        "states": [
            "heaPum.P",
            "heaPum.QCon_flow",
            "rad.Q_flow",
            "temHP2Hex.T",
            "temHex2HP.T",
            "temTan2Rad.T",
            "temRad2Tan.T",
            "TOut.T",
            "temRoo.T",
        ],
        "params": {
            "P_nominal": 5e3,
            "COP_nominal": 5,
            "gaiHP.k": 1.0,
            "therm_cond_G": 500,
            "heat_capa_C": 5e5,
        },
        "in_specs": {
            "hp_uin": {
                "type": "scalar",
                "lower_bound": 1,
                "upper_bound": 1,
            },
            "room_Tset": {
                "type": "scalar",
                "lower_bound": T0 + 4,
                "upper_bound": T0 + 40,
            },
        },
        "out_specs": {
            "hpT": {
                "type": "scalar",
                "lower_bound": T0 - 10,
                "upper_bound": T0 + 70,
            },
            "roomT": {
                "type": "scalar",
                "lower_bound": T0 + 0,
                "upper_bound": T0 + 40,
            },
        },
        "init": {"key": ["hp_uin", "room_Tset"], "val": [0.0, T0 + 20.0]},
        # Controller I/O and Gains
        "input": "hp_uin",
        # 'input'         : ['hp_uin', 'room_Tset'],
        "sensor": "temHP2Hex.T",
        "ref": T0 + 60,
        "kp": 0.1,
        "bound": [0, 1],
    }
    return mdl


# ============================================================================
# FMU Functions
# ============================================================================
def build_model(mdl):
    env = EnvModFMU(
        model_path=mdl["model_path"],
        start_time=mdl["start_time"],
        stop_time=mdl["stop_time"],
        step_size=mdl["step_size"],
        weather=mdl["weather"],
        input_specs=mdl["in_specs"],
        output_specs=mdl["out_specs"],
        kpi_options={},
    )
    # print(env.model_description)
    # env.build_action_space(input_specs = INPUT_SPECS)
    return env


def get_model_data(env, var):
    out = env.get_variable_data(var)
    return out


def set_model_param(env, pvar, pval):
    env.set_model_variables(pvar, pval)


def control_step(env, uvar, uval):
    env.step(inputs={uvar: [uval]})
    # env.step(inputs = dict(zip(uvar, uval)))


def controller(meas, ref, kp, bnd):
    uval = kp * (ref - meas)
    uval = np.min([np.max([uval, bnd[0]]), bnd[1]])
    return uval


# ============================================================================
# Plot Functions
# ============================================================================


def plot_dummy(mdl, record):
    row, col = 2, 1
    fig, ax = plt.subplots(row, col, sharex=True, num="co-simulation")

    record[mdl["states"]].plot(ax=ax[0])
    record[mdl["input"]].plot(ax=ax[1])
    ax[1].set_ylabel("input")
    # plt.show()


def plot_simple_house(mdl, record, model_name):
    row, col = 3, 1
    fig, ax = plt.subplots(row, col, sharex=True, num=model_name)

    (record[mdl["states"]].iloc[:, :3].abs() * 1e-3).plot(ax=ax[0])
    (record[mdl["states"]].iloc[:, 3:] - T0).plot(ax=ax[1])
    record[mdl["input"]].plot(ax=ax[row - 1])
    ax[0].set_ylabel("P [kW]")
    ax[1].set_ylabel("T [°C]")
    ax[2].set_ylabel("input")
    # plt.show()


def model_function(model_name: str):
    if model_name == "dummy":
        func = dummy_model
    elif model_name == "simple_house_rad":
        func = simple_house_rad
    elif model_name == "simple_house_slab":
        func = simple_house_slab
    elif model_name == "sh_tank":
        func = sh_tank
    else:
        print("no model available")
        func = None

    return func


def run_model(model_name: str):

    func = model_function(model_name)
    mdl = func()

    # Build model
    env = build_model(mdl)

    # Read parameters
    print(get_model_data(env, mdl["params"].keys()))

    # Set parameters and check
    set_model_param(env, mdl["params"].keys(), mdl["params"].values())
    print(get_model_data(env, mdl["params"].keys()))

    # Set initial conditions (for states and/or inputs) and check
    set_model_param(env, mdl["init"].keys(), mdl["init"].values())
    print(get_model_data(env, mdl["init"].keys()))
    print(get_model_data(env, mdl["states"]))

    # Init data record
    N = round((mdl["stop_time"] - mdl["start_time"]) / mdl["step_size"])
    record = pd.DataFrame(
        np.zeros((N, len(mdl["states"]) + 1)),
        index=np.arange(N) * mdl["step_size"],
        columns=["u"] + mdl["states"],
    )

    # Run feedback loop
    tic = time.time()
    for dt in record.index:

        # Get states, control law, and DoStep
        out = get_model_data(env, mdl["states"])
        uval = controller(
            out[mdl["sensor"]], mdl["ref"], mdl["kp"], mdl["bound"]
        )
        # uval = [controller(out[mdl['sensor']], mdl['ref'], mdl['kp'], mdl['bound']), T0+20]
        control_step(env, mdl["input"], uval)

        # Save into DataFrame
        record.loc[dt, mdl["input"]] = uval
        record.loc[dt, mdl["states"]] = out

    toc = time.time()
    print("Elapsed time: %.2f s" % (toc - tic))

    return mdl, record


def run_model_new(model_name: str):
    env = energym.make(model_name)
    # Init data record
    N = round((env.stop_time - env.start_time) / env.step_size)
    outputs = env.get_outputs()
    record = pd.DataFrame(
        np.zeros((N, len(outputs) + 1)),
        index=np.arange(N) * env.step_size,
        columns=["u"] + outputs,
    )

    extra_vals = {
        "ref": T0 + 20,
        "kp": 0.1,
        "bound": [0, 1],
    }

    # Get states
    out = env.get_variable_data(outputs)

    # Run feedback loop
    tic = time.time()
    for dt in record.index:

        # Get control law
        uval = controller(
            out["temRoo.T"],
            extra_vals["ref"],
            extra_vals["kp"],
            extra_vals["bound"],
        )

        # Save into DataFrame
        record.loc[dt, "u"] = uval
        record.loc[dt, outputs] = out

        # DoStep
        out = env.step({"u": [uval]})

    toc = time.time()
    print("Elapsed time: %.2f s" % (toc - tic))

    return record


def test_models():
    # List of models to be tested
    to_test = ["simple_house_rad", "simple_house_slab"]
    records ={}

    for model_name in to_test:

        mdl, record = run_model(model_name)
        assert record.to_numpy().sum() != 0
        records[model_name] = record

        # plot
        if "dummy" in mdl["model_path"]:
            plot_dummy(mdl, record)
        elif "simple_house" in mdl["model_path"]:
            plot_simple_house(mdl, record, model_name)
        else:
            print("no plot")
    return records


def test_new_models():
    # List of models to be tested
    to_test = ["SimpleHouseRad-v0", "SimpleHouseSlab-v0"]
    records = {}

    for model_name in to_test:

        record = run_model_new(model_name)
        assert record.to_numpy().sum() != 0
        records[model_name] = record
    return records


# ============================================================================
# Main
# ============================================================================
if __name__ == "__main__":
    plt.close("all")
    # records_new = test_new_models()
    records_old = test_models()
