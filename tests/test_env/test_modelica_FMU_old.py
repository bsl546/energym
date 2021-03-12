from timeit import default_timer as timer

import pandas as pd
import matplotlib.pyplot as plt

from energym.envs import EnvFMU
from pidLA import pidLA, doublePid

T0 = 273.15


def test_dummy_model():
    env = EnvFMU(
        model_path="modelica\\dummy\\fmus\\modelica_dummy_srcmo_vdp_osc.fmu",
        start_time=0,
        stop_time=1,
        step_size=0.01,
    )
    # print(env.model_description)
    INPUT_SPECS = {"u": {"type": "scalar", "lower_bound": -1, "upper_bound": 1}}
    env.__build_input_space(input_specs=INPUT_SPECS)
    outputs = env.step(inputs={"u": [0.1]})
    outputs = env.step(inputs={"u": [0.1]})
    outputs = env.step(inputs={"u": [0.1]})
    outputs = env.get_variable_data(["x1", "x2"])
    print(outputs)


def test_weather_forecast():
    INPUT_SPECS = {"u": {"type": "scalar", "lower_bound": 0, "upper_bound": 1}}
    env = EnvFMU(
        model_path="modelica\\HP1room\\fmus\\modelica_HP1room_srcmo_HP_u_Rad_1RC.fmu",
        start_time=0,
        stop_time=15000,
        step_size=300,
    )
    # print(env.model_description)
    env.__build_input_space(input_specs=INPUT_SPECS)

    # Look for weahter file
    env.look_for_weather_file()
    forecast = env.get_forecast()
    forecast_sun = env.get_forecast(
        key_list=[
            "Global Horizontal Radiation",
            "Direct Normal Radiation",
            "Diffuse Horizontal Radiation",
        ]
    )
    print(forecast_sun)


def PID_controller(ts, ref):
    I_term = 0.01 * ts / 60
    ctrl = pidLA(0.5, I_term, 0)  # Kp, Ki, Kd
    ctrl.set_saturation(0.0, 1.0)
    ctrl.set_awindup("clamp")
    ctrl.set_Ts(1)
    ctrl.set_reference(T0 + ref)
    return ctrl


def control_loop(env, ctrl, ts, in_var, out_var):
    n_steps = int(24 * 3600 * 1 / ts)
    inputs, outputs, outputs_other = [], [], []
    pid_p, pid_i = [], []
    timing = []
    for i in range(n_steps):
        start = timer()
        if i % int(24 * 3600 / ts) == 0:
            print("Starting day: {}".format(i // (24 * 3600 / ts)))
        input = {"u": ctrl.get_u()}
        try:
            output = env.step(inputs={in_var: [ctrl.get_u()]})
        except:
            print("failing at step: {}".format(i))
            break
        inputs.append(input)
        ctrl.calculate_u(output[out_var])
        outputs_other.append(env.get_variable_data(["heaPum.P", "heaPum.COP"]))
        pid_i.append(ctrl.I)
        pid_p.append(ctrl.P)
        outputs.append(output)
        timing.append(timer() - start)
    inputs = pd.DataFrame(inputs)
    outputs = pd.DataFrame(outputs)
    outputs_other = pd.DataFrame(outputs_other)
    IO = pd.concat([inputs, outputs, outputs_other], axis=1)
    IO["pid_I"] = pid_i
    IO["pid_P"] = pid_p
    IO["timing"] = timing
    IO.index = outputs["time"] / 3600
    IO.drop(columns=["time"], inplace=True)
    # outputs = env.step(inputs = {'u': [0.1]})
    # outputs = env.step(inputs = {'u': [0.1]}),
    # outputs_other = env.get_variable_data(['heaPum.P', 'rad.T_a_nominal', 'temRoo.T'])
    # inputs.plot()
    return IO


def test_HP1roomModel(ts):
    INPUT_SPECS = {"u": {"type": "scalar", "lower_bound": 0, "upper_bound": 1}}
    env = EnvFMU(
        model_path="modelica\\HP1room\\fmus\\modelica_HP1room_srcmo_HP_u_Rad_1RC.fmu",
        start_time=0,
        stop_time=500,
        step_size=ts,
    )
    # print(env.model_description)
    env.__build_input_space(input_specs=INPUT_SPECS)

    # # Look for weather file
    # env.look_for_weather_file()
    # forecast = env.get_forecast()
    # # Setting on e parameter
    variables = [
        "heat_capa_C",
        "therm_cond_G",
        "P_nominal",
        "COP_nominal",
        "heaCap.C",
        "theCon.G",
        "heaPum.P_nominal",
        "heaPum.COPCar",
    ]
    curr_value = env.get_variable_data(variables)
    # curr_value = env.get_variable_data([])
    print(
        [
            "%s (%s) = %s" % (p.name, p.causality, p.valueReference)
            for p in env.model_description.modelVariables
            if p.name in variables
        ]
    )
    # print('(var, val): {}'.format(curr_value))
    env.set_model_variables("heat_capa_C", curr_value["heat_capa_C"] * 10)
    env.set_model_variables("therm_cond_G", curr_value["therm_cond_G"])
    env.set_model_variables("P_nominal", curr_value["P_nominal"] / 4)
    env.set_model_variables("COP_nominal", curr_value["COP_nominal"] / 2)
    # env.set_model_variables('heaPum.P_nominal', curr_value['P_nominal']/4)
    # env.set_model_variables('heaPum.COP_nominal', curr_value['COP_nominal'])
    # env.set_model_variables('heaPum.COPCar', curr_value['heaPum.COPCar']+30)
    in_var = "u"
    out_var = "y"

    # Controller
    ctrl = PID_controller(ts, 20)

    # Control Loop
    IO = control_loop(env, ctrl, ts, in_var, out_var)

    IO.plot(subplots=True)
    plt.show()


def test_HP1TankRoomModel(ts):
    INPUT_SPECS = {
        "hp_uin": {"type": "scalar", "lower_bound": 0, "upper_bound": 1},
        "room_Tset": {"type": "scalar", "lower_bound": T0, "upper_bound": T0 + 40},
    }
    env = EnvFMU(
        model_path="modelica\\HP1room\\fmus\\modelica_HP1room_srcmo_HP_u_Tank_PI_Rad_1RC.fmu",
        start_time=0,
        stop_time=500,
        step_size=ts,
    )
    # print(env.model_description)
    # env.build_input_space(input_specs = INPUT_SPECS)

    # Set tank size
    curr_value = env.get_variable_data(["SH_tank_vol_m3"])
    # curr_value = env.get_variable_data([])
    print("Tank vol.: {}".format(curr_value))
    env.set_model_variables("SH_tank_vol_m3", 1.0)

    # Controller for room temp
    I_term = 5e-3 * ts / 60
    ctrl1 = pidLA(0.25, I_term, 0)
    ctrl1.set_saturation(0.0, 0.5)
    ctrl1.set_awindup("clamp")
    ctrl1.set_Ts(1)
