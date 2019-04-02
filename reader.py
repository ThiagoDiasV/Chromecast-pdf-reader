from tika import parser
import re
from pprint import pprint
import xlsxwriter
from glob import glob
import os


def acquire_files() -> list:
    '''
    Puts all pdf files in a list.
    '''
    path = (r'/pdf samples')
    files = glob(path, '/*.pdf')
    files.sort(key=os.getmtime)
    return files


def text_extract(*files) -> list:
    '''
    Extracts pdf text.
    '''
    pattern = re.compile(r'(PDA-\d{3}nm)|'
                         r'(\d,\d{3}\s\d*\s\d?\d,\d{2}\s\d*\s\d?\d,\d{2})')
    for file in files:
        raw = parser.from_file(file)
    text = raw['content']
    result_matches = re.findall(pattern, text)
    return result_matches


def results_extract(regex_matches: list) -> dict:
    '''
    Returns a dict with results.
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
    worksheet.set_column(0, 10, 15)
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
    pdf_files = acquire_files()
    regex_matches = text_extract(*pdf_files)
    results = results_extract(regex_matches)
    workbook = create_workbook(**results)
