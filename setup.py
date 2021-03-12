import setuptools
import os
import platform


def get_all_files():

    data_files = []

    dir_path = os.path.dirname(os.path.realpath(__file__))
    op_sys = platform.system().lower()

    # Energyplus & Modelica files
    Epath_rel = os.path.join("simulation", "energyplus")
    Epath_abs = os.path.join(dir_path, Epath_rel)
    Mpath_rel = os.path.join("simulation", "modelica")
    Mpath_abs = os.path.join(dir_path, Mpath_rel)

    # schedules files
    schedules_rel = os.path.join("energym", "schedules", "ScheduleFiles")
    schedules_abs = os.path.join(dir_path, schedules_rel)

    Edirs = [
        p for p in os.listdir(Epath_abs) if os.path.isdir(os.path.join(Epath_abs, p))
    ]
    Mdirs = [
        p for p in os.listdir(Mpath_abs) if os.path.isdir(os.path.join(Mpath_abs, p))
    ]

    # fmus
    listdirs_rel_fmus = [os.path.join(Epath_rel, p, "fmus", op_sys) for p in Edirs] + [
        os.path.join(Mpath_rel, p, "fmus", op_sys) for p in Mdirs
    ]

    listdirs_abs_fmus = [os.path.join(Epath_abs, p, "fmus", op_sys) for p in Edirs] + [
        os.path.join(Mpath_abs, p, "fmus", op_sys) for p in Mdirs
    ]

    # weather files
    listdirs_rel_wea = [os.path.join(Epath_rel, p, "wf") for p in Edirs] + [
        os.path.join(Mpath_rel, p, "wf") for p in Mdirs
    ]

    listdirs_abs_wea = [os.path.join(Epath_abs, p, "wf") for p in Edirs] + [
        os.path.join(Mpath_abs, p, "wf") for p in Mdirs
    ]

    for i, d in enumerate(listdirs_abs_fmus):

        files = [
            os.path.join(listdirs_rel_fmus[i], f)
            for f in os.listdir(d)
            if f.endswith(".fmu")
        ]
        data_files += [(listdirs_rel_fmus[i], files)]

    for i, d in enumerate(listdirs_abs_wea):

        files = [
            os.path.join(listdirs_rel_wea[i], f)
            for f in os.listdir(d)
            if f.endswith(".epw") or f.endswith(".mos")
        ]
        data_files += [(listdirs_rel_wea[i], files)]

    data_files += [
        (
            schedules_rel,
            [
                os.path.join(schedules_rel, f)
                for f in os.listdir(schedules_abs)
                if f.endswith(".csv")
            ],
        )
    ]

    return data_files


data_files = get_all_files()


setuptools.setup(
    name="energym",
    version="0.1",
    author="CSEM",
    author_email="",
    description="A benchmark for controllers of energy systems",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
        "pandas>=0.24",
        "FMPy>=0.2.14",
        "scipy>=1.2.3",
        "numpy>=1.16",
        "matplotlib>=2.2.5",
        "six>=1.13.0",
    ],
    data_files=data_files,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: None",
        "Operating System :: Windows :: Linux",
    ],
)
