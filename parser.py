import os
import re
import shutil
import zipfile
import itertools
import pandas as pd
from lxml import etree
from xml.dom import minidom

class Parser():
    def __init__(self, root):
        self.root = root
        self.get_body_elem()

    def clean_tag(self, string):
        for num, char in enumerate(string):
            if char == "{":
                pos1 = num
            if char == "}":
                pos2 = num 
            if char == "<":
                return
        dlte_str = ""
        while pos1 <= pos2:
            dlte_str = dlte_str + string[pos1]
            pos1 = pos1 + 1
        string = string.replace(dlte_str, "")
        return string

    def get_body_elem(self):
        for body in self.root:
            for elem in body:
                tag = self.clean_tag(str(elem.tag))
                if tag=='p':
                    if self.process_p(elem) is not None:
                        print("*************************************************PARABEGIN")
                        print(self.process_p(elem))
                        print("*************************************************PARAEND")
                if tag=='tbl':
                    print("*************************************************TABLEBEGIN")
                    self.process_tbl(elem)
                    print("*************************************************TABLEEND")

    def process_p(self, root):
        p_text = self.get_p_text(root)
        p_text = self.join_p(p_text)
        return p_text

    def join_p(self, x):
        if isinstance(x, str):
            return x
        elif isinstance(x, list):
            if len(x)>1:
                if isinstance(x[0], list):
                    merge = lambda x: list(itertools.chain.from_iterable(x))
                    x = merge(x)
                elif isinstance(x[0], str):
                    x = ''.join(x)
                return self.join_p(x)
            elif len(x) == 1:
                return self.join_p(x[0])
            else:
                return

    def get_p_text(self, root):
        text = list()
        for child in root:
            if self.clean_tag(str(child.tag)) == "align" or self.clean_tag(str(child.tag)) == "posOffset":
                continue
            if child.text is not None:
                text.append(child.text)
            if self.clean_tag(str(child.tag)) == "tab":
                text.append(" ")
            _text = self.get_p_text(child)
            if len(_text) == 0:
                pass
            else:
                text.append(_text)
        return text

    def process_tbl(self, root):
        rows = list()
        for elem in root:
            tag = self.clean_tag(str(elem.tag))
            if tag=='tr':
                row = self.process_row(elem)
                if len(row) != 0:
                    rows.append(row)
        pattern = [len(row) for row in rows]
        frame = list()
        for i, (row_len, row) in enumerate(zip(pattern,rows)):
            if row_len == 1:
                if len(frame) > 0 :
                    print(frame)
                frame = list()
                print(self.read_row_as_list(row))
            elif row_len  >  1:
                try:
                    if pattern[i] == pattern[i+1] or pattern[i] == pattern[i-1]:
                        frame_item = list()
                        for cell in rows[i]:
                            frame_item.append(self.process_cell(cell))
                        frame.append(frame_item)
                    else:
                        print(self.read_row_as_list(row))
                except IndexError:
                    if pattern[i] == pattern[i-1]:
                        frame_item = list()
                        for cell in rows[i]:
                            frame_item.append(self.process_cell(cell))
                        frame.append(frame_item)
                    else:
                        print(self.read_row_as_list(row))
        if len(frame) > 0 :
            print(frame)

    def read_row_as_list(self, row):
        row_data = list() 
        for cell in row:
            if self.process_cell(cell) is not None:
                row_data.append(self.process_cell(cell))
        return row_data

    def pattern_indices(self, pattern):
        index_pattern = [0]
        if any(len(list(g)) > 2 for k, g in itertools.groupby(pattern)):
            index = 0
            for i, (k, g) in enumerate(itertools.groupby(pattern)):
                temp = list(g)
                index = index+len(temp)
                index_pattern.append(index)
        return index_pattern

    def process_row(self, root):
        cells = list()
        for cell in root:
            tag = self.clean_tag(str(cell.tag))
            if tag=='tc':
                cells.append(cell)
        return cells

    def process_cell(self, root):
        p_group = list()
        for p in root:
            tag = self.clean_tag(str(p.tag))
            if tag=='p':
                if self.process_p(p) is not None:
                    p_group.append(self.process_p(p))
        return self.join_p(p_group)

if __name__ == '__main__':
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
    doc_xml_path = 'cache/' + name + '/word/document.xml'

    # Parse the XML
    tree = etree.parse(doc_xml_path)
    root = tree.getroot()
    parser = Parser(root)
    
    # Save a pretty printed xml in the debugger directory
    xmlstr = minidom.parseString(etree.tostring(tree)).toprettyxml(indent="   ")
    with open("debugger/sample.xml", "w") as f:
        f.write(xmlstr)
