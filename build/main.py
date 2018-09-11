import helpers.sbnd_coldFeAsic as sbnd
import os
import sys
from jinja2 import Template, Environment, FileSystemLoader
from glob import glob
from helpers import io, prep
from pprint import pprint #for printing out dictionaries

HTML_BASE = '/home/rlazur/public_html/coldFeAsic'

def main():
    print("starting...")

    prep.confirm_path(HTML_BASE)
    
    #get the dictionaries from the clean_summary for a first time build
    summary_list, master_run_dict, master_chip_dict, master_board_dict = sbnd.clean_summary()

    env = Environment(loader=FileSystemLoader('j2'))

    build_summary_page(summary_list,env)
    
    generic_page_builder(master_run_dict, env, 'runid')

    generic_page_builder(master_chip_dict, env, 'asicid')
    
    generic_page_builder(master_board_dict, env, 'boardid')   

    build_rates_page(master_chip_dict, env)
    
    print("...finished")


def generic_page_builder(master_dict, env, subdir):
    #first build the summary page (coldfeasic/subdir/index.html)
    summary_dir = os.path.join(HTML_BASE,subdir)
    summary_dict = prep.prep_summary(master_dict, subdir)
    template_name = 'coldfeasic_' + subdir[:-2] + '_summary.html.j2'
    #ensure path exists
    prep.confirm_path(summary_dir)
    #get template
    template_obj = env.get_template(template_name)
    #write html file
    with open(os.path.join(summary_dir,'index.html'), 'w') as html_file:
        text = template_obj.render(summary_dict)
        html_file.write(text)
    
    #...and build the the individual run pages    
    for key in master_dict.keys():
        indiv_dir = os.path.join(summary_dir,key)
        prep.confirm_path(indiv_dir)
        indiv_dict = prep.prep(master_dict, key, subdir, indiv_dir)
        template_name = 'coldfeasic_' + subdir[:-2] + '.html.j2'
        template_obj = env.get_template(template_name)
        with open(os.path.join(indiv_dir,'index.html'), 'w') as html_file:
            text = template_obj.render(indiv_dict)
            html_file.write(text)


def build_summary_page(summary_list, env):
    #build the summary html file (coldFeAsic/summary/index.html)
    #the summary list is a list of dictionaries
    #each dictionary contains boardid, chip names, run id
    #jinja prefers a dictionary not a list
    summary_dict = {'summary_list':summary_list}
    template_obj = env.get_template('coldfeasic_summary.html.j2')
    summary_dir = os.path.join(HTML_BASE,'summary') 
    prep.confirm_path(summary_dir)
    with open(summary_dir+'/index.html', 'w') as html_file:
        text = template_obj.render(summary_dict)
        html_file.write(text)

def build_rates_page(summary_dict, env):
    #builds the
    rates_dict = prep.prep_rates(summary_dict)
    template_obj = env.get_template('coldfeasic_testingrates.html.j2')

    with open('../public_html/coldFeAsic/testingrates/index.html', 'w') as html_file:
        text = template_obj.render(rates_dict)
        html_file.write(text)
    
if __name__ == "__main__":
    main()
