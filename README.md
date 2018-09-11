# sbnd_coldfeasic_website

First the virtual environment must be setup
  source venv/bin/activate

the bash script run.sh is the 'GO button' 
  source run.sh
this script renames all the .html files to .html.j2 files to make jinja2 happy then runs the build/main.py script and converts the files back to .html format
This is done for aesthetics reasons because emacs frames .html files in a nice way where it doesn't .html.j2
