import re

ddmmyyyy = re.compile(r"((0[1-9]|[12][0-9]|3[01])|[1-9])[- /.]((0[1-9]|1[012])|[1-9])[- /.]((19|20)\d\d|\d\d[^]d])")
mmddyyyy = re.compile(r"((0[1-9]|1[012])|[1-9])[- /.]((0[1-9]|[12][0-9]|3[01])|[1-9])[- /.]((19|20)\d\d|\d\d[^]d])")
yyyymmdd = re.compile(r"((19|20)\d\d|\d\d[^]d])[- /.]((0[1-9]|1[012])|[1-9])[- /.]((0[1-9]|[12][0-9]|3[01])|[1-9])re.compile(r")

monthyearrange = re.compile(r"((january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|sept|october|oct|november|nov|december|dec)(.)?(\s|-|–))?(19|20)\d\d(–|-)((19|20)\d\d|\d\d[^d])")

monthyear = re.compile(r"((0[1-9]|[12][0-9]|3[01])|[1-9])(\s|(st|nd|rd|th)\s)?(january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|sept|october|oct|november|nov|december|dec)([.]|\s|'\d|-|,)(\s)?((0[1-9]|[12][0-9]|3[01])|[1-9])(st|nd|rd|th)?,?\s?((19|20)\d\d|\d\d[^]d])?")

year = re.compile(r"(19|20)\d\d[^\d]")

monthday = re.compile(r"(january|february|march|april|may|june|july|august|september|october|november|december)\s(0[1-9]|[12][0-9]|3[01])[^\d](,|\s)?((\s)?(19|20)\d\d)?")
smonthday = re.compile(r"(jan|feb|mar|apr|aug|sep|sept|oct|nov|dec)(\.|,)\s((0[1-9]|[12][0-9]|3[01])|[1-9])(,|\s)?((\s)?(19|20)\d\d)?")
