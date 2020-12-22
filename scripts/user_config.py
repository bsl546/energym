# -*- coding: utf-8 -*-
"""
Get user list of modelica libraries paths
Created on Mar 2020
@author: mxb
"""

import getpass

username = getpass.getuser()

config_dict = {}

config_dict["mxb"] = {
    "libs": [
        r"C:\Data\Projects\ModeLib\lbl-srg\modelica-buildings\Buildings",
        r"C:\Data\Projects\ModeLib\ibpsa\modelica-ibpsa\IBPSA",
        r"C:\Data\Projects\ModeLib\best\simulation\modelica",
    ]
}


config_dict["root"] = {
    "libs": [
        r"/home/libraries/modelica-buildings/Buildings",
        r"/home/libraries/modelica-ibpsa/IBPSA",
        r"/app/simulation/modelica",
    ]
}


config_dict["bsl"] = {
    "libs": [
        r"C:\Users\bsl\Documents\90_Other_scripts\Buildings-v7.0.0\Buildings 7.0.0",
        r"C:\Users\bsl\Documents\90_Other_scripts\modelica-ibpsa",
        r"C:\Users\bsl\Documents\20_Python_Scripts\170_Building_lib\code_refac\best\simulation\modelica",
    ]
}


libs = config_dict[username]["libs"]
