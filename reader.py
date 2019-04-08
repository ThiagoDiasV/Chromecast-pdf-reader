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
    path = (r'pdf samples/')
    files = glob(path + '/*.pdf')
    files.sort(key=os.path.getmtime)
    return files


def text_extract(*files: list) -> dict:
    '''
    Extracts pdf text.
    '''
    files_results_container = dict()
    pattern = re.compile(r'(PDA-\d{3}nm)|'
                         r'(\d,\d{3}\s\d*\s\d?\d,\d{2}\s\d*\s\d?\d,\d{2})')
    for file in files:
        file_name = os.path.basename(file)[:-4]
        raw = parser.from_file(file)
        text = raw['content']
        result_matches = re.findall(pattern, text)
        results_container = dict()
        for match in result_matches:
            if match[0]:
                key = match[0]
                results_container[key] = []
            elif match[1]:
                results_container[key].append(match[1].split(" "))

        files_results_container[file_name] = results_container
    return files_results_container


def create_workbook(**container: dict):
    '''
    Creates a workbook with results.
    Area% values above 5% will be inserted on worksheet.
    '''
    workbook = xlsxwriter.Workbook('teste.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 10, 15)
    row = 0
    col = 2
    columns_labels = ('Retention time', 'Area', 'Area%', 'Height', 'Height%')
    for label in columns_labels:
        worksheet.write_row(row, col, columns_labels)
    col = 0
    row = 1
    # A partir daqui é gambiarra
    for file_name, results in container.items():
        worksheet.write(row, col, file_name)
        for pda_lambda, values in results.items():
            if pda_lambda == 'PDA-283nm':
                worksheet.write(row, col + 1, pda_lambda)
                for value in values:
                    area = float(value[2].replace(',', '.'))
                    if area > 10:
                        worksheet.write_row(row, col + 2, value)
                        row += 1
        row += 1
    workbook.close()
    return workbook


if __name__ == '__main__':
    pdf_files = acquire_files()
    results_containers = text_extract(*pdf_files)
    workbook = create_workbook(**results_containers)