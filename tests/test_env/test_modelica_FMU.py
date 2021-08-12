import numpy as np
import pandas as pd
import platform
import time

import matplotlib.pyplot as plt

import energym

# ============================================================================
# Constants
# ============================================================================
op_sys = platform.system().lower()

T0 = 273.15  # [K] Zero degree Celsius in Kelvin
cp = 4180  # [J/(kg K)] Water specific heat capacity


# ============================================================================
# Plot Functions
# ============================================================================


def set_plot_labels(ax):
    ax[0, 0].set_ylabel("I [W/m2]")
    ax[1, 0].set_ylabel("P [kW]")
    ax[2, 0].set_ylabel("T [°C]")
    ax[0, 1].set_ylabel("-")
    ax[1, 1].set_ylabel("mf [kg/s]")
    ax[2, 1].set_ylabel("-")


def plot_sh_rad(record, model_name):
    row, col = 3, 2
    fig, ax = plt.subplots(row, col, sharex=True, num=model_name)

    record["rad_Q"] = (
            (record["temSup.T"] - record["temRet.T"]) * record["rad.m_flow"] * cp
    )
    (
        record[
            [
                "weaBus.HDifHor",
                "weaBus.HDirNor",
                "weaBus.HGloHor",
                "weaBus.HHorIR",
                "sunRad.y",
            ]
        ]
    ).plot(ax=ax[0, 0])
    (
        record[
            [
                "preHea.Q_flow",
                "sunHea.Q_flow",
                "heaPum.QEva_flow",
                "heaPum.QCon_flow",
                "heaPum.P",
                "rad.Q_flow",
                "rad_Q",
            ]
        ].abs()
        * 1e-3
    ).plot(ax=ax[1, 0])
    (
        record[
            [
                "heaPum.TEvaAct",
                "heaPum.TConAct",
                "temRet.T",
                "temSup.T",
                "temRoo.T",
                "TOut.T",
            ]
        ]
        - T0
    ).plot(ax=ax[2, 0])
    record[["heaPum.COP", "heaPum.COPCar"]].plot(ax=ax[0, 1])
    record[["rad.m_flow"]].plot(ax=ax[1, 1])
    record[["u"]].plot(ax=ax[2, 1])
    set_plot_labels(ax)
    # plt.show()


def plot_sh_rsla(record, model_name):
    row, col = 3, 2
    fig, ax = plt.subplots(row, col, sharex=True, num=model_name)

    record["rad_Q"] = (
            (record["temSup.T"] - record["temRet.T"]) * record["sla.m_flow"] * cp
    )
    (
        record[
            [
                "weaBus.HDifHor",
                "weaBus.HDirNor",
                "weaBus.HGloHor",
                "weaBus.HHorIR",
                "sunRad.y",
            ]
        ]
    ).plot(ax=ax[0, 0])
    (
        record[
            [
                "preHea.Q_flow",
                "sunHea.Q_flow",
                "heaPum.QEva_flow",
                "heaPum.QCon_flow",
                "heaPum.P",
                "sla.QTot",
            ]
        ].abs()
        * 1e-3
    ).plot(ax=ax[1, 0])
    (
        record[
            [
                "heaPum.TEvaAct",
                "heaPum.TConAct",
                "temRet.T",
                "temSup.T",
                "sla.heatPortEmb[1].T",
                "temRoo.T",
                "TOut.T",
            ]
        ]
        - T0
    ).plot(ax=ax[2, 0])
    record[["heaPum.COP", "heaPum.COPCar"]].plot(ax=ax[0, 1])
    record[["sla.m_flow"]].plot(ax=ax[1, 1])
    record[["u"]].plot(ax=ax[2, 1])
    set_plot_labels(ax)
    # plt.show()


def plot_sh_slab(record, model_name):
    row, col = 3, 2
    fig, ax = plt.subplots(row, col, sharex=True, num=model_name)

    record["slab_Q"] = (
            (record["temSup.T"] - record["temRet.T"]) * record["sla.m_flow"] * cp
    )
    (
        record[
            [
                "weaBus.HDifHor",
                "weaBus.HDirNor",
                "weaBus.HGloHor",
                "weaBus.HHorIR",
                "sunRad.y",
            ]
        ]
    ).plot(ax=ax[0, 0])
    (
        record[
            [
                "preHea.Q_flow",
                "sunHea.Q_flow",
                "heaPum.QEva_flow",
                "heaPum.QCon_flow",
                "heaPum.P",
                "sla.surf_a.Q_flow",
                "sla.surf_b.Q_flow",
                "slab_Q",
            ]
        ].abs()
        * 1e-3
    ).plot(ax=ax[1, 0])
    (
        record[
            [
                "heaPum.TEvaAct",
                "heaPum.TConAct",
                "temRet.T",
                "temSup.T",
                "sla.surf_a.T",
                "sla.surf_b.T",
                "temRoo.T",
                "TOut.T",
            ]
        ]
        - T0
    ).plot(ax=ax[2, 0])
    record[["heaPum.COP", "heaPum.COPCar"]].plot(ax=ax[0, 1])
    record[["sla.m_flow"]].plot(ax=ax[1, 1])
    record[["u"]].plot(ax=ax[2, 1])
    set_plot_labels(ax)
    # plt.show()


def plot_tank_sh_rsla(record, model_name):
    row, col = 3, 1
    fig, ax = plt.subplots(row, col, sharex=True, num=model_name)

    (record[["heaPum.P", "heaPum.QCon_flow", "sla.QTot"]].abs() * 1e-3).plot(ax=ax[0])
    (record[["tanSH.heaPorSid.T", "sla.heatPortEmb[1].T",
             "temRoo.T", "TOut.T"]] - T0).plot(ax=ax[1])
    record[["uHP", "uRSla"]].plot(ax=ax[row - 1])
    ax[0].set_ylabel("P [kW]")
    ax[1].set_ylabel("T [°C]")
    ax[2].set_ylabel("inputs")
    # plt.show()


def select_plot_model(model_name: str):
    if "SimpleHouseRad" in model_name:
        func = plot_sh_rad
    elif "SimpleHouseRSla" in model_name or "SwissHouseRSlaW2W" in model_name or "SwissHouseRSlaA2W" in model_name:
        func = plot_sh_rsla
    elif "SimpleHouseSlab" in model_name:
        func = plot_sh_slab
    elif "SwissHouseRSlaTank" in model_name:
        func = plot_tank_sh_rsla
    else:
        print("no plot function available")
        func = None
    return func


# ============================================================================
# Model and control
# ============================================================================


def model_param(env, model_name):
    """Model parameters configuration"""
    param_fmu = {
        # "P_nominal": 1000,
        "COP_nominal": 3,
        # "therm_cond_G": 100,
        # "heat_capa_C": 40e6,
        # "TCon_nominal": T0 + 30,
        # "room_vol_V": 750,
    }
    # get_param = env.get_variable_data(["P_nominal"])
    # param_fmu["P_nominal"] = get_param["P_nominal"]*0.5

    param_read = [
        "P_nominal", "COP_nominal",
        "therm_cond_G", "heat_capa_C",
    ]

    if "SimpleHouseRad" in model_name:
        param_fmu = dict(**param_fmu, **{
            # "TRadSup_nominal": T0 + 40,
            # "TRadRet_nominal": T0 + 35,
        })
        param_read.extend([
            "Q_flow_nominal",
            "mHeaPum_flow_nominal",
        ])
    elif "SimpleHouseRSla" in model_name or "SwissHouseRSlaW2W" in model_name or "SwissHouseRSlaA2W" in model_name:
        param_fmu = dict(**param_fmu, **{
            # "slab_surf": 200,
        })
        param_read.extend([
            "Q_flow_nominal",
            "mHeaPum_flow_nominal",
            "slab_surf",
        ])
    elif "SimpleHouseSlab" in model_name:
        param_fmu = dict(**param_fmu, **{
            # "slab_surf": 200,
            # "slab_G_Abo": 1e3, #10e3,
            # "slab_G_Bel": 1e3, #120,
        })
        param_read.extend([
            "Q_flow_nominal",
            "mHeaPum_flow_nominal",
            "slab_G_Abo", "slab_G_Bel",
            "slab_surf",
        ])
    else:
        # param_fmu = {}
        # param_read = []
        pass

    print("old param:", env.get_variable_data(param_fmu))
    env.set_model_variables(list(param_fmu.keys()), param_fmu.values())
    print("new param:", env.get_variable_data(param_fmu))
    print("read param:", env.get_variable_data(param_read))


def control_param(model_name):
    """Feedback controller parameters"""
    if "Tank" in model_name:
        ctrl = {
            "inputs": ["uHP", "uRSla"],
            "sensor": ["tanSH.heaPorSid.T", "temRoo.T"],
            "ref": [T0 + 40, T0 + 21],
            "kp": [0.1, 0.04],
            "bound": [[0, 1], [0, 1]]
        }
    elif "TankDhw" in model_name:
        ctrl = {
            "inputs": ["uHP", "uRSla"],
            "sensor": ["tanSH.heaPorSid.T", "temRoo.T"],
            "ref": [T0 + 40, T0 + 21],
            "kp": [0.1, 0.04],
            "bound": [[0, 1], [0, 1]]
        }
    else:
        ctrl = {
            "inputs": ["u"],
            "sensor": ["temRoo.T"],
            "ref": [T0 + 20],
            "kp": [0.5],
            "bound": [[0, 1]]
        }
    return ctrl


def controller(meas, ref, kp, bnd):
    uval = kp * (ref - meas)
    uval = np.clip(uval, bnd[0], bnd[1])
    return uval


def run_model(model_name: str):
    env = energym.make(model_name)
    print(model_name)
    # Init data record
    N = round((env.stop_time - env.start_time) / env.step_size)
    outputs = env.get_outputs_names()
    record = pd.DataFrame(
        np.zeros((N, len(outputs) + 1)),
        index=np.arange(N) * env.step_size,
        columns=["u"] + outputs,
    )

    model_param(env, model_name)
    ctrl = control_param(model_name)

    # Get states
    out = env.get_variable_data(outputs)

    # Run feedback loop
    tic = time.time()
    for dt in record.index:
        # Get control law
        uval = [[controller(
            out[ctrl["sensor"][n]], ctrl["ref"][n], ctrl["kp"][n], ctrl["bound"][n]
            )] for n in range(len(ctrl["inputs"]))]

        # DoStep
        out = env.step(dict(zip(ctrl["inputs"], uval)))

        # Save into DataFrame
        record.loc[dt, ctrl["inputs"]] = [val[0] for val in uval]
        record.loc[dt, outputs] = [out[key] for key in outputs]

    toc = time.time()
    print("Elapsed time: %.2f s" % (toc - tic))

    return record, env


def test_models():
    # List of models to be tested
    # to_test = ["SimpleHouseRad-v0", "SimpleHouseSlab-v0", "SimpleHouseRSla-v0"]
    # to_test = ["SimpleHouseRSla-v0", "SwissHouseRSlaW2W-v0", "SwissHouseRSlaA2W-v0"]
    to_test = ["SimpleHouseRSla-v0", "SwissHouseRSlaW2W-v0", "SwissHouseRSlaA2W-v0", "SwissHouseRSlaTank-v0"]
    # to_test = ["SwissHouseRSlaTank-v0", "SwissHouseRSlaTankDhw-v0"]
    records, envs = {}, {}

    for model_name in to_test:
        record, env = run_model(model_name)
        assert record.to_numpy().sum() != 0
        records[model_name] = record
        envs[model_name] = env
        # plot
        plot_fun = select_plot_model(model_name)
        plot_fun(record, model_name)

    return records, envs


# ============================================================================
# Main
# ============================================================================
if __name__ == "__main__":
    plt.close("all")
    records, envs = test_models()
