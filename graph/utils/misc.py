import os
import numpy as np

def get_dir_root(file_folder: str):
    path = {}
    path["root"] = file_folder
    path["MSD_tags"] = os.path.join(path["root"], "MSD_tags")
    path["graph"] = os.path.join(path["root"], "graph_results")

    return path
