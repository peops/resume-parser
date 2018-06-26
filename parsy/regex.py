import re

ddmmyyyy = re.compile(r"(((0[1-9]|[12][0-9]|3[01])|[1-9])[- /.]((0[1-9]|1[012])|[1-9])[- /.]((19|20)\d\d|\d\d))")
mmddyyyy = re.compile(r"(((0[1-9]|1[012])|[1-9])[- /.]((0[1-9]|[12][0-9]|3[01])|[1-9])[- /.]((19|20)\d\d|\d\d))")
yyyymmdd = re.compile(r"(((19|20)\d\d|\d\d)[- /.]((0[1-9]|1[012])|[1-9])[- /.]((0[1-9]|[12][0-9]|3[01])|[1-9]))")


monthyear1 = re.compile(r"((january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|sept|october|oct|november|nov|december|dec)((\.\s)|\s|,|,\s)((19|20)\d\d))", re.IGNORECASE)
monthyear2 = re.compile(r"((january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|sept|october|oct|november|nov|december|dec)('\d\d|’\d\d|-\d\d|–\d\d))", re.IGNORECASE)

monthdateyear = re.compile(r"((january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|sept|october|oct|november|nov|december|dec)((\.\s)|\s|'\d\d|’\d\d|-\d\d|–\d\d|,|,\s)((0[1-9]|[12][0-9]|3[01])|[1-9])(\s|st,|nd,|rd,|th,|,)\s?((19|20)\d\d)?)", re.IGNORECASE)

yearrange = re.compile(r"(((19|20)\d\d)(-|–)(((19|20)\d\d)|(\d\d)))", re.IGNORECASE)

year = re.compile(r"((19|20)\d\d)")



literal = re.compile(r"((to\still\sdate|to\still\snow|-\still\sdate|-\still\snow|–\still\sdate|–\still\snow|-\spresent|-present|–\spresent|–present|to\spresent))", re.IGNORECASE)

phonenumber = re.compile(r"[\d]{10}")

email = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", re.IGNORECASE)