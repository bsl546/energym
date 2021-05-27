import numpy as np
import pandas as pd
import os, time
import platform

import matplotlib.pyplot as plt

# import energym
from energym.envs.env_fmu_mod import EnvModFMU


# ============================================================================
# Constants
# ============================================================================
op_sys = platform.system().lower()

T0 = 273.15   # [K] Zero degree Celsius in Kelvin
cp = 4180   # [J/(kg K)] Water specific heat capacity


# ============================================================================
# Model parameters
# ============================================================================

def sh_dhw_tank():
    mdl = {
        "model_path": os.path.join(
            "swiss_house",
            "fmus",
            op_sys,
            "HP_u_Tank_u_DHW_u_RSla_1RC_Sun",
        ),
        "weather": "CH_ZH_Maur",
        "start_time": 0,  # [s]
        "stop_time": 21 * 24 * 3600,  # [s]
        "step_size": 5 * 60,  # [s]
        "states": [
            "heaPum.P",
            "heaPum.QCon_flow",
            "sla.QTot",
            "temHP2Hex.T",
            "temHex2HP.T",
            "tanDHW.heaPorSid.T",
            "hotWaterTap.tem_in.T",
            "tanSH.heaPorSid.T",
            "temTan2Sla.T",
            "temSla2Tan.T",
            "sla.heatPortEmb[1].T",
            "temRoo.T",
            "TOut.T",
        ],
        "params": {
            "P_nominal": 1002,
            "COP_nominal": 3,
            "gaiHP.k": 1.0,
            "therm_cond_G": 102,
            "heat_capa_C": 40e6,
        },
        "in_specs": {
            "uHP": {
                "type": "scalar",
                "lower_bound": 0,
                "upper_bound": 1,
            },
            "uRSla": {
                "type": "scalar",
                "lower_bound": 0,
                "upper_bound": 1,
            },
            "uValveDHW": {
                "type": "scalar",
                "lower_bound": 0,
                "upper_bound": 1,
            },
            "uFlowDHW": {
                "type": "scalar",
                "lower_bound": 0,
                "upper_bound": 1,
            },
        },
        "out_specs": {
            "temHP": {
                "type": "scalar",
                "lower_bound": T0 + 10,
                "upper_bound": T0 + 60,
            },
            "temRoom": {
                "type": "scalar",
                "lower_bound": T0 + 0,
                "upper_bound": T0 + 40,
            },
        },
        "kpi_options": {},
        "init": {"key": ["uHP", "uRSla", "uValveDHW", "uFlowDHW"],
                 "val": [0.2, 0.0, 1.0, 0.0]},

        # Controller I/O and Gains
        "inputs": ["uHP", "uRSla"],
        "sensor": ["temHP2Hex.T", "temRoo.T"],
        "ref": [T0 + 60, T0 + 21],
        "kp": [0.1, 0.04],
        "bound": [[0, 1], [0, 1]],

        # Extra inputs for DHW
        "dhw": ["uValveDHW", "uFlowDHW"],
    }
    return mdl


# ============================================================================
# Plot functions
# ============================================================================

def plot_swiss_house(mdl, record, model_name):
    row, col = 3, 1
    fig, ax = plt.subplots(row, col, sharex=True, num=model_name)

    (record[mdl["states"]].iloc[:, :3].abs() * 1e-3).plot(ax=ax[0])
    (record[mdl["states"]].iloc[:, 3:] - T0).plot(ax=ax[1])
    record[mdl["inputs"] + mdl["dhw"]].plot(ax=ax[row - 1])
    ax[0].set_ylabel("P [kW]")
    ax[1].set_ylabel("T [°C]")
    ax[2].set_ylabel("inputs")
    # plt.show()


# ============================================================================
# FMU functions
# ============================================================================

def build_model(mdl):
    env = EnvModFMU(
        model_path=mdl["model_path"],
        start_time=mdl["start_time"],
        stop_time=mdl["stop_time"],
        step_size=mdl["step_size"],
        weather=mdl["weather"],
        params={},
        init_vals={},
        input_specs=mdl["in_specs"],
        output_specs=mdl["out_specs"],
        kpi_options=mdl["kpi_options"],
    )
    return env


def get_model_data(env, var):
    out = env.get_variable_data(var)
    return out


def set_model_param(env, pvar, pval):
    env.set_model_variables(pvar, pval)


def control_step(env, uvar, uval):
    env.step(inputs=dict(zip(uvar, uval)))


def controller(meas, ref, kp, bnd):
    uval = kp * (ref - meas)
    uval = np.min([np.max([uval, bnd[0]]), bnd[1]])
    return uval


# ============================================================================
# Model functions
# ============================================================================

def model_function(model_name: str):
    if model_name == "sh_dhw_tank":
        func = sh_dhw_tank
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
    set_model_param(env, list(mdl["params"].keys()), mdl["params"].values())
    print(get_model_data(env, mdl["params"].keys()))

    # Set initial conditions (for states and/or inputs) and check
    set_model_param(env, mdl["init"]["key"], mdl["init"]["val"])
    print(get_model_data(env, mdl["init"]["key"]))
    print(get_model_data(env, mdl["states"]))

    # Init data record
    N = round((mdl["stop_time"] - mdl["start_time"]) / mdl["step_size"])
    record = pd.DataFrame(
        np.zeros((N, len(mdl["inputs"] + mdl["dhw"]) + len(mdl["states"]))),
        index=np.arange(N) * mdl["step_size"],
        columns=mdl["inputs"] + mdl["dhw"] + mdl["states"],
    )

    # Run feedback loop
    tic = time.time()
    for dt in record.index:

        # Get states, control law, and DoStep
        out = get_model_data(env, mdl["states"])
        uval = [[controller(
            out[mdl["sensor"][n]], mdl["ref"][n], mdl["kp"][n], mdl["bound"][n]
            )] for n in range(len(mdl["inputs"]))]
        uval.extend([
            [0.5 + 0.4 * np.sin(2 * np.pi * dt/(24*3600))],  # DHW valve opening
            [0.2 + 0.1 * np.sin(2 * np.pi * dt/(6*3600))],  # tap flow
        ])
        control_step(env, mdl["inputs"] + mdl["dhw"], uval)

        # Save into DataFrame
        record.loc[dt, mdl["inputs"] + mdl["dhw"]] = [val[0] for val in uval]
        record.loc[dt, mdl["states"]] = [out[key] for key in mdl['states']]

    toc = time.time()
    print("Elapsed time: %.2f s" % (toc - tic))

    return mdl, record


def test_models():
    # List of models to be tested
    to_test = ["sh_dhw_tank"]
    records = {}

    for model_name in to_test:

        mdl, record = run_model(model_name)
        assert record.to_numpy().sum() != 0
        records[model_name] = record

        # plot
        if "swiss_house" in mdl["model_path"]:
            plot_swiss_house(mdl, record, model_name)
        else:
            print("no plot")
    return records


# ============================================================================
# Main
# ============================================================================
if __name__ == "__main__":
    plt.close("all")
    records = test_models()
