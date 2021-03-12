import argparse
import os
import sys
import time
import shutil
import platform
import user_config  # for Modelica libraries

# Within JModelica.org-2.14 (Python 2.7)
from pymodelica import compile_fmu
import pymodelica

# to extend memory limit
pymodelica.environ["JVM_ARGS"] = "-Xmx4096m"

###############################################################################################
# Script to create fmu files from a folder with modelica files
###############################################################################################

PLATFORM = platform.system().lower()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Script to create a new environment")

    parser.add_argument(
        "-folder_name",
        action="store",
        default=None,
        help="Name of the environment folder, e.g. simple_house. All modelica folders are used if not specified.",
    )

    parser.add_argument(
        "-src",
        action="store",
        default=None,
        help="If specified, only the specified mo file will be transformed to fmu. Otherwise, all mo files in the folder are used.",
    )

    args = parser.parse_args()

    # Put correct path
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    parent_path = os.path.abspath(path)
    absolute_path = os.path.join(os.path.abspath(path), "simulation", "modelica")
    package_path = os.path.join(absolute_path, "package.mo")
    script_path = os.path.join(os.path.abspath(path), "scripts")
    working_dir = os.getcwd()

    if args.folder_name is None:
        list_dir_path = [
            os.path.join(absolute_path, p)
            for p in os.listdir(absolute_path)
            if os.path.isdir(os.path.join(absolute_path, p))
        ]
        list_folders = [
            p
            for p in os.listdir(absolute_path)
            if os.path.isdir(os.path.join(absolute_path, p))
        ]
    else:
        list_dir_path = [os.path.join(absolute_path, args.folder_name)]
        list_folders = [args.folder_name]

    for n, dir_path in enumerate(list_dir_path):
        sys.path.append(dir_path)
        fmus_path = os.path.join(dir_path, "fmus", PLATFORM)
        src_path = os.path.join(dir_path, "src")

        # Pickup model names
        with open(os.path.join(src_path, "package.order")) as f:
            list_mo = f.read().splitlines()

        if args.src is None:

            mo_full = [os.path.join(src_path, src) for src in os.listdir(src_path)]
            mo_reduced = list_mo
        else:
            mo_reduced = [args.src[:-3]]

        # Handle all the weather files: create duplicates from source,
        # Remember them to remove them afterwards
        if args.wf is None:
            w_reduced = ["weather"]  # [p[:-4] for p in os.listdir(w_path)]
        else:
            w_reduced = [args.wf[:-4]]

        print("The following mo files will be used to generate fmus:")
        print(mo_reduced)

        for i, mo in enumerate(mo_reduced):
            print("Modelica file: ", mo)

            for j, we in enumerate(w_reduced):

                print("Weather file: ", mo)

                # Modify mo file to have new weather file in it
                orig = open(mo_full[i], "rt")  # open lorem.txt for reading text
                contents = orig.read()  # read the entire file to string
                contents = re.sub(
                    "modelica://modelica/.*?.mos",
                    "modelica://modelica/"
                    + list_folders[n]
                    + "/wf/"
                    + w_reduced[j]
                    + ".mos",
                    contents,
                    flags=re.DOTALL,
                )

                contents = contents.replace(
                    "model " + mo_reduced[i],
                    "model " + mo_reduced[i] + "_" + w_reduced[j],
                )
                contents = contents.replace(
                    "end " + mo_reduced[i], "end " + mo_reduced[i] + "_" + w_reduced[j]
                )
                orig.close()

                src_new_weather = mo_full[i][:-3] + "_" + w_reduced[j] + ".mo"
                src_new_weather_reduced = mo_reduced[i] + "_" + w_reduced[j]
                new_src = open(src_new_weather, "wt")
                new_src.write(contents)
                new_src.close()

                print("creating fmu file for: " + src_new_weather_reduced)
                point_path = ".".join(
                    ["modelica", list_folders[n], "src", src_new_weather_reduced]
                )

                # Create the fmu
                temp_path = os.path.join(fmus_path, "tmp", src_new_weather_reduced)
                # os.makedirs(temp_path, exist_ok=True)
                if os.path.isdir(temp_path):
                    shutil.rmtree(temp_path, ignore_errors=False)
                os.makedirs(temp_path)
                os.chdir(temp_path)

                # Compile model with options
                fmu = compile_fmu(
                    point_path,
                    user_config.libs,
                    compiler="auto",
                    target="me+cs",
                    version="2.0",
                    compiler_options={},
                    compiler_log_level="info:%s.log" % mo,
                )
                print("Model compiled")
                found = [p for p in os.listdir(temp_path) if p.endswith(".fmu")][0]
                name_file = os.path.join(
                    fmus_path, "tmp", src_new_weather_reduced, found
                )

                if point_path.replace(".", "_") + ".fmu" in os.listdir(fmus_path):
                    shutil.rmtree(
                        os.path.join(fmus_path, point_path.replace(".", "_") + ".fmu"),
                        ignore_errors=True,
                    )  # Remove existing fmu files
                try:
                    shutil.copy2(
                        name_file,
                        os.path.join(fmus_path, mo_reduced[i] + ".fmu"),
                    )

                except BaseException as e:
                    print(e)

                os.chdir(fmus_path)
                # Remove temporary folder
                time.sleep(5)  # wait a few seconds
                try:
                    shutil.rmtree(temp_path, ignore_errors=False)
                except BaseException as e:
                    print(e)
                    pass

                os.chdir(working_dir)
                try:
                    os.remove(src_new_weather)
                except BaseException as e:
                    print(e)
                    pass
