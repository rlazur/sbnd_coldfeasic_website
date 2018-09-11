import os
import sys
from glob import glob
import io

def get_timestamp(**params):
    return params.get("session_start_time")

def get_version(**params):
    return params.get("test_version")

def get_hostname(**params):
    return params.get("hostname")

def get_chipIDs(**params):
    chip_list = params.get("chip_lsit")
    chip_names
    for chip in chip_list:
        chip_names.append(chip_list[1])
    return chip_names

def get_boardID(**params):
    return params.get("boardid")

def common_params(**params):
    '''
    Return a relevent and common subset of data likely found in larger params.json
    '''
    return dict(category = "sbnd_feasic", femb_config = 'sbnd_quadFeAsic_cold', timestamp = get_timestamp(**params), version = get_version(**params), hostname = get_hostname(**params), chip_list = get_chipIDs(**params), boardID = get_boardID(**params))
