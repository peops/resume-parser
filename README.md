# resume-parser

Parse any resume/cv and extract relevant information

**THIS IS NOT YET COMPLETE, PLEASE DO NOT USE YET**

## Getting Started
***Step 1: Create a virtual environment and clone this repo***

```
pip3 install virtualenv
python3 -m virtualenv omnifin
source omnifin/bin/activate
git clone https://github.com/innovationchef/resume-parser.git
cd resume-parser
```

***Step 2: Install Python dependencies***

```
pip3 install -r requirements.txt
```

## Usage

***Step 1: Copy the resume that you want to parse in the data/input_doc directory***

***Step 2: Open parser.py in the root directory and set the variable "filename"***

***Step 3: Run the script***

```
python3 parser.py > output.txt
```

PS: You can see the parsed doc in the output.txt file in the root directory


## Algorithm
1. Take the input file - 'data/input_doc/sample.docx'
2. Copy and rename the file to another directory - 'cache/cv.zip' - using shutil
3. Unzip the directory to 'cache/cv/' - with zipfile.ZipFile(cache_path,"r") - read about "with" aka context managers
4. find the relevant document.xml - 'cache/cv/word/document.xml'
5. Parse this doc - etree.parse
6. get the root - tree.getroot()
7. Call the recursive function - get_Child()
8. if child.text is not None: - ie, child node contains some text (spaces, tabs, letters, numbers, spcl chars etc), then look at the text. If text contains any charater (other than spaces), that text is relevant -  if any(c.isalpha() for c in child.text) is True:
9. Then print the text 
10. Whatever happens, find the next child and go ondoing it - step 7
