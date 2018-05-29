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
