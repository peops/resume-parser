import os
import re
import shutil
import zipfile
from lxml import etree

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
                    self.process_tbl(elem)

    def process_p(self, root):
        print(self.get_p_text(root, space = 1))
        print("**")

    def get_p_text(self, root, space = 1):
        text = list()
        for child in root:
            if child.text is not None:
                if any(c.isalpha() or c.isdigit() for c in child.text) is False:
                    pass
                else:
                    text.append(child.text)
            _text = self.get_p_text(child, space = space + 1)
            if len(_text) == 0:
                pass
            else:
                text.append(_text)
        return text 

    def process_tbl(self, root):
        print('****************************************************************************TABLE')
        self.find_rows(root)

    def find_rows(self, root):
        for row in root:
            tag = self.clean_tag(str(row.tag))
            if tag=='tr':
                print("****************************************ROW")
                print(self.process_row(row))

    def process_row(self, root):
        n_cells = 0
        for cell in root:
            n_cells += 1
            tag = self.clean_tag(str(cell.tag))
            if tag=='tc':
                print("************CELL")
                self.process_cell(cell)
        return n_cells

    def process_cell(self, root):
        for p in root:
            tag = self.clean_tag(str(p.tag))
            if tag=='p':
                self.process_p(p)


if __name__ == '__main__':
    i = 6    
    filename = str(i)+'.docx'
    name = filename[:-5]
    print('filename', name)
    input_base_dir = 'data/input_doc/'
    cache_path = 'cache/'+name+'.zip'
    shutil.copy(input_base_dir+filename, cache_path)
    with zipfile.ZipFile(cache_path,"r") as zip_ref:
        zip_ref.extractall("cache/"+name)
    if os.path.isfile(cache_path):
        os.remove(cache_path)

    doc_xml_path = 'cache/' + name + '/word/document.xml'

    tree = etree.parse(doc_xml_path)
    root = tree.getroot()
    parser = Parser(root)
    
    from xml.dom import minidom
    xmlstr = minidom.parseString(etree.tostring(tree)).toprettyxml(indent="   ")
    with open("debugger/sample.xml", "w") as f:
        f.write(xmlstr)
