from os.path import dirname
import numpy as np

def get_dir_root():
    path = {}
    path["root"] = "/home/oberlav1/scratch/graphics/oberlav1/junction22"
    path["MSD_tags"] = path["root"] + "/MSD_tags"
    path["graph"] = path["root"] + "/graph_results"

    return path
