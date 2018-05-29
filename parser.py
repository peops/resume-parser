import shutil
import zipfile
from lxml import etree


def clean_tag(string):
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

def get_child(root, space = 1):
    for child in root:
        if child.text is not None:
            if any(c.isalpha() for c in child.text) is False:
                print("----"*space,clean_tag(str(child.tag)))
            else:
                print("----"*space,clean_tag(str(child.tag)), "      ", child.text)
        get_child(child, space = space + 1)
    return


if __name__ == '__main__':
    input_base_dir = 'data/input_doc/'
    cache_path = 'cache/cv.zip'
    filename = 'sample.docx'
    shutil.copy(input_base_dir+filename, cache_path)
    with zipfile.ZipFile(cache_path,"r") as zip_ref:
        zip_ref.extractall("cache/cv")

    doc_xml_path = 'cache/cv/word/document.xml'

    tree = etree.parse(doc_xml_path)
    root = tree.getroot()
    get_child(root)
