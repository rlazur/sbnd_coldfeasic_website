import os
import sys
from glob import glob

from helpers import io, raw

databasedir = '/dsk/1/data/sync-json'
seed_glob = '*/dsk/?/oper/sbnd_feasic/sbnd_quadFeAsic_cold/*'
methods = ["sync_adcs", "baseline_test_sequence-g2s2b0-0010", "baseline_test_sequence-g2s2b1-0010", "monitor_data_test_sequence-g2s2b0-0010", "input_alive_power_cycle_sequence-g2s2b0-0010"]

class Run(seed):
    def __init__(self):
        self.seed_paths = glob(os.path.join(databasedir,seed_glob))
        self.summary_list = []
        self.master_run_dict = {}
        self.master_chip_dict = {}
        self.master_board_dict = {}
        
