import os
import json
import shutil
import zipfile
import  numpy as np
from lxml import etree
from xml.dom import minidom
from parsy.parser import Parser 
from collections import OrderedDict


class ConnectFlask():
    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        filename = self.filename

        # Validate input file
        ext = os.path.splitext(filename)[-1].lower()
        if ext != ".docx":
            exit()

        # Extract file initial name
        name = os.path.splitext(os.path.basename(filename))[0]

        # input Folder
        input_base_dir = 'data/flask/'

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

        return resume

        ###############################################################################

        # config = 'config/default.json'
        # with open(config) as f:
        #     resume_config = json.load(f)
        
        # def match(keywords, item):
        #   for keyword in keywords:
        #       if item[0].lower().find(keyword.lower()) != -1:
        #           print(keyword, item)

        # for line in resume:
        #   if len(line) == 1:
        #       for sec, subsec in resume_config.items():
        #           for key, keywords in subsec.items():
        #               match(keywords, line)
        #               # print("******************************LINE")
        #   else:
        #       try:
        #           r, c = np.array(line).shape
        #           print("table")
        #       except ValueError:
        #           print("List of lists")
        #           