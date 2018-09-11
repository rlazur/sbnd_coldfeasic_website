import os
import sys
from glob import glob

from helpers import io, raw

databasedir = '/dsk/1/data/sync-json'
seed_glob = '*/dsk/?/oper/sbnd_feasic/sbnd_quadFeAsic_cold/*'


def test(phrase):
    print(phrase)

def get_seed_paths():
    'return collection of seed paths'
    return glob(os.path.join(databasedir,seed_glob))

def dump_dir(fp):
    fps = glob(os.path.join(fp,'*'))
    base_names = []
    for path in fps:
        base_names.append(os.path.basename(path))
    return base_names
    

def get_release(params):
    code_location = params["femb_python_location"]
    return os.path.split(os.path.split(code_location)[0])[1]

def get_chiplist(seed):
    
    chip_names = []
    for path in glob(os.path.join(seed,'*')):
        if ('.json' not in path) and ('.txt' not in path): 
            chip_name = os.path.basename(path)
            chip_names.append(chip_name)
            completed_run = True
        #the runs that ONLY contain a params file are useless
        if len(chip_names) > 4:
            #print("these are the big runs: {}\n".format(run_dir_contents))
            chip_names = []
            #some files have extra directories, because shifters fixed a typo
            #the sync-json files reflect both the old and new versions of the label
            #some param files have the asic names stored in them
            for i in range(4):                    
                label = "asic"+str(i)+"id"
                data = io.load_path(os.path.join(seed,"params.json"))
                chip_names.append(data[label])
                completed_run = True
                
        #these runs failed, don't include them
        elif len(chip_names) < 4:
            #print("these are the small runs: {}\n".format(run_dir_contents))
            completed_run = False
            continue

    return chip_names, completed_run

def get_boardid(seed):
    #accepts seed to run directory and returns boardid
    run_data = io.load_path(os.path.join(seed,"params.json"))
    boardid = run_data['boardid']
    if not boardid:
        boardid = "unrecorded"
    return boardid

def check_result(seed, chip):
    #returns "Pass" or "Fail" if the chip passed or failed this run
    #assuming the seed is to the run directory
    #takes a look through each method directory because that's reliable
    methods = ["baseline_test_sequence-g2s2b0-0010", "baseline_test_sequence-g2s2b1-0010", "monitor_data_test_sequence-g2s2b0-0010", "input_alive_power_cycle_sequence-g2s2b0-0010"]
    for method in methods:
        try:
            method_data = io.load_path(os.path.join(seed,chip,method,'results.json'))            
            result = method_data["result"]
        except FileNotFoundError:
            return "Fail"
        if result == "Fail":
            return "Fail"
    return "Pass"
    
def clean_summary():
    '''
    grab the relevent info from the run directory and put it in a convenient JSON file for later
    '''
    seed_paths = get_seed_paths()
    summary_list = []
    master_run_dict = {}
    master_chip_dict = {}
    master_board_dict = {}
    methods = ["sync_adcs", "baseline_test_sequence-g2s2b0-0010", "baseline_test_sequence-g2s2b1-0010", "monitor_data_test_sequence-g2s2b0-0010", "input_alive_power_cycle_sequence-g2s2b0-0010"]
    #loop through all the runs
    for seed in seed_paths:
        completed_run = True
        found_config = False
        runid = os.path.basename(seed)

        run_dir_contents = glob(os.path.join(seed,"*"))
        
        #if the run has anything in it
        if len(run_dir_contents) > 0:
            run_data = io.load_path(os.path.join(seed,'params.json'))
            
            try:
                config_list = run_data["config_list"]
                found_config = True
            except KeyError:
                found_config = False
            
            code_release = get_release(run_data)

            chip_names, completed_run = get_chiplist(seed)
            
            #scan through the tests for each chip
            for chip in chip_names:
                chip_dir = os.path.join(seed,chip)
                for method in methods:
                    method_dir = os.path.join(chip_dir,method)
                    try:
                        method_data = io.load_path(os.path.join(method_dir,"results.json"))
                    except FileNotFoundError:
                        if "Sync_Plot_Monitor.png" not in  dump_dir(method_dir):
                            completed_run = False
                        else:
                            completed_run = True                            
                        
        #these runs are empty, ignore them
        else:
            #print("these are the empty runs: {}\n".format(run_dir_contents))
            completed_run = False
            continue


        #start building up the directories
        #each subdict will be used as a seed for the HTML pages
        if completed_run:
            summary_list = get_summarylist(summary_list, seed)
            master_run_dict = get_rundict(master_run_dict, seed)
            master_chip_dict = get_chipdict(master_chip_dict, seed)
            master_board_dict = get_boarddict(master_board_dict, seed)

    return [summary_list, master_run_dict, master_chip_dict, master_board_dict]
            
def get_boarddict(d, seed):
    run = os.path.basename(seed)
    chips, dummyvar = get_chiplist(seed)
    board = get_boardid(seed)

    if board not in d.keys():
        d[board] = []
    d[board].append({'runid':run, 'chips':chips})

    return d
            
def get_chipdict(d, seed):
    run = os.path.basename(seed)
    board = get_boardid(seed)
    chips, dummyvar = get_chiplist(seed)

    for chip in chips:
        if chip not in d.keys():
            d[chip] = []
        result = check_result(seed,chip)
        d[chip].append({'boardid':board, 'runid':run, 'result': result})

    return d

def get_rundict(d, seed):
    methods = ["sync_adcs", "baseline_test_sequence-g2s2b0-0010", "baseline_test_sequence-g2s2b1-0010", "monitor_data_test_sequence-g2s2b0-0010", "input_alive_power_cycle_sequence-g2s2b0-0010"]
    sync_pngs = []
    baseline1_pngs = []
    baseline2_pngs = []
    monitor_pngs = []
    alive_pngs = []
    run = os.path.basename(seed)
    board = get_boardid(seed)
    chips, dummyvar = get_chiplist(seed)

    d[run] = {'boardid': board, 'chips': chips}
    for m,method in enumerate(methods):
        d[run][method] = {}
        d[run][method]['results'] = []
        for i,chip in enumerate(chips):            
            method_dir = os.path.join(seed,chip,method)
            d[run][method]['gain'] = "14mV"
            d[run][method]['shape'] = "2us"
            if "g2s2b1" in method:
                d[run][method]['base'] = "900mV"
            else:
                d[run][method]['base'] = "200mV"

            if m == 0:
                d[run][method]['results'] = [{'result':'N/A'}, {'result':'N/A'}, {'result':'N/A'}, {'result':'N/A'},]
            else:
                try:
                    data = io.load_path(os.path.join(method_dir,'results.json'))                
                    try:
                        result = data['result']
                        if result in ["Pass", "Fail"]:
                            d[run][method]['results'].append({'result':result})
                        else:
                            d[run][method]['results'].append({'result':"N/A"})
                    except KeyError:
                        #the sync folder doesn't have a pass/fail key
                        d[run][method]['results'].append({'result':'N/A'})
                    try:
                            d[run][method][chip+'_config'] = data['config_list'][i]
                    except KeyError:
                            #this was an edition made to later versions of the code
                            pass
                except FileNotFoundError:
                    #the input_power_alive folder is sometimes skipped for time purposes
                    d[run][method]['results'].append({'result':'skipped'})
            for item in dump_dir(method_dir):
                if 'png' in item:
                    if m == 0:
                        sync_pngs.append(os.path.join(method_dir,item))
                        d[run][method]['pngs'] = sync_pngs
                    if m == 1:
                        baseline1_pngs.append(os.path.join(method_dir,item))
                        d[run][method]['pngs'] = baseline1_pngs
                    if m == 2:
                        baseline2_pngs.append(os.path.join(method_dir,item))
                        d[run][method]['pngs'] = baseline2_pngs
                    if m == 3:
                        monitor_pngs.append(os.path.join(method_dir,item))
                        d[run][method]['pngs'] = monitor_pngs
                    if m == 4:
                        alive_pngs.append(os.path.join(method_dir,item))
                        d[run][method]['pngs'] = alive_pngs

    return d
                       
def get_summarylist(d, seed):
    run = os.path.basename(seed)
    board = get_boardid(seed)
    chips, dummyvar = get_chiplist(seed)
    d.append({'runid':run,'boardid':board})
    for i,chip in enumerate(chips):
        key = 'asic'+str(i)
        d[-1][key] = chip

    return d
    
def unique(summary):
    'Return a short string which should be unique and usable as file base name'
    return "sbnd_coldFeAsic-{ident}".format(**summary)

def instdir(summary):
    'Return relative installation directory for one summary'
    if summary['boardID']:
        return "/sbnd_feasic/{boardID}/{timestamp}".format(**summary)
    else:
        return "/sbnd_feasic/boardunknown/{timestamp}".format(**summary)

