import os
import json

def test(phrase):
    print(phrase)

def load(fp):
    '''
    Load JSON file
    '''
    dat = fp.read()
    return json.loads(dat)

def load_path(path):
    return load(open(path, encoding='utf-8'))

def serialize_date(dt):
    ret = int(dt.strftime("%s")) * 1000
    return ret

def dumps(dat):
    return json.dumps(dat, default=serialize_date, indent=4) + '\n'

def render(out, template, **params):
    path = os.path.realpath(template)
    base = os.path.dirname(path)
    rel = os.path.basename(path)
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader(base))
    env.globals.update(zip=zip)
    tmplobj = env.get_template(rel)
    text = tmplobj.render(**params)
    open(out,'w').write(text)
