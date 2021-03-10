import argparse
import os
import sys
import time
import shutil
import platform

###############################################################################################
# Script to create fmu files from a folder with idfs files
###############################################################################################

# PLEASE, adapt the two line below for your local energyplus installation and the energyplustofmu local installation.
# The script run both on windows, ubuntu, centos and debian (TODO: the tests on ubuntu, centos and debian)

ENERGYPLUS_PATH = os.path.join("C:\\", "EnergyPlusV9-4-0", "Energy+.idd")
ENERGYPLUSTOFMU_PATH = os.path.join(
    "C:\\",
    "Users",
    "bsl",
    "Documents",
    "00_Apps",
    "EnergyPlusToFMU-v3.0.0",
    "Scripts",
    "EnergyPlusToFMU.py",
)

""" #############################  Docker paths  ############################
ENERGYPLUS_PATH = "/usr/local/EnergyPlus-9-4-0/Energy+.idd"
ENERGYPLUSTOFMU_PATH = os.path.join(
    "/home","libraries",
    "EnergyPlusToFMU",
    "Scripts",
    "EnergyPlusToFMU.py",
)
"""

PLATFORM = platform.system().lower()
if PLATFORM == "linux":
    pythoncom = "python3 "
else:
    pythoncom = "python "

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Script to create a new environment")

    parser.add_argument(
        "-folder_name",
        action="store",
        default=None,
        help="Name of the environment folder, e.g. apartments. All energyplus folders are used if not specified.",
    )

    parser.add_argument(
        "-src",
        action="store",
        default=None,
        help="If specified, only the specified idf file will be transformed to fmu. Otherwise, all idf files in the folder are used.",
    )

    parser.add_argument(
        "-wf",
        action="store",
        default=None,
        help="If specified, only one fmu with the specified epw file will be created. Otherwise, all .epw files in the folder are used.",
    )

    args = parser.parse_args()

    # Put correct path
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    parent_path = os.path.abspath(path)
    asbolute_path = os.path.join(os.path.abspath(path), "simulation", "energyplus")

    if args.folder_name is None:
        list_dir_path = [
            os.path.join(asbolute_path, p)
            for p in os.listdir(asbolute_path)
            if p != ".keep"
        ]
    else:
        list_dir_path = [os.path.join(asbolute_path, args.folder_name)]

    for dir_path in list_dir_path:
        sys.path.append(dir_path)
        fmus_path = os.path.join(dir_path, "fmus", PLATFORM)
        src_path = os.path.join(dir_path, "src")
        w_path = os.path.join(dir_path, "wf")
        parent_path_ext = os.getcwd()

        # Adresses
        if args.src is None:
            idf_files = [os.path.join(src_path, p) for p in os.listdir(src_path)]
            idf_reduced = [p[:-4] for p in os.listdir(src_path)]
        else:
            idf_files = [os.path.join(src_path, args.src)]
            idf_reduced = [args.src[:-4]]

        if args.wf is None:
            w_files = [os.path.join(w_path, "weather.epw")]
            w_reduced = [p[:-4] for p in os.listdir(w_path)]
        else:
            w_files = [os.path.join(w_path, args.wf)]
            w_reduced = [args.wf[:-4]]

        idf_files = ['"' + idf_file + '"' for idf_file in idf_files]
        w_files = ['"' + w_file + '"' for w_file in w_files]

        print(
            "The following idf files will be used to generate fmus: ",
            idf_files,
        )
        print(
            "The following weather files will be used to generate fmus: ",
            w_files,
        )

        for i, idf in enumerate(idf_files):
            for k, w in enumerate(w_files):
                cmd = (
                    pythoncom
                    + ENERGYPLUSTOFMU_PATH
                    + " -d -i "
                    + ENERGYPLUS_PATH
                    + " -w  "
                    + w
                    + " -a 2.0 "
                    + " -d -L "
                    + idf
                )
                print("creating file using command:  \n ")
                os.system(cmd)

                # move fmu files
                name_file_red = idf_reduced[i] + ".fmu"
                name_file = os.path.join(fmus_path, name_file_red)
                if name_file_red in os.listdir(fmus_path):
                    os.remove(name_file)  # Remove existing files
                try:
                    shutil.move(
                        os.path.join(parent_path_ext, idf_reduced[i] + ".fmu"),
                        name_file,
                    )
                except BaseException as e:
                    print(e)
                    pass

        # Remove folders if not removed by E+toFMU
        time.sleep(5)  # wait a few seconds
        dll_rm = [name + ".dll" for name in idf_reduced]
        to_rm = [
            os.path.join(parent_path_ext, p)
            for p in os.listdir(parent_path_ext)
            if "bld-" in p
            or "idf-to-fmu-export-prep-win" in p
            or "variables.cfg" in p
            or "modelDescription.xml" in p
            or "util-get-address-size" in p
            or p in dll_rm
        ]
        print(to_rm)
        for p in to_rm:
            try:
                if (
                    p.endswith(".exe")
                    or p.endswith(".dll")
                    or p.endswith(".cfg")
                    or p.endswith(".xml")
                ):
                    os.remove(p)
                else:
                    shutil.rmtree(p, ignore_errors=False)
            except BaseException as e:
                print(e)
                pass
