import os
import re
import json
import shutil
import zipfile
import  numpy as np
from lxml import etree
from parsy import regex
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

    def map(self):
        config = 'config/default.json'
        with open(config) as f:
            resume_config = json.load(f)
        
        blocks = self.create_blocks(resume_config)
        if blocks is None:
            return
        # print(blocks)
        for (start, end), sec in blocks.items():
            if sec == "EXPERIENCES":
                for i in range(start+1, end+1):
                    line = self.resume[i]
                    if len(line) == 1:
                        # pass
                        print(line)
                        # print(self.check_dates(line[0]))
                    else:
                        try:
                            table = np.array(line)
                            r, c = table.shape
                            self.pprint(table)
                            # print(table.shape)
                        except ValueError:
                            print(line)
                            # self.check_dates(line)

    def identify_section(self, line, resume_config):
        for sec, subsec in resume_config.items():
            keywords = subsec["HEADING"]
            for keyword in keywords:
                if line[0].lower().find(keyword.lower()) != -1:
                    if len(line[0].split(" ")) < 5:
                        return sec

    def create_blocks(self, resume_config):
        block_bounds = OrderedDict()
        for i, line in self.resume.items():
            if len(line) == 1:
                sec = self.identify_section(line, resume_config)
                if sec is not None:
                    block_bounds[i] = sec

        if len(block_bounds) == 0 :
            print("cannot Parse")
            return

        blocks = OrderedDict()
        blocks[(0, list(block_bounds.keys())[0]-1)] = "BUFFER"
        for i, (k, sec) in enumerate(block_bounds.items()):
            try:
                next_k = list(block_bounds.keys())[i+1]
            except IndexError:
                next_k = len(self.resume.items())
            blocks[(k, next_k-1)] = sec
        return blocks

    def check_dates(self, line):
        matches = list()
        matches.extend(self._check_dates(regex.ddmmyyyy, line))
        # matches.extend(self._check_dates(regex.mmddyyyy, line))
        # matches.extend(self._check_dates(regex.yyyymmdd, line))
        matches.extend(self._check_dates(regex.monthyearrange, line))
        matches.extend(self._check_dates(regex.monthyear, line))
        # matches.extend(self._check_dates(regex.year, line))
        return matches

    def check_email(self, line):
        return re.findall(regex.email, line)

    def check_phone(self, line):
        return re.findall(regex.phonenumber, line)

    def _check_dates(self, pattern, line):
        matches = list()
        m = re.findall(pattern, line)
        for i in m:
            matches.append(i[0])
        return matches
        
    def pprint(self, table):
        import pandas as pd
        df = pd.DataFrame(table)
        print (df)

# 16, 25, 45 =====> CV cannot be parsed
for i in range(1,47):
    Resume = ConnectFlask(str(i) + '.docx')
    # for i, line in Resume.resume.items(): 
    #     print(i, line)
    Resume.map()
    print("#############################################################3")
