#################################################################################
#--------------------------------------Core-------------------------------------#
#################################################################################
import os
class Retailor(object):
    """
    Retailor is another file traveller
    """
    def __init__(self, input_dir):
        self.input_dir=input_dir
        self.files = {}
        for Root, Dirs, Files in os.walk(input_dir):
           for f in Files:
               self.files[os.path.join(Root[len(input_dir)+1:] ,f)]={}
               self.files[os.path.join(Root[len(input_dir)+1:] ,f)]["content"]=open(
                   os.path.join(Root,f),"r").read()

    def use(self, plugin, *args, **kwargs):
        plugin(self, *args, **kwargs)
        return self

    def ls(self,meta,val=True):
        lst = []
        for key, value in self.files.iteritems():
            if "meta" in value and meta in value["meta"] and value["meta"][meta]==val:
                lst.append(os.path.join(self.input_dir,key))
        return lst
    def do(self):
        print "OK"
    
#################################################################################
#----------------------------------Meta Plugins---------------------------------#
#################################################################################
import yaml
import re
def yaml_frontmatter(retailor):
    """
    its load frontmatter to system and delete from content buffer
    """
    for key, value in retailor.files.iteritems():
        m=re.search(r'^\s*---(.*)---\s*(.*)$',value["content"],re.DOTALL)
        if m is not None:
            value["meta"] = yaml.load(m.group(1))
            value["content"] = m.group(2)


def meta_dir(retailor, directory, meta, val=True):
    for key, value in retailor.files.iteritems():
        if directory==os.path.dirname(key) and "meta" in value:
            value["meta"][meta]=val
        elif directory==os.path.dirname(key):
            value["meta"]={}
            value["meta"][meta]=val

            
#################################################################################
#--------------------------------Output Plugins---------------------------------#
#################################################################################

def save(retailor, destination):
    """
    file output for save 
    """
    if os.path.isdir(destination):
        pass
    else:
        os.makedirs(destination)

    for key, value in retailor.files.iteritems():
        out_location=os.path.join(destination, key)
        out_basename=os.path.dirname(out_location)
        if os.path.isdir(out_basename):
            pass
        else:
            os.makedirs(out_basename)

        if "generated" in value:
            with open(out_location,"w") as f:
                f.write(value["generated"])


def read_allcontent(retailor):
    """
    cli output for debug 
    """
    for key, value in retailor.files.iteritems():
        print(key)
        print(value["content"])

#################################################################################
#----------------------------Template Engine Plugins----------------------------#
#################################################################################

def jinja2(retailor, dct):
    from jinja2 import Environment, DictLoader
    env={}
    for key, value in retailor.files.iteritems():
        env[key]=value["content"]

    e = Environment(loader=DictLoader(env))
    e.list_templates()
    for key, value in retailor.files.iteritems():
        if "meta" in value and "render" in value["meta"] and value["meta"]["render"] is True:
            template = e.get_template(key)
            value["generated"] = template.render(dct)

#################################################################################
#------------------------------------End----------------------------------------#
#################################################################################
