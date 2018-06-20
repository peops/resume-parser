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
        self.resume = []
        self.parse()

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
        self.resume = dict(zip(range(0, len(parser.master)), parser.master))
        ###############################################################################

    def map(self):
        config = 'config/default.json'
        with open(config) as f:
            resume_config = json.load(f)
        
        block_bounds = self.create_block_bounds(resume_config)
        blocks = self.create_blocks(block_bounds)
        for (start, end), sec in blocks.items():
            if sec == "EXPERIENCES":
                for i in range(start, end+1):
                    print(i, self.resume[i])

            if sec == "EDUCATIONAL QUALIFICATIONS":
                for i in range(start, end+1):
                    print(i, self.resume[i])


        # print(blocks)
            # else:
            #     try:
            #         table = np.array(line)
            #         r, c = table.shape
            #         # self.pprint(table)
            #     except ValueError:
            #         # print(i)
            #         pass
                      
    def identify_section(self, line, resume_config):
        for sec, subsec in resume_config.items():
            keywords = subsec["HEADING"]
            for keyword in keywords:
                if line[0].lower().find(keyword.lower()) != -1:
                    if len(line[0].split(" ")) < 5:
                        return sec

    def create_block_bounds(self, resume_config):
        block_bounds = OrderedDict()
        for i, line in self.resume.items():
            if len(line) == 1:
                sec = self.identify_section(line, resume_config)
                if sec is not None:
                    block_bounds[i] = sec
        return block_bounds

    def create_blocks(self, block_bounds):
        blocks = OrderedDict()
        blocks[(0, list(block_bounds.keys())[0]-1)] = "BUFFER"
        for i, (k, sec) in enumerate(block_bounds.items()):
            try:
                next_k = list(block_bounds.keys())[i+1]
            except IndexError:
                next_k = len(self.resume.items())
            blocks[(k, next_k-1)] = sec
        return blocks

    def pprint(self, table):
        import pandas as pd
        df = pd.DataFrame(table)
        print (df)


# 9.docx has error
Resume = ConnectFlask('1.docx')
# for i, line in Resume.resume.items(): 
#     print(i, line)
Resume.map()
