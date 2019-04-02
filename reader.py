from tika import parser
import re
from pprint import pprint
import xlsxwriter


def text_extract() -> list:
    '''
    Extracts pdf text
    '''
    pattern = re.compile(r'(PDA-\d{3}nm)|'
                         r'(\d,\d{3}\s\d*\s\d?\d,\d{2}\s\d*\s\d?\d,\d{2})')
    raw = parser.from_file('pdf samples/Varfarina amostra 1 rep 1.pdf')
    text = raw['content']
    result_matches = re.findall(pattern, text)
    return result_matches


def results_extract(regex_matches: list) -> dict:
    '''
    Returns a dict with results
    '''
    results = dict()
    for match in regex_matches:
        if match[0]:
            key = match[0]
            results[key] = []
        elif match[1]:
            results[key].append(match[1].split(" "))
    return results


def create_workbook(**results: dict):
    '''
    Creates a workbook with results.
    Area% values above 5% will be inserted on worksheet.
    '''
    workbook = xlsxwriter.Workbook('teste.xlsx')
    worksheet = workbook.add_worksheet()
    row = col = 0
    columns_labels = ('Retention time', 'Area', 'Area%', 'Height', 'Height%')
    for label in columns_labels:
        worksheet.write(row, col+1, label)
        col += 1
    col = 0
    for key, values in results.items():
        worksheet.write(row+1, col, key)
        row += 1
        col = 1
        for value in values:
            if float(value[2].replace(',', '.')) > 5:
                worksheet.write_row(row, col, value)
                row += 1
        col = 0

    workbook.close()
    return workbook


if __name__ == '__main__':
    regex_matches = text_extract()
    results = results_extract(regex_matches)
    workbook = create_workbook(**results)
