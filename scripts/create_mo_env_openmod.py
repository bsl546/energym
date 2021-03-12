import argparse
import os
import sys
import time
import shutil
import platform

###############################################################################################
# Script to create fmu files from a folder with mo files
###############################################################################################


BUILDINGS = "/home/libraries/modelica-buildings/Buildings/package.mo"
IBPSA = "/home/libraries/modelica-ibpsa/IBPSA/package.mo"


PLATFORM = platform.system().lower()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Script to create a new environment")

    parser.add_argument(
        "-folder_name",
        action="store",
        default=None,
        help="Name of the environment folder, e.g. haus. All modelica folders are used if not specified.",
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
        src_path = os.path.join(
            dir_path, "srcmo"
        )  # Change, the name should be src in next versions

        if args.src is None:
            mo_reduced = [
                p[:-3]
                for p in os.listdir(src_path)
                if p.endswith(".mo") and "package" in p
            ]
        else:
            mo_reduced = [args.src[:-3]]

        print(
            "The following mo files will be used to generate fmus: ",
            mo_reduced,
        )

        for i, mo in enumerate(mo_reduced):

            print("creating fmu file for :  \n " + mo)
            point_path = ".".join(["modelica", list_folders[n], "srcmo", mo_reduced[i]])

            # Create the fmu
            temp_path = os.path.join(fmus_path, "tmp", mo_reduced[i])
            os.makedirs(temp_path, exist_ok=True)
            os.chdir(temp_path)

            mos_file = open(r"create_fmutmp.mos", "w+")
            mos_file.write("loadModel(Modelica);\n")
            mos_file.write("loadModel(Complex);\n")
            mos_file.write("loadModel(ModelicaServices);\n")
            mos_file.write('loadFile("{}");\n'.format(BUILDINGS))
            mos_file.write('loadFile("{}");\n'.format(IBPSA))
            mos_file.write('loadFile("/app/simulation/modelica/package.mo");\n')
            mos_file.write('setCommandLineOptions("-d=initialization");\n')
            mos_file.write('setCommandLineOptions("-d=dumpLoops");\n')
            mos_file.write('setCommandLineOptions("-d=ignoreCycles");\n')
            mos_file.write(
                'buildModelFMU({}, version="2.0", fmuType="cs",includeResources=false);\n'.format(
                    point_path
                )
            )
            # platforms={"x86_64-linux-gnu"}
            mos_file.close()
            os.system("omc create_fmutmp.mos")

            found = [p for p in os.listdir(temp_path) if p.endswith(".fmu")][0]
            name_file = os.path.join(fmus_path, "tmp", mo_reduced[i], found)

            if point_path.replace(".", "_") + ".fmu" in os.listdir(fmus_path):
                shutil.rmtree(
                    os.path.join(fmus_path, point_path.replace(".", "_") + ".fmu"),
                    ignore_errors=True,
                )  # Remove existing files
            try:
                shutil.copy2(
                    name_file,
                    fmus_path,
                )
            except BaseException as e:
                print(e)
                pass

            os.chdir(fmus_path)
            # Remove  temporary folder
            time.sleep(5)  # wait a few seconds
            try:
                shutil.rmtree(temp_path, ignore_errors=False)
            except BaseException as e:
                print(e)
                pass
