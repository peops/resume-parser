import os
import json
import shutil
import zipfile
from lxml import etree
from xml.dom import minidom
from parsy.parser import Parser 
from collections import OrderedDict


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
cache_path = 'cache/cv.zip'

# Make temporary directory in cache folder
shutil.copy(input_base_dir+filename, cache_path)
with zipfile.ZipFile(cache_path,"r") as zip_ref:
    zip_ref.extractall("cache/cv")
if os.path.isfile(cache_path):
    os.remove(cache_path)

# Locate the xml file to be parsed
doc_xml_path = 'cache/cv/word/document.xml'

# Parse the XML
tree = etree.parse(doc_xml_path)
root = tree.getroot()

# Save a pretty printed xml in the debugger directory
xmlstr = minidom.parseString(etree.tostring(tree)).toprettyxml(indent="   ")
with open("cache/debugger/sample.xml", "w") as f:
    f.write(xmlstr)

# Parse file
parser = Parser(root)
resume = parser.master

# Get default resume fields
config = 'config/default.json'
with open(config) as f:
    resume_config = json.load(f)

print(resume)

# parsed = OrderedDict()

# def similarity_single_lines(section, key, keywords, line):
# 	line = line[0].lower()
# 	for word in keywords:
# 		word = word.lower()
# 		if (line.find(word) == -1):
# 			parsed[line] = "TBD"
# 		else:
# 			parsed[line] = section

# def similarity_multiple_lines(section, key, keywords, line):
# 	line = ' '.join(line).lower()
# 	for word in keywords:
# 		word = word.lower()
# 		if (line.find(word) == -1):
# 			parsed[line] = "TBD"
# 		else:
# 			parsed[line] = section

# for i, line in enumerate(resume):
# 	if len(line) == 1:
# 		for section, attribute in resume_config.items():
# 			for key, keywords in attribute.items():
# 				similarity_single_lines(section, key, keywords, line)
# 	else:
# 		if isinstance(line[0], list):
# 			parsed[line[0][0]] = "table"
# 		elif isinstance(line[0], str):
# 			for section, attribute in resume_config.items():
# 				for key, keywords in attribute.items():
# 					similarity_multiple_lines(section, key, keywords, line)

# for key, val in parsed.items():
# 	print(key, "******>", val)
