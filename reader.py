from tika import parser
import re

pattern = re.compile(r'\d,\d{3}\s\d*\s\d?\d,\d{2}\s\d*\s\d?\d,\d{2}')

raw = parser.from_file('pdf samples/Varfarina amostra 1 rep 1.pdf')
text = raw['content']

matches = re.findall(pattern, text)
#print(matches)
print(text)