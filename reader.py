from tika import parser
import re
from pprint import pprint


def text_extract():
    '''
    Extracts pdf text
    '''
    pattern = re.compile(r'(PDA-\d{3}nm)|'
                         r'(\d,\d{3}\s\d*\s\d?\d,\d{2}\s\d*\s\d?\d,\d{2})')
    raw = parser.from_file('pdf samples/Varfarina amostra 1 rep 1.pdf')
    text = raw['content']
    result_matches = re.findall(pattern, text)
    return result_matches


def results_extract(regex_matches):
    '''
    Returns a dict with results
    '''
    results = dict()
    for match in regex_matches:
        if match[0]:
            key = match[0]
            results[key] = []
        elif match[1]:
            results[key].append(match[1])
    return results


if __name__ == '__main__':
    regex_matches = text_extract()
    results = results_extract(regex_matches)
    pprint(results)
