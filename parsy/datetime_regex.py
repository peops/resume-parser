import re

ddmmyyyy = re.compile(r"(((0[1-9]|[12][0-9]|3[01])|[1-9])[- /.]((0[1-9]|1[012])|[1-9])[- /.]((19|20)\d\d|\d\d))")
mmddyyyy = re.compile(r"(((0[1-9]|1[012])|[1-9])[- /.]((0[1-9]|[12][0-9]|3[01])|[1-9])[- /.]((19|20)\d\d|\d\d))")
yyyymmdd = re.compile(r"(((19|20)\d\d|\d\d)[- /.]((0[1-9]|1[012])|[1-9])[- /.]((0[1-9]|[12][0-9]|3[01])|[1-9]))")

monthyearrange = re.compile(r"(((january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|sept|october|oct|november|nov|december|dec)(.)?(\s|-|–))?(19|20)\d\d(–|-)((19|20)\d\d|\d\d[^d]))", re.IGNORECASE)

monthyear = re.compile(r"((january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|sept|october|oct|november|nov|december|dec)([.]|\s|'\d\d|-\d\d|,)(\s)?((19|20)\d\d)?((0[1-9]|[12][0-9]|3[01])|[1-9])?(\s|st|nd|rd|th)?(,\s|\s)?((19|20)\d\d)?)", re.IGNORECASE)

year = re.compile(r"((19|20)\d\d)")

phonenumber = re.compile(r"[\d]{10}")

email = re.compile(r"\w+@\w+")