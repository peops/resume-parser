import os
import shutil
import zipfile
from lxml import etree
from xml.dom import minidom
from parsy.parser import Parser 


i = 1
filename = str(i)+'.docx'

# Validate input file
ext = os.path.splitext(filename)[-1].lower()
if ext != ".docx":
    exit()

# Extract file initial name
name = os.path.splitext(os.path.basename(filename))[0]

# input Folder
input_base_dir = 'data/input_doc/'

# cache folder 
cache_path = 'cache/'+name+'.zip'

# Make temporary directory in cache folder
shutil.copy(input_base_dir+filename, cache_path)
with zipfile.ZipFile(cache_path,"r") as zip_ref:
    zip_ref.extractall("cache/"+name)
if os.path.isfile(cache_path):
    os.remove(cache_path)

# Locate the xml file to be parsed
doc_xml_path = 'cache/cv/word/document.xml'

# Parse the XML
tree = etree.parse(doc_xml_path)
root = tree.getroot()
parser = Parser(root)
print(parser.master)

# Save a pretty printed xml in the debugger directory
xmlstr = minidom.parseString(etree.tostring(tree)).toprettyxml(indent="   ")
with open("debugger/sample.xml", "w") as f:
    f.write(xmlstr)