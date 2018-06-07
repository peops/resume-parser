import os
import re
import shutil
import zipfile
import itertools
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

    def get_body_elem(self, space= 1):
        for body in self.root:
            for elem in body:
                tag = self.clean_tag(str(elem.tag))
                if tag=='p':
                    self.process_p(elem)
                if tag=='tbl':
                    print('****************************************************************************TABLEBEGIN')
                    self.process_tbl(elem)
                    print('****************************************************************************TABLEEND')

    def process_p(self, root):
        p_text = self.get_p_text(root, space = 1)
        p_text = self.join_p(p_text)
        print(p_text)

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

    def get_p_text(self, root, space = 1):
        text = list()
        for child in root:
            if child.text is not None:
                text.append(child.text)
            if self.clean_tag(str(child.tag)) == "tab":
                text.append(" ")
            _text = self.get_p_text(child, space = space + 1)
            if len(_text) == 0:
                pass
            else:
                text.append(_text)
        return text

    def process_tbl(self, root):
        pattern = list()
        rows = list()
        for row in root:
            tag = self.clean_tag(str(row.tag))
            if tag=='tr':
                n_cells, row = self.process_row(row, count = True)
                pattern.append(n_cells)
                rows.append(row)
        # pattern = [1,6,6,6,6,6]
        pattern_indices = self.pattern_indices(pattern)
        # print(pattern_indices)
        used_rows = list()
        if len(pattern_indices)>1:
            for i, _ in enumerate(pattern_indices):
                if i == len(pattern_indices)-1:
                    break
                if pattern_indices[i+1]-pattern_indices[i] > 2:
                    for x in range(pattern_indices[i], pattern_indices[i+1]):
                        for cell in rows[x]:
                            print("************CELL")
                            self.process_cell(cell)
                        print("**********************************ROW")
                        used_rows.append(x)
                    for index in sorted(used_rows, reverse=True):
                        del rows[index]

        for remaining_row in rows:
            print("**********************************ROW")
            for cell in remaining_row:
                print("************CELL")
                self.process_cell(cell)

    def pattern_indices(self, pattern):
        index_pattern = [0]
        if any(len(list(g)) > 2 for k, g in itertools.groupby(pattern)):
            index = 0
            for i, (k, g) in enumerate(itertools.groupby(pattern)):
                temp = list(g)
                index = index+len(temp)
                index_pattern.append(index)
        return index_pattern

    def process_row(self, root, count):
        n_cells = 0
        cells = list()
        for cell in root:
            tag = self.clean_tag(str(cell.tag))
            if tag=='tc':
                n_cells += 1
                cells.append(cell)
                if count == False:
                    print("************CELL")
                    self.process_cell(cell)
        return n_cells, cells

    def process_cell(self, root):
        for p in root:
            tag = self.clean_tag(str(p.tag))
            if tag=='p':
                self.process_p(p)


if __name__ == '__main__':
    i = 10
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
