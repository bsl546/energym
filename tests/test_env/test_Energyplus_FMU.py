import sys
from pathlib import Path

sys.path.append("..")

from energym import make
from energym.envs.utils.kpi import KPI
from energym.envs.utils.weather import EPW, MOS


def test_can_run_gym_interface_on_apartments_thermal():
    env = make("ApartmentsThermal-v0")
    episodes = 2
    n_steps_per_episode = 100
    for _ in range(episodes):
        observation = env.get_output()
        print(observation)
        for _ in range(n_steps_per_episode):
            action = env.sample_random_action()
            observation = env.step(action)
        print("Episode finished")
        env.reset()
    env.close()


def test_can_run_gym_interface_on_apartments_grid():
    env = make("ApartmentsGrid-v0")
    episodes = 2
    n_steps_per_episode = 100
    for _ in range(episodes):
        observation = env.get_output()
        print(observation)
        for _ in range(n_steps_per_episode):
            action = env.sample_random_action()
            observation = env.step(action)
        print("Episode finished")
        env.reset()
    env.close()


def test_can_run_gym_interface_on_apartments2_thermal():
    env = make("Apartments2Thermal-v0")
    episodes = 2
    n_steps_per_episode = 100
    for _ in range(episodes):
        observation = env.get_output()
        print(observation)
        for _ in range(n_steps_per_episode):
            action = env.sample_random_action()
            observation = env.step(action)
        print("Episode finished")
        env.reset()
    env.close()


def test_can_run_gym_interface_on_apartments2_grid():
    env = make("Apartments2Grid-v0")
    episodes = 2
    n_steps_per_episode = 100
    for _ in range(episodes):
        observation = env.get_output()
        print(observation)
        for _ in range(n_steps_per_episode):
            action = env.sample_random_action()
            observation = env.step(action)
        print("Episode finished")
        env.reset()
    env.close()


def test_can_run_gym_interface_on_offices_thermostat():
    env = make("OfficesThermostat-v0")
    episodes = 2
    n_steps_per_episode = 100
    for _ in range(episodes):
        observation = env.get_output()
        print(observation)
        for _ in range(n_steps_per_episode):
            action = env.sample_random_action()
            observation = env.step(action)
        print("Episode finished")
        env.reset()
    env.close()


def test_can_run_gym_interface_on_mixeduse_fan_fcu():
    env = make("MixedUseFanFCU-v0")
    episodes = 2
    n_steps_per_episode = 100
    for _ in range(episodes):
        observation = env.get_output()
        print(observation)
        for _ in range(n_steps_per_episode):
            action = env.sample_random_action()
            observation = env.step(action)
        print("Episode finished")
        env.reset()
    env.close()


def test_can_run_gym_interface_on_seminarcenter_thermostat():
    env = make("SeminarcenterThermostat-v0")
    episodes = 2
    n_steps_per_episode = 100
    for _ in range(episodes):
        observation = env.get_output()
        print(observation)
        for _ in range(n_steps_per_episode):
            action = env.sample_random_action()
            observation = env.step(action)
        print("Episode finished")
        env.reset()
    env.close()


def test_can_run_gym_interface_on_seminarcenter_full():
    env = make("SeminarcenterFull-v0")
    episodes = 2
    n_steps_per_episode = 100
    for _ in range(episodes):
        observation = env.get_output()
        print(observation)
        for _ in range(n_steps_per_episode):
            action = env.sample_random_action()
            observation = env.step(action)
        print("Episode finished")
        env.reset()
    env.close()


def full_test():
    test_can_run_gym_interface_on_apartments_thermal()
    test_can_run_gym_interface_on_apartments_grid()
    test_can_run_gym_interface_on_apartments2_thermal()
    test_can_run_gym_interface_on_apartments2_grid()
    test_can_run_gym_interface_on_offices_thermostat()
    test_can_run_gym_interface_on_mixeduse_fan_fcu()
    test_can_run_gym_interface_on_seminarcenter_thermostat()
    test_can_run_gym_interface_on_seminarcenter_full()


def epw_test():
    energym_path = Path(__file__).resolve().parent.parent.parent
    print(energym_path)
    weather_eplus = EPW()
    path_eplus = (
        energym_path
        / "simulation\\energyplus\\offices\\wf\\GRC_Athens.167160_IWEC.epw"
    )
    print(path_eplus)
    weather_eplus.read(path_eplus)
    print(weather_eplus.get_forecast(1, 1, 1, 24))
    weather_mod = MOS()
    path_mod = energym_path / "simulation\\modelica\\dummy\\wf\\Basel_Fixed.mos"
    weather_mod.read(path_mod)
    print(weather_mod.get_forecast(3600, 24))


def test_KPI_construct():
    kpi_opts1 = {
        "kpi1": {"name": "Z01_T", "type": "avg_dev", "target": [19, 23]},
        "kpi2": {"name": "Z01_T", "type": "tot_viol", "target": [19, 23]},
        "kpi3": {"name": "Fa_Pw_All", "type": "avg"},
        "kpi4": {"name": "Fa_Pw_All", "type": "sum"},
    }
    kpi = KPI(kpi_opts1)
    assert len(kpi.kpi_dict) == 4


def test_KPI_add():
    kpi_opts1 = {
        "kpi1": {"name": "Z01_T", "type": "avg_dev", "target": 22.0},
        "kpi2": {
            "name": "Z01_T",
            "type": "tot_viol",
            "target": [19.0, 23.0],
        },
        "kpi3": {"name": "Fa_Pw_All", "type": "avg"},
        "kpi4": {"name": "Fa_Pw_All", "type": "sum"},
    }
    kpi = KPI(kpi_opts1)
    obs = {
        "Fa_Pw_All": [100.0],
        "Z01_T": [21.0],
        "Ext_T": [15.1],
        "Something_else": [3],
    }
    kpi.add_observation(obs)
    res_dict = kpi.get_kpi()
    assert res_dict["kpi1"]["kpi"] == 1.0
    assert res_dict["kpi2"]["kpi"] == 0
    assert res_dict["kpi3"]["kpi"] == 100.0
    assert res_dict["kpi4"]["kpi"] == 100.0
    obs = {
        "Fa_Pw_All": [300.0],
        "Z01_T": [25.0],
        "Ext_T": [15.1],
        "Something_else": [3],
    }
    kpi.add_observation(obs)
    res_dict = kpi.get_kpi()
    assert res_dict["kpi1"]["kpi"] == 2.0
    assert res_dict["kpi2"]["kpi"] == 1
    assert res_dict["kpi3"]["kpi"] == 200.0
    assert res_dict["kpi4"]["kpi"] == 400.0


def test_KPI_cumulative():
    kpi_opts1 = {
        "kpi1": {"name": "Z01_T", "type": "tot_viol", "target": [19, 23]},
        "kpi2": {"name": "Z02_T", "type": "tot_viol", "target": [19, 23]},
        "kpi3": {"name": "Z03_T", "type": "tot_viol", "target": [19, 23]},
        "kpi4": {"name": "Fa_Pw_All", "type": "sum"},
    }
    kpi = KPI(kpi_opts1)
    obs = {
        "Fa_Pw_All": [100.0],
        "Z01_T": [21.0],
        "Z02_T": [15.1],
        "Z03_T": [3],
    }
    kpi.add_observation(obs)
    kpi_val = kpi.get_cumulative_kpi("_T", "tot_viol", "sum")
    assert kpi_val == 2


if __name__ == "__main__":
    full_test()
    epw_test()
    test_KPI_construct()
    test_KPI_add()
    test_KPI_cumulative()
